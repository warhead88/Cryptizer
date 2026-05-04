import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def load_key():
    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, "rb") as f:
                return f.read()
        except Exception:
            return None
    return None

def save_key(key):
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def delete_key():
    if os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)
        return True
    return False

def generate_key():
    return Fernet.generate_key()

def get_cipher():
    key = load_key()
    if not key:
        return None
    try:
        return Fernet(key)
    except Exception:
        return None

def encrypt_message(cipher, text):
    if not cipher or not text:
        return None
    return cipher.encrypt(text.encode()).decode()

def decrypt_message(cipher, encrypted_text):
    if not cipher or not encrypted_text:
        return None
    try:
        return cipher.decrypt(encrypted_text.encode()).decode()
    except Exception:
        return None

def validate_key_format(key_string):
    try:
        Fernet(key_string.encode())
        return True
    except Exception:
        return False
