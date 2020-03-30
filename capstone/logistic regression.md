![image](https://user-images.githubusercontent.com/54131109/77319293-ec275280-6d51-11ea-8b69-6bc5857125ac.png)


## 분류 모델
 → 어떤 분류 모델을 사용할 것인지, 어떤 모델이 가장 뛰어난 성능을 내는지는 학습에 사용하는 데이터셋에 따라 다르다
   [알고리즘 훈련을 위한 주요 단계]
1. 특성을 선택하고 훈련 샘플을 모음
2. 성능 지표 선택
3. 분류 모델과 최적화 알고리즘 선택
4. 모델의 성능 평가
5. 알고리즘 튜닝


## Logistic regression
- odds ratio :특정 이벤트가 발생할 확률 = p/(p-1) → 로그함수를 취해 logic함수 정의
- logit함수를 뒤집어서 logistic sigmoid함수 정의
- logistic sigmoid function =특정 샘플이 클래스 1에 속할 확률 ∅(z)=P(y=1|x;w)
ex) ∅(z)=0.8 → 확률이 80%, P(y=0|x;w)=1-P(y=1|x;w)=0.2 → 확률이 20%
- cost function :제곱 오차합 비용함수
![cost function](https://user-images.githubusercontent.com/54131109/77937256-0bdcee80-72ef-11ea-8480-77ccf6ae9f7a.png)

→클래스 1에 속한 샘플을 정확히 예측하면 비용이 0에 가까워지고 클래스 0에 속한 샘플을 y=0으로 정확히 예측하면 y축의 비용이 0에 가까워짐
