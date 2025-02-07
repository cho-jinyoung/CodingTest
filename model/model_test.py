from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Classifiers():
	def __init__(self, X, Y):
		labels = np.unique(Y)
 		self.x_train, self.x_test, self.y_train, self.y_test = \
 		train_test_split(X, Y, test_size=0.2, random_state=0)

	def do_svm(self):
		clf = SVC()
		clf.fit(self.x_train, self.y_train)
		y_pred = clf.predict(self.x_test)

		return accuracy_score(self.y_test, y_pred)

	def do_randomforest(self):
		clf = RandomForestClassifier()
		clf.fit(self.x_train, self.y_train)

		y_pred = clf.predict(self.x_test)

   		return accuracy_score(self.y_test, y_pred)

	def do_xgboost(self):
		clf = XGBClassifier()
		clf.fit(self.x_train, self.y_train)
		
		y_pred = clf.predict(self.x_test)
		
		return accuracy_score(self.y_test, y_pred)

	def do_dnn(self):
		if "Series" in str(type(self.y_train)):
			self.y_train = self.y_train.to_frame()
			self.y_test = self.y_test.to_frame()
			input_len = len(self.x_train.columns)
		else:
			self.y_train = self.y_train.reshape(len(self.y_train), 1)
			self.y_test = self.y_test.reshape(len(self.y_test), 1)
			input_len = np.size(self.x_train, 1)

		learning_rate = 0.001
		batch_size = 128
		training_epochs = 15
		keep_prob = 0.5

		x_train = self.x_train
		y_train = self.y_train

		X = tf.placeholder(tf.float32, [None, input_len])
		Y = tf.placeholder(tf.float32, [None, 1])

		W1 = tf.Variable(tf.random_normal([input_len, 1024]), name='weight1')
		b1 = tf.Variable(tf.truncated_normal([1024]), name='bias1')
		L1 = tf.sigmoid(tf.matmul(X, W1) + b1)

		W2 = tf.Variable(tf.random_normal([1024, 128]), name='weight4')
		b2 = tf.Variable(tf.truncated_normal([128]), name='bias4')
		L2 = tf.sigmoid(tf.matmul(L1, W2) + b2)

		W3 = tf.Variable(tf.random_normal([128, 1]), name='weight5')
		b3 = tf.Variable(tf.truncated_normal([1]), name='bias5')
		
		output = tf.sigmoid(tf.add(tf.matmul(L2, W3), b3))

		cost = -tf.reduce_mean(Y * tf.log(output) + (1 - Y) * tf.log(1 - output))
		train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

		predicted = tf.cast(output > 0.5, dtype=tf.float32)
		accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))

		with tf.Session() as sess:
			sess.run(tf.global_variables_initializer())

			for epoch in range(training_epochs):
				avg_cost = 0
				total_batch = int(len(x_train) / batch_size)

				for i in range(total_batch-1):
					batch_xs = x_train[i*batch_size:(i+1)*batch_size]
					batch_ys = y_train[i*batch_size:(i+1)*batch_size]

					_ , c =sess.run([train, cost], feed_dict={X: batch_xs, Y: batch_ys})

			acc =  sess.run(accuracy, feed_dict={X: self.x_test, Y: self.y_test})

		return acc


	def do_all(self):
		rns = []

		#rns.append(self.do_svm())
		rns.append(self.do_randomforest())
		rns.append(self.do_xgboost())
		rns.append(self.do_dnn())

		return rns
def hot_encoding(df):
    enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
    lab = LabelEncoder()    

    dat = df['packer_type']
    lab.fit(dat)
    lab_dat = lab.transform(dat)

    df = df.drop('packer_type', 1)
    lab_dat = lab_dat.reshape(len(lab_dat), 1)
    enc_dat = enc.fit_transform(lab_dat)
    enc_dat = pd.DataFrame(enc_dat, columns=lab.classes_)

    df = df.reset_index(drop=True)
    enc_dat = enc_dat.reset_index(drop=True)
    
    df = pd.concat([df, enc_dat], axis=1)

    return df, lab.classes_

def pe_packer(pe_all):
	pe_all = pe_all.drop(['filename', 'MD5'], 1)

	pe_all, classes_ = hot_encoding(pe_all)

	pe_all = pd.DataFrame(pe_all)
	pe_all.to_csv('pe_packer.csv', index=False)

	Y = pe_all['class'] 
	X = pe_all.drop('class', axis=1)

	md_pe_packer = Classifiers(X, Y)
	
	return md_pe_packer.do_all()

def pe_predit(pe_all):
	NA_values = pe_all.isnull().values.sum()
	pe_all = pe_all.dropna()

	pe_all = pe_all.drop(['filename', 'MD5', 'packer_type'], 1)
	
	Y = pe_all['class']
	X = pe_all.drop('class',1)
	Y_bak = Y

	md_pe = Classifiers(X,Y)
	
	return md_pe.do_all()
	

def gram(gram_all):	
	gram_all = gram_all.drop(['filename', 'MD5'], 1) 

	Y = gram_all['class']
	X = gram_all.drop('class', 1) 
	md_gram = Classifiers(X, Y)

	return md_gram.do_all()

def main():
	colum = ["randomforest", "xgboost", "dnn"]
	df = pd.DataFrame(columns=colum)
	
	pe_all = pd.read_csv('./DataSet/PE/pe_header_all.csv')
	gram_all = pd.read_csv('./DataSet/ngram/ngram_all.csv')

	df.loc['pe'] = pe_predit(pe_all)
	df.loc['pe_packer'] = pe_packer(pe_all)
	df.loc['ngram'] = gram(gram_all)
	
	avg_pe = df.loc['pe'].mean(axis=0)
	avg_pe_packer = df.loc['pe_packer'].mean(axis=0)
	avg_ngram = df.loc['ngram'].mean(axis=0)

	#mv_clf = MajorityVoteClassifier(classifiers=[pipe1, clf2, pipe3])

	#clf_labels += ['Majority voting']
	#all_clf = [pipe1, clf2, pipe3, mv_clf]
	
	print(df)

if __name__ == '__main__':
	main()
