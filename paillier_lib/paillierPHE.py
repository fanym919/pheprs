import pathlib

from paillier_lib.partialenc import *

# get current directory of this file
cwd = pathlib.Path(__file__).parent.resolve()

ENCRYPTED_DATA = {}
ENCRYPTED_CLIENT = ["/enc_weight_client1.txt",
                    "/enc_weight_client2.txt",
                    "/enc_weight_client3.txt",
                    "/enc_weight_client4.txt"]

KEYS = {"public_key" : None, "private_key" : None}

def generate_keys():
    KEYS["public_key"], KEYS["private_key"] = paillier.generate_paillier_keypair()

def encrypt_weights(weights, output_filename):
    """ This function will be used by clients to encrypt local model's weights and send its to server.
        - weights         : vector of model's weights (float numbers)
        - output_filename : store the output of encrypted_weights (as `Ciphertext<DCRTPoly>` object) to `output_filename`.
    """
    weights_div = [w / 4 for w in weights]
    ENCRYPTED_DATA[output_filename] = Encrypt(weights_div, KEYS["public_key"])

def decrypt_weights(cipher_file):
    """ This function will be used by clients to decrypt aggregated global model's weights.
        - cipher_file     : contain aggregated_weights compute using homomorphic operations by server
    """
    
    return ENCRYPTED_DATA[cipher_file].decrypt(KEYS["private_key"])

def aggregator():
    """ This function will be used by server to calculate aggregated global model's weights by applying
        homomorphic encryption to encrypted local model's weights of clients
    """
    total = ENCRYPTED_DATA[ENCRYPTED_CLIENT[0]]
    for client in ENCRYPTED_CLIENT[1:]:
        # total = [sum(x) for x in zip(total, ENCRYPTED_DATA[client])]
        total += ENCRYPTED_DATA[client]
    # total = [num / 4 for num in total]
    ENCRYPTED_DATA["/enc_aggregator_weight_server.txt"] = total

def demo():
    print("""
    /*
    Demo openFHE library: This is a simple python wrapper of openFHE library
    using CKKS scheme
    > link: https://github.com/openfheorg/openfhe-development/tree/main
    */
    """)
    print("=== This is demostration of calculating (w1 + w2 + w3)/3 using openFHE ===")
    w1 = [0.11231323, -4.112312394, 3.012444, -0.42341, 1.07234235, 1.123]
    w2 = [-2.323133, 7.134434, 0.010234, 13.052342342, 0.02405, -2.322]
    w3 = [-1.55135, -1.983334, 2.3234231, -8.424441, 0.033245, -3.33]
    w4 = [-1.1, 2.3, -2.2, 2.3, 0.03245, 3.33]
    n = len(w1)
    
    print("w1 = " + str(w1))
    print("w2 = " + str(w2))
    print("w3 = " + str(w3))
    print("w4 = " + str(w4))

    print("\n[+] Homo encryption by clients...")
    print("> Encrypt w1 -> ./data/enc_weight_client1.txt")
    encrypt_weights(w1, "/enc_weight_client1.txt")
    print("> Encrypt w2 -> ./data/enc_weight_client2.txt")
    encrypt_weights(w2, "/enc_weight_client2.txt")
    print("> Encrypt w3 -> ./data/enc_weight_client3.txt")  
    encrypt_weights(w3, "/enc_weight_client3.txt")
    print("> Encrypt w4 -> ./data/enc_weight_client4.txt")
    encrypt_weights(w4, "/enc_weight_client4.txt")
    
    print("\n[+] Homo add + mult by server...")
    print("> server calculate -> ./data/enc_aggregator_weight_server.txt")
    aggregator()

    print("\n[+] Homo decryption by clients...")

    print("\n[+] Compare final result: ")
    predict = [(a + b + c + d)/4 for a,b,c,d in zip(w1, w2, w3, w4)]
    print("> True value: " + str(predict))
    print("> Use homo: " + str(decrypt_weights("/enc_aggregator_weight_server.txt")[:n]))