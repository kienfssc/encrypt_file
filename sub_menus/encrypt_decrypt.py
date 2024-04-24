import base64
import random
import string
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from concurrent.futures import ThreadPoolExecutor
import os

class EncryptDecrypt:
    def __init__(self, is_initialized, public_key, private_key):
        self.is_initialized = is_initialized
        self.private_key = private_key
        self.public_key = public_key
        self.cache_dir = "./temp/"

    def encrypt(self, cipher, data):
        
        """
        Encrypt data using the RSA cryptosystem.

        Args:
            public_key (Crypto.PublicKey.RSA.RsaKey): The public key to use for encryption.
            data (str): The data to encrypt.

        Returns:
            str: The encrypted data.
        """

        # Encrypt the data
        encrypted_data = cipher.encrypt(data)

        return encrypted_data

    def decrypt(self, private_key_bytes, encrypted_data):
        """
        Decrypt data using the RSA cryptosystem.

        Args:
            private_key (Crypto.PublicKey.RSA.RsaKey): The private key to use for decryption.
            encrypted_data (str): The encrypted data to decrypt.

        Returns:
            str: The decrypted data.
        """
        # Create a cipher object using the private key
        cipher = PKCS1_OAEP.new(private_key_bytes)

        # Decrypt the data
        decrypted_data = cipher.decrypt(encrypted_data)

        return decrypted_data

    def encrypt_file(self, file_path, chunk_size, public_key):
        if (self.is_initialized == False):
            print("Key pair is not initialized. Please generate or import a key pair first.")
            return
        
        public_key_bytes = RSA.import_key(public_key)

        # Create a cipher object using the public key
        cipher = PKCS1_OAEP.new(public_key_bytes)

        #empty encrypted file
        open(f'{file_path}.enc', 'w').close()

        # read the file by chunk size
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                # process the chunk of data here
                encrypted_chunk = self.encrypt(cipher, chunk)

                # write the encrypted chunk to a new file
                with open(f'{file_path}.enc', 'ab') as f_enc:
                    f_enc.write(encrypted_chunk)

        f.close()
        f_enc.close()

        return True
            

    def decrypt_file(self, file_path, chunk_size, private_key_bytes):
        if (self.is_initialized == False):
            print("Key pair is not initialized. Please generate or import a key pair first.")
            return
        
        # Import the private key
        private_key = RSA.import_key(private_key_bytes)

        # read the file by chunk size
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size * 2)
                if not chunk:
                    break
                # process the chunk of data here
                decrypted_chunk = self.decrypt(private_key, chunk)

                # write the decrypted chunk to a new file
                with open(f'{file_path}.dec', 'ab') as f_dec:
                    f_dec.write(decrypted_chunk)

        f.close()
        f_dec.close()

        return True
    
    def encrypt_chunk_to_cache(self, public_key_bytes, chunk, cache_dir, session, chunk_count):
        encrypted_chunk = self.encrypt(public_key_bytes, chunk)
        with open(f'{cache_dir}/{session}_{chunk_count}.temp', 'wb') as f_enc:
            f_enc.write(encrypted_chunk)
        f_enc.close()
    
    def encrypt_file_multiple_threads(self, file_path, chunk_size, public_key):
        if (self.is_initialized == False):
            print("Key pair is not initialized. Please generate or import a key pair first.")
            return
        
        public_key_bytes = RSA.import_key(public_key)

        # Create a cipher object using the public key
        cipher = PKCS1_OAEP.new(public_key_bytes)

        #empty encrypted file
        open(f'{file_path}.enc', 'w').close()

        # generate file session string random string with 6 characters and digits
        session_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # count chunk
        chunk_count = 0
        # read the file by chunk size
        with open(file_path, 'rb') as f:
            with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    chunk_count += 1
                    
                    executor.submit(self.encrypt_chunk_to_cache, cipher, chunk, self.cache_dir, session_string, chunk_count)
        f.close()

        # merge all encrypted chunks
        with open(f'{file_path}.enc', 'wb') as f_enc:
            for i in range(1, chunk_count + 1):
                with open(f'{self.cache_dir}/{session_string}_{i}.temp', 'rb') as f_enc_temp:
                    f_enc.write(f_enc_temp.read())
                
                # remove temp file
                f_enc_temp.close()
                os.remove(f'{self.cache_dir}/{session_string}_{i}.temp')
        f_enc.close()

        return True

    def encrypt_text(self, text, chunk_size, public_key):
        if (self.is_initialized == False):
            print("Key pair is not initialized. Please generate or import a key pair first.")
            return
        
        # split text by chunk size
        text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        public_key_bytes = RSA.import_key(public_key)
        
        # Create a cipher object using the public key
        cipher = PKCS1_OAEP.new(public_key_bytes)

        encrypted_text = []
        for chunk in text_chunks:
            encrypted_chunk = self.encrypt(cipher, chunk.encode())
            encrypted_text.append(base64.b64encode(encrypted_chunk).decode())

        return ".".join(encrypted_text)

    
    def decrypt_text(self, text, chunk_size, private_key):
        if (self.is_initialized == False):
            print("Key pair is not initialized. Please generate or import a key pair first.")
            return
        # split text by chunk size
        text_chunks = text.split(".")

        private_key_bytes = RSA.import_key(private_key)
        decrypted_text = ""
        for chunk in text_chunks:
            encrypted_chunk = base64.b64decode(chunk)
            decrypted_chunk = self.decrypt(private_key_bytes, encrypted_chunk)
            decrypted_text += decrypted_chunk.decode()

        return decrypted_text
    
    def print_encrypt_decrypt_menus(self):
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Encrypt text (one line only)")
        print("4. Decrypt text (one line only)")
        print("5. Encrypt file using multiple threads")
        print("7. Back to main menu")
        
    def menu_run(self):
        self.print_encrypt_decrypt_menus()
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    file_path = input("Enter the file path to encrypt: ")
                    chunk_size = int(input("Enter the chunk size: "))
                    self.encrypt_file(file_path, chunk_size, self.public_key)
                    print("File encrypted successfully.")
                elif choice == 2:
                    file_path = input("Enter the file path to decrypt: ")
                    chunk_size = int(input("Enter the chunk size: "))
                    self.decrypt_file(file_path, chunk_size, self.private_key)
                    print("File decrypted successfully.")
                elif choice == 3:
                    text = input("Enter the text to encrypt: ")
                    chunk_size = int(input("Enter the chunk size: "))
                    encrypted_text = self.encrypt_text(text, chunk_size, self.public_key)
                    print(f"Encrypted text: {encrypted_text}")
                elif choice == 4:
                    text = input("Enter the text to decrypt: ")
                    chunk_size = int(input("Enter the chunk size: "))
                    decrypted_text = self.decrypt_text(text, chunk_size, self.private_key)
                    print(f"Decrypted text: {decrypted_text}")
                elif choice == 5:
                    file_path = input("Enter the file path to encrypt: ")
                    chunk_size = int(input("Enter the chunk size: "))
                    self.encrypt_file_multiple_threads(file_path, chunk_size, self.public_key)
                    print("File encrypted successfully.")
                elif choice == 7:
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")