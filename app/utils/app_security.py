from config import settings
from cryptography.fernet import Fernet


env = settings.get_settings()


def encrypt_text(text):
    key = env.APP_SECRET_KEY + "="
    fernet_key_bytes = key.encode()
    # Create a Fernet symmetric encryption cipher using the key
    cipher = Fernet(fernet_key_bytes)

    # Encrypt the message
    encrypted_text = cipher.encrypt(text.encode())

    return encrypted_text


def decrypt_message(encrypted_text):
    key = env.APP_SECRET_KEY + "="
    fernet_key_bytes = key.encode()
    # Create a Fernet symmetric encryption cipher using the key
    cipher = Fernet(fernet_key_bytes)

    # Decrypt the message
    decrypted_text = cipher.decrypt(encrypted_text).decode()
    return decrypted_text
