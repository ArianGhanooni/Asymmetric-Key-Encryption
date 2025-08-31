#Math
def gcd(a, b):
    # Computes the Greatest Common Divisor (GCD) of two numbers using the Euclidean algorithm.

    while a != 0:
        a , b = b % a , a
    return b

def findModInverse(a, m):
    # Finds the modular inverse of a relative to m using the Extended Euclidean Algorithm.
    # Returns x such that (a * x) % m == 1.

    if gcd(a, m) != 1:
        return None
    
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

    return u1 % m