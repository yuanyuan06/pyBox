import random

from cryptography.hazmat.primitives.ciphers import algorithms

csprng = random.SystemRandom()
random.seed(b"ere")

aes = algorithms.AES(bytes(random.random(), 'utf-8'))
print(aes)
