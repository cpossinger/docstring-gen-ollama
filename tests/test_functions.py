from typing import List, Union


def factorial(n: int) -> Union[int, str]:
    """
    Calculates the factorial of a given integer.

    Args:
      n (int): The input integer. Must be non-negative.

    Returns:
      Union[int, str]: The factorial result if `n` is non-negative, otherwise an error message.

    Raises:
      None

    Example:
      >>> factorial(5)
      120
    """
    if n == 0:
        return 1
    elif n < 0:
        return "Input should be non-negative"
    else:
        return n * factorial(n - 1)


def is_prime(n: int) -> bool:
    """
    Returns whether the given integer `n` is prime.
    If `n` is less than or equal to 1, returns `False`.
    Otherwise, checks if `n` has any divisors between 2 and the square root of `n`, inclusive. If it does, returns `False`. Otherwise, returns `True`.

    Args:
        n: int
            The integer to check for primality.

    Returns:
        bool
            Whether `n` is prime.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def fibonacci(n: int) -> Union[List[int], str]:
    """
    Returns the Fibonacci sequence up to the nth term.
    If n is less than or equal to 0, returns "Input should be positive".
    If n is 1, returns [0].
    If n is 2, returns [0, 1].
    Otherwise, generates the Fibonacci sequence up to the nth term and returns it as a list of integers.

    Args:
        n: The number of terms in the Fibonacci sequence to return. Must be a positive integer.

    Returns:
        A list of integers representing the Fibonacci sequence up to the nth term, or "Input should be positive" if n is less than or equal to 0.
    """
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
