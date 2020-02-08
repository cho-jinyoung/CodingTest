## lec01. 기본적인 Machine Learning의 용어와 개념 설명
> - supervised learning :learning with labeled example 
>   - 이미 레이블이 달려있는 데이터를 학습  (training dataset)  
>   - image labeling  
>   - predicting exam score based on time spent →regression  
>   - pass/non-pass(Letter grade) based on time spent →binary(multi-label) classification  
> - unsupervised learning :google news grouping, word clustering   
>   - 데이터를 보고 스스로 학습  

## lab01. tensorflow설치 및 기본적인operations
- Python3.6, Anaconda 설치  
- Anaconda prompt 에서 
```
> python -m pip install --upgrade pip
> conda create -n tensorflow python
```
-tensorflow 가상환경으로 들어가서 tensorflow설치  
```
> activate tensorflow
(tensorflow) > pip install tensorflow
```

### Tensorflow Machine
1. Build graph using tensorflow operations
2. Feed data and run graph(operation) **sess.run(op)**
3. update variables in the graph(and return values)

```
//Computational Graph
import tensorflow as tf

node1=tf.constant(3.0, tf.float32)  //1. 노드 하나 생성
node2=tf.constant(4.0)
node3=tf.add(node1, node2) 

sess=tf.Session() //2. 실행시키기 위해서는 session이 필요
print("sess.run(node1, node2): ", sess.run([node1, node2]))  //session run이 리턴하는 값을 출력
print("sess.run(node3): ", sess.run(node3))
```
[tensor rank, shapes, types](https://chromium.googlesource.com/external/github.com/tensorflow/tensorflow/+/r0.7/tensorflow/g3doc/resources/dims_types.md)
