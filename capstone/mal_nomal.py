import pandas as pd
from collections import Counter

gramdata=pd.read_csv("C:/Users/ycjy0/Documents/_cho/capstone/4-1/DataSet/ngram.csv", sep=",", dtype='unicode')
maldata=pd.read_csv("C:/Users/ycjy0/Documents/_cho/capstone/4-1/DataSet/nomal.csv", sep=",", dtype='unicode')

gram_name=gramdata["filename"]
gram_class=gramdata["class"]

#mal_name=maldata["name"]
#mal_class=maldata["class"]


for i, row in gramdata.iterrows(): 
	for j, j_row in maldata.iterrows():
		if (j_row['name']==row['filename']) :
			row['class']='0'
		else :
			row['class']='1'
		print(row['filename'], row['class'])
#	else :
#		lst2.append({'name': n, 'class': c})

