# Decorator

기존의 코드에 여러가지 기능을 추가하는 파이썬 구문

```decorator.py```

```python
def outer_function(msg):
    def inner_function():
        print msg
    return inner_function

hi_func = outer_function('Hi')
bye_func = outer_function('Bye')

hi_func()
bye_func()
```
