import math
from sympy.ntheory.factor_ import totient

def isPrime(num: int): 
    # Corner case 
    if num <= 1 : 
        return False

    # check from 2 to n-1 
    for i in range(2, num): 
        if num % i == 0: 
            return False

    return True
# b = bound
def generatePrimes(b):
    primes = []
    for num in range(0, b):
        if isPrime(num):
            primes.append(num)
    return primes

# Function to calculate Euler's totient function φ(n)
def euler_phi(p, q):
    return (p - 1) * (q - 1)

# Function to find the order of an element 'a' in Z_n
def findOrder(a, p, q):
    n = p * q
    phi_n = euler_phi(p, q)

    # Iterate through divisors of φ(n)
    for d in range(1, phi_n + 1):
        # Check if a^(φ(n)/d) ≡ 1 (mod n)
        if pow(a, phi_n // d, n) == 1:
            return phi_n // d

    # If no order is found, return -1 to indicate an error
    return -1

# get order in Z*_p
def getOrder(num, p): 
    order = totient(p) // math.gcd(p, num)
    return int(order)

def getOrderCorrect(num, p): 
    order = 0 
    
    curr = num 

    while curr != 1: 
        curr = (curr * num) % p
        order += 1
    return int(order)

def bitfield(num):
    return [int(digit) for digit in bin(num)[2:]]
    