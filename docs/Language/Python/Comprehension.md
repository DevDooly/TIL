# Comprehension

iterable 한 오브젝트를 생성하기위한 방법 중 하나.

## 종류
* List Comprehension (LC)
* Set Comprehension (SC)
* Dict Comprehension (DC)
* Generator Expression (GE)

## List Comprehension (LC)
List Comprehension 은 리스트를 쉽게 생성하기 위한 방법이다.  

```python
# 20까지의 짝수를 출력하기 위해 다음과 같은 LC를 사용할 수 있다
evens = [x * 2 for x in range(11)]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# 리스트의 모든 원소값을 정규화 시킨 후 상수값을 더하는 LC
vals = [32, 12, 96, 42, 32, 93, 31, 23, 65, 43, 76]
amount = sum(vals)
norm_and_move = [(x / amount) + 1 for x in vals]
# [1.0587155963302752, 1.0220183486238532, 1.1761467889908257, 1.0770642201834861, 1.0587155963302752, 1.1706422018348623, 1.0568807339449542, 1.0422018348623854, 1.1192660550458715, 1.0788990825688074, 1.1394495412844037]
```



## References 
* https://mingrammer.com/introduce-comprehension-of-python/
* 
