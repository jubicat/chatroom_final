import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_key_pair(p, q):
    # n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private key_pair
    # Public key is (e, n) and private key is (d, n)
    public=str(e)+":"+str(n)
    private=str(d)+":"+str(n)
    return (public,private)


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key = int(pk.split(":")[0])
    n = int(pk.split(":")[1])
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [pow(char, key, n) for char in plaintext]
    # Return the array of bytes
    newcipher=''
    for i in cipher:
        newcipher+=str(i)+':'
    return newcipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key = int(pk.split(":")[0])
    n = int(pk.split(":")[1])
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    newcipher = ciphertext.split(":")
    arr = newcipher[0:-1]
    aux = [pow(int(char), key, n) for char in arr]
    # Return the array of bytes as a string
    plain = [chr(char2) for char2 in aux]
    return ''.join(plain)


