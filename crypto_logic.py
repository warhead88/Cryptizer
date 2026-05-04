import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

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
    # Генерируем 64 байта (512 бит) случайных данных
    # Для AES-256 нам нужно 32 байта, но мы будем хранить 64-битный "мастер-ключ"
    # и брать из него энтропию для максимальной надежности.
    raw_key = os.urandom(64)
    return base64.urlsafe_b64encode(raw_key)

def get_cipher():
    key_b64 = load_key()
    if not key_b64:
        return None
    try:
        # Декодируем 512-битный ключ
        raw_key = base64.urlsafe_b64decode(key_b64)
        # Берем первые 32 байта (256 бит) для AES-256-GCM
        aes_key = raw_key[:32]
        return AESGCM(aes_key)
    except Exception:
        return None

def encrypt_message(cipher, text):
    if not cipher or not text:
        return None
    try:
        # Генерируем случайный 96-битный nonce (рекомендовано для GCM)
        nonce = os.urandom(12)
        encrypted_data = cipher.encrypt(nonce, text.encode(), None)
        # Возвращаем nonce + зашифрованные данные в base64
        return base64.urlsafe_b64encode(nonce + encrypted_data).decode()
    except Exception:
        return None

def decrypt_message(cipher, encrypted_text_b64):
    if not cipher or not encrypted_text_b64:
        return None
    try:
        data = base64.urlsafe_b64decode(encrypted_text_b64.encode())
        # Первые 12 байт - это nonce
        nonce = data[:12]
        ciphertext = data[12:]
        decrypted_data = cipher.decrypt(nonce, ciphertext, None)
        return decrypted_data.decode()
    except Exception:
        return None

def validate_key_format(key_string):
    try:
        decoded = base64.urlsafe_b64decode(key_string.encode())
        # Проверяем, что в ключе достаточно байт (минимум 32 для AES-256)
        return len(decoded) >= 32
    except Exception:
        return False
