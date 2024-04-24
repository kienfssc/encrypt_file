import os

class BundleAction:
    def __init__(self):
        print("Bundle action is in development in next phase.")

    def run(self):
        print(f"Running action on bundle {self.bundle}")

    def list_all_file_in_folder(self, folder_path):
        files = []
        for file in os.listdir(folder_path):
            if file.endswith(".pem"):
                files.append(file)
        return files

    # def encrypt_folder(self, folder_path, chunk_size, public_key):
    #     files = self.list_all_file_in_folder(folder_path)
    #     for file in files:
    #         encrypt_file(file, chunk_size, public_key)

    # def decrypt_folder(self, folder_path, chunk_size, private_key):
    #     files = self.list_all_file_in_folder(folder_path)
    #     for file in files:
    #         decrypt_file(file, chunk_size, private_key)    

    def print_menu(self):
        print("Bundle Action Menu")
        print("1. Encrypt a full folder")
        print("2. Decrypt a full folder")
        print("3. Exit")
    