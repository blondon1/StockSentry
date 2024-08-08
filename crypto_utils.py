# crypto_utils.py

from cryptography.fernet import Fernet
import json
import os

def generate_key():
    return Fernet.generate_key()

def load_key():
    return open("secret.key", "rb").read()

def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

def save_config(data, key):
    encrypted_data = encrypt_data(json.dumps(data), key)
    with open("config.enc", "wb") as config_file:
        config_file.write(encrypted_data)

def load_config(key):
    with open("config.enc", "rb") as config_file:
        encrypted_data = config_file.read()
    decrypted_data = decrypt_data(encrypted_data, key)
    return json.loads(decrypted_data)
