import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key_from_password(password: str) -> bytes:
    """
    Generates a url-safe base64 encoded 32-byte key from a string password.
    Uses SHA256 hashing to convert any length password into exactly 32 bytes.
    """
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_message(message: str, password: str) -> str:
    """
    Encrypts a text message using Fernet symmetric encryption and the provided password.
    Returns the encrypted message as a string.
    """
    if not password:
        return message
        
    key = generate_key_from_password(password)
    f = Fernet(key)
    
    # Fernet encrypts bytes and returns bytes
    encrypted_bytes = f.encrypt(message.encode('utf-8'))
    
    # Return as string so our encoder can process it character by character
    return encrypted_bytes.decode('utf-8')

def decrypt_message(encrypted_message: str, password: str) -> str:
    """
    Decrypts an encrypted string message using the provided password.
    Returns the original text message.
    """
    if not password:
        return encrypted_message
        
    try:
        key = generate_key_from_password(password)
        f = Fernet(key)
        
        decrypted_bytes = f.decrypt(encrypted_message.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    except Exception:
        raise ValueError("Decryption failed. Incorrect password or the data is not encrypted.")
