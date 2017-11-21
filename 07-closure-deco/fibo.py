# -*- coding: utf-8 -*-

import functools
from clockdeco import clock


@clock
def fibonacci_slow(n):
    if n < 2:
        return n
    return fibonacci_slow(n - 2) + fibonacci_slow(n - 1)


# 使用缓存，速度更快
@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)



if __name__ == '__main__':
    print(fibonacci(10))
