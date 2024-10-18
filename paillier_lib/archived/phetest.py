import phe.paillier as paillier

public_key, private_key = paillier.generate_paillier_keypair()


x1 = 12.123
x2 = 13.324

c1 = public_key.encrypt(x1)
c2 = public_key.encrypt(x2)

c3 = c1 + c2

print(private_key.decrypt(c3))