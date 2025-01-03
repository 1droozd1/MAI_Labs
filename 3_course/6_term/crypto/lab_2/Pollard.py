import math
import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    x = random.randint(1, n-1)
    y = x
    c = random.randint(1, n-1)
    d = 1
    while d == 1:
        x = (pow(x, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        d = gcd(abs(x-y), n)
        if d == n:
            return pollard_rho(n)
    return d

n1 = 108762353292448487441247663685513658893167646930627178946128889967643172154127
factor = pollard_rho(n1)
print(f"Один из сомножителей: {factor}")
print(f"Другой сомножитель: {n1 // factor}")
