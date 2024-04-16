import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class EncryptDecrypt:
    def __init__(self, is_initialized, public_key, private_key):
        self.is_initialized = is_initialized
        self.private_key = private_key
        self.public_key = public_key

    def encrypt(self, public_key_bytes, data):
        
        """
        Encrypt data using the RSA cryptosystem.

        Args:
            public_key (Crypto.PublicKey.RSA.RsaKey): The public key to use for encryption.
            data (str): The data to encrypt.

        Returns:
            str: The encrypted data.
        """
        # Create a cipher object using the public key
        cipher = PKCS1_OAEP.new(public_key_bytes)

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
        public_key_bytes = RSA.import_key(public_key)

        #empty encrypted file
        open(f'{file_path}.enc', 'w').close()

        # read the file by chunk size
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                # process the chunk of data here
                encrypted_chunk = self.encrypt(public_key_bytes, chunk)

                # write the encrypted chunk to a new file
                with open(f'{file_path}.enc', 'ab') as f_enc:
                    f_enc.write(encrypted_chunk)

        f.close()
        f_enc.close()

        return True
            

    def decrypt_file(self, file_path, chunk_size, private_key_bytes):
        # Import the private key
        print(private_key_bytes)
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
    
    
    def print_encrypt_decrypt_menus(self):
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Back to main menu")
        
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
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")