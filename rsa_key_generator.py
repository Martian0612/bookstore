from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import os
from dotenv import load_dotenv
# Generate the RSA key pair
private_key = rsa.generate_private_key(
    public_exponent = 65537,
    key_size = 2048
)

# Password for encrypting the private key
password_str = os.getenv("ENCRYPT_PASSWORD")
password = password_str.encode('utf-8')

# Serialize the private key to PEM format with encryption
private_key_pem = private_key.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm= serialization.BestAvailableEncryption(password) 
)

# Extract the public key from the private key
public_key = private_key.public_key()

# Serialize the public key to PEM format
public_key_pem = public_key.public_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the private and public keys to files
with open('private_key.pem','wb') as f:
    f.write(private_key_pem)

with open('public_key.pem', 'wb') as f:
    f.write(public_key_pem)







