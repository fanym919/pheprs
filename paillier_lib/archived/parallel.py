import phe.paillier as paillier
from concurrent.futures import ProcessPoolExecutor

PARALLEL = False

class Encrypt(object):
    def __init__(self, array, public_key, encrypted = False):
        self.public_key = public_key
        if (encrypted):
            self.cipher = array
        else:
            if (PARALLEL):
                with ProcessPoolExecutor() as executor:
                    cipher = list(executor.map(self.public_key.encrypt, array))
            else:
                cipher = [self.public_key.encrypt(a) for a in array]
            self.cipher = cipher

    def decrypt(self, private_key):
        if (PARALLEL):
            with ProcessPoolExecutor() as executor:
                plaintext = list(executor.map(private_key.decrypt, self.cipher))
        else:
            plaintext = [private_key.decrypt(c) for c in self.cipher]
        return plaintext
    
    def __add__(self, other):
        if (len(self.cipher) != len(other.cipher)):
            raise Exception
        
        addlist = [self.cipher[i] + other.cipher[i] for i in range(len(self.cipher))]
        return Encrypt(addlist, self.public_key, True)
        
        # if (True):
        #     def add_elements(index):
        #         return self.cipher[index] + other.cipher[index]

        #     addlist = [None] * len(self.cipher)

        #     with ProcessPoolExecutor() as executor:
        #         futures = [executor.submit(add_elements, i) for i in range(len(self.cipher))]
        #         for i, future in enumerate(futures):
        #             addlist[i] = future.result()
        # else:
        #     addlist = [self.cipher[i] + other.cipher[i] for i in range(len(self.cipher))]

def demo():
    public_key, private_key = paillier.generate_paillier_keypair()

    import random
    import time

    t1 = time.time()
    m1 = [random.randint(0,100) - 50 + round(random.random(), 8) for _ in range(200)]
    m2 = [random.randint(0,100) - 50 + round(random.random(), 8) for _ in range(200)]

    c1 = Encrypt(m1, public_key)
    c2 = Encrypt(m2, public_key)

    c12 = c1 + c2

    m12 = c12.decrypt(private_key)

    print(time.time() - t1)

    # print(m12)
    # print([m1[i] + m2[i] for i in range(len(m1))])
    print(m12 == [m1[i] + m2[i] for i in range(len(m1))])

demo()