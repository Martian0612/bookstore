from cryptography.hazmat.primitives import serialization
import os
from dotenv import load_dotenv

def load_private_key():

    # Load the encrypted private key from the file
    with open('private_key.pem','rb') as f:
        encrypted_private_key_pem = f.read()

    # Password for decryption
    password_str = os.getenv("ENCRYPT_PASSWORD")
    password = password_str.encode('utf-8')

    private_key = serialization.load_pem_private_key(encrypted_private_key_pem,
                                                     password = password)
    
    return private_key

# if __name__ == '__main__':
#     private_keyy = load_private_key()
#     print(private_keyy)