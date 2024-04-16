from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

def decode_file(file_path, chunk_size, key):
    """
    Decrypt a file using the RSA cryptosystem.

    Args:
        file_path (str): The path to the file to decrypt.
        chunk_size (int): The size of the chunks to read from the file. (bytes)
        key (Crypto.PublicKey.RSA.RsaKey): The private key to use for decryption.

    Returns:
        str: The decrypted content of the file.
    """

    # Create a cipher object using the private key
    cipher = PKCS1_OAEP.new(key)

    # Read the encrypted file
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    # Decrypt the file in chunks
    decrypted_data = b""
    for i in range(0, len(encrypted_data), chunk_size):
        chunk = encrypted_data[i:i + chunk_size]
        decrypted_chunk = cipher.decrypt(chunk)
        decrypted_data += decrypted_chunk

    return decrypted_data.decode()