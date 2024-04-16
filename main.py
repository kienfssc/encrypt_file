from sub_menus.bundle_action import BundleAction
import sub_menus.key_management as key_management
from sub_menus.encrypt_decrypt import EncryptDecrypt
from print_menu import print_welcome_message, print_menus, print_sign_verify_menus, print_about

KEY_MANAGEMENT_FOLDER = "./keys/"
new_key = key_management.KeyManagement()

def main():
    print_welcome_message()
    print_menus()

    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                new_key.menu_run()
                print_menus()
            elif choice == 2:
                encrypt_decrypt = EncryptDecrypt(new_key.is_initialized, new_key.public_key, new_key.private_key)
                encrypt_decrypt.menu_run()
                print_menus()
            elif choice == 3:
                bundle_action = BundleAction()
                print_menus()
            elif choice == 4:
                print_about()
                print_menus()
            elif choice == 5:
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()