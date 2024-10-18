from lightphe import LightPHE

algorithms = [
#   "Exponential-ElGamal",
  "Paillier",
#   "Damgard-Jurik",
#   "Okamoto-Uchiyama",
#   "Benaloh",
#   "Naccache-Stern",
#   "EllipticCurve-ElGamal"
]

class Encrypt(object):
    def __init__(self, array, param, encrypted = False):
        self.cs = param[0]
        self.move = param[2]
        if (encrypted):
            self.precision = param[1]
            self.cipher = array
        else:
            self.precision = 10 ** param[1]
            self.cipher = [self.cs.encrypt(int((a + self.move) * self.precision)) for a in array]

    def decrypt(self):
        plaintext = [self.cs.decrypt(c) / self.precision - self.move * 2 for c in self.cipher]
        return plaintext
    
    def __add__(self, other):
        if (len(self.cipher) != len(other.cipher)):
            raise Exception
        
        addlist = [self.cipher[i] + other.cipher[i] for i in range(len(self.cipher))]

        return Encrypt(addlist, (self.cs, self.precision, self.move), True)

def demo():
    cs = LightPHE(algorithm_name = algorithms[0])

    import random
    m1 = [random.randint(0,100) - 50 + round(random.random(), 8) for _ in range(10)]
    m2 = [random.randint(0,100) - 50 + round(random.random(), 8) for _ in range(10)]

    c1 = Encrypt(m1, (cs, 20, 100))
    c2 = Encrypt(m2, (cs, 20, 100))

    c12 = c1 + c2

    m12 = c12.decrypt()
    print(m12)
    print([m1[i] + m2[i] for i in range(len(m1))])

demo()