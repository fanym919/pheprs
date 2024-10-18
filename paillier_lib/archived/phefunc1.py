from lightphe import LightPHE

algorithms = [
#   "Exponential-ElGamal",
  "Paillier",
#   "Damgard-Jurik",
#   "Okamoto-Uchiyama",
#   "Naccache-Stern"
]

class Encrypt(object):
    def __init__(self, array, param):
        self.cs = param[0]
        self.move = param[1]
        if (isinstance(array, list)):
            self.cipher = self.cs.encrypt(array)
        else:
            self.cipher = array

    def decrypt(self):
        plaintext = self.cs.decrypt(self.cipher)
        return plaintext
    
    def __add__(self, other):
        return Encrypt(self.cipher + other.cipher, (self.cs, self.move))

def demo():
    cs = LightPHE(algorithm_name = algorithms[0], precision = 10)

    import random
    m1 = [random.randint(0,100) - 50 + round(random.random(), 10) for _ in range(5)]
    m2 = [random.randint(0,100) - 50 + round(random.random(), 10) for _ in range(5)]

    m1 = [12,-13,14,14]
    m2 = [12,-13,-15,-13]

    c1 = Encrypt(m1, (cs, 100))
    c2 = Encrypt(m2, (cs, 100))

    c12 = c1 + c2

    m12 = c12.decrypt()
    print(m1)
    print()
    print(m2)
    print()
    print([round(m, 10) for m in m12])
    print()
    print([round(m1[i] + m2[i], 10) for i in range(len(m1))])

    n=1446606821255940682692880354745380630433977042733187959218138137754294333873247180643573693083063985160471050083715762285976006592658745869913238926607332486402043881272937245159758201130376752793867173680815008068654166567627294646713446717975387368629954844280472444932483382648450872909063209676578630141
    print()
    print(int(m12[2]))
    print(n)

    # print(dir(cs.cs))
    # print(cs.cs.keys)
demo()