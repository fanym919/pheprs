import phe.paillier as paillier

class Encrypt(object):
    def __init__(self, array, public_key, encrypted = False):
        self.public_key = public_key
        if (encrypted):
            self.cipher = array
        else:
            self.cipher = [self.public_key.encrypt(a) for a in array]

    def decrypt(self, private_key):
        plaintext = [private_key.decrypt(c) for c in self.cipher]
        return plaintext
    
    def __add__(self, other):
        if (len(self.cipher) != len(other.cipher)):
            raise Exception
        
        addlist = [self.cipher[i] + other.cipher[i] for i in range(len(self.cipher))]

        return Encrypt(addlist, self.public_key, True)

def demo():
    public_key, private_key = paillier.generate_paillier_keypair()

    import random
    m1 = [random.randint(0,100) - 50 + round(random.random(), 8) for _ in range(10)]
    m2 = [random.randint(0,100) - 50 + round(random.random(), 8) for _ in range(10)]

    c1 = Encrypt(m1, public_key)
    c2 = Encrypt(m2, public_key)

    c12 = c1 + c2

    m12 = c12.decrypt(private_key)
    print(m12)
    print([m1[i] + m2[i] for i in range(len(m1))])
    print(m12 == [m1[i] + m2[i] for i in range(len(m1))])

demo()