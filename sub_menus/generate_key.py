from Crypto.PublicKey import RSA

def generate_rsa_keypair(key_size=2048):
    """
    Generate an RSA key pair.

    Args:
        key_size (int): The size of the RSA key in bits. Default is 2048 bits.

    Returns:
        tuple: A tuple containing the public key and private key objects.
    """
    key = RSA.generate(key_size)
    public_key = key.publickey().export_key()
    private_key = key.export_key()
    return public_key, private_key

if __name__ == "__main__":
    # Example usage:
    public_key, private_key = generate_rsa_keypair()
    print("Public Key:")
    print(public_key.decode())
    print("\nPrivate Key:")
    print(private_key.decode())