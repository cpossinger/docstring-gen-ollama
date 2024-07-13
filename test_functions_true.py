from typing import List, Union


def factorial(n: int) -> Union[int, str]:
    if n == 0:
        return 1
    elif n < 0:
        return "Input should be non-negative"
    else:
        return n * factorial(n - 1)


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def fibonacci(n: int) -> Union[List[int], str]:
    if n <= 0:
        return "Input should be positive"
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_list = [0, 1]
        while len(fib_list) < n:
            fib_list.append(fib_list[-1] + fib_list[-2])
        return fib_list


# Test the functions
print(factorial(5))  # Output: 120
print(is_prime(7))  # Output: True
print(fibonacci(5))  # Output: [0, 1, 1, 2, 3]
