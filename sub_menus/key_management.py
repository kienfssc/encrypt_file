import time, os, pickle
from sub_menus.generate_key import generate_rsa_keypair
from Crypto.PublicKey import RSA

class KeyManagement:
    def __init__(self, key_management_folder = "./keys/"):
        self.is_initialized = False
        self.private_key = None
        self.public_key = None
        self.key_version = None
        self.key_management_folder = key_management_folder

    def generate_key(self):
        # warning if key pair is already initialized
        if self.is_initialized == True:
            print("Key pair is already initialized. Are you at risk of losing the current key pair?")
            x = input("Do you want to continue? (y/n): ")
            if x.lower() != 'y':
                return
        
        # generate a new key pair
        self.public_key, self.private_key = generate_rsa_keypair()
        self.is_initialized = True
        self.key_version = time.time()

    def save_key(self, key_name, folder_path):
        try:
            if self.is_initialized == False:
                print("Key pair is not initialized. Please generate a key pair first.")
                return
            # bundle the public and private key into a single file by pickle
            with open(os.path.join(folder_path, key_name + ".pem"), 'wb') as f:
                pickle.dump((self.public_key, self.private_key), f)
        except FileNotFoundError:
            print("Folder not found. Please create the folder first.")
        except Exception as e:
            print("An error occurred while saving the key pair.")
            print(e)
        

    def load_key(self, key_name, folder_path):
        try:
            if self.is_initialized == True:
                print("Key pair is already initialized. Are you at risk of losing the current key pair?")
                
                x = input("Do you want to continue? (y/n): ")
                if x.lower() != 'y':
                    return
            # load the public and private key from a single file by pickle
            with open(os.path.join(folder_path, key_name + ".pem"), 'rb') as f:
                self.public_key, self.private_key = pickle.load(f)
                self.is_initialized = True
                self.key_version = time.time()
        except FileNotFoundError:
            print("Key pair not found.")
        except Exception as e:
            print("An error occurred while loading the key pair.")
            print(e)

    def list_keys(self, folder_path):
        # find all file in folder ending with .pem
        files = []
        for file in os.listdir(folder_path):
            if file.endswith(".pem"):
                files.append(file)

        unique_files_array = []
        for file in files:
            if file not in unique_files_array:
                unique_files_array.append(file)

        return unique_files_array

    def print_key_info(self):
        print("Key Version:", self.key_version)

    def print_menu(self):
        print("Key Management Menu")
        print("1. Generate Key Pair")
        print("2. Save Key Pair")
        print("3. Load Key Pair")
        print("4. List Keys")
        print("5. Print Key Info")
        print("7. Share public")
        print("8. Import public")
        print("9. Exit")

    def menu_run(self):
        while True:
            try:
                self.print_menu()
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.generate_key()
                elif choice == 2:
                    key_pair_name = input("Enter the name of the key pair: ")
                    self.load_key(key_pair_name, self.key_management_folder)
                elif choice == 3:
                    key_pair_name = input("Enter the name of the key pair: ")
                    self.save_key(key_pair_name, self.key_management_folder)
                elif choice == 4:
                    self.print_key_info()
                elif choice == 5:
                    key_names = self.list_keys(self.key_management_folder)
                    print("Key pairs in management folder:")
                    for key_name in key_names:
                        print(key_name)

                elif choice == 7:
                    if self.is_initialized == False:
                        print("Key pair is not initialized. Please generate a key pair first.")
                        continue
                    print("Your current public key: ")
                    print(self.public_key.decode())
                elif choice == 8:
                    if (self.is_initialized == True):
                        print("Key pair is already initialized. Are you at risk of losing the current key pair?")
                        x = input("Do you want to continue? (y/n): ")
                        if x.lower() != 'y':
                            return
                        
                    print("Enter the public key to import: ")

                    lines = []
                    while True:
                        line = input()
                        if line:
                            lines.append(line)
                        else:
                            break
                    public_key = '\n'.join(lines)

                    # init public key as RSA object
                    public_key_bytes = RSA.import_key(public_key)

                    self.private_key = None
                    self.public_key = public_key_bytes
                    self.is_initialized = True
                    self.key_version = time.time()
                
                elif choice == 9:
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid choice. Please try again.")