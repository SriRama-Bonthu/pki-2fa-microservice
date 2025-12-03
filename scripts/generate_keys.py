from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair(key_size: int = 4096):
    """
    Generate RSA key pair
    
    Returns:
        Tuple of (private_key, public_key) objects
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,   # REQUIRED
        key_size=key_size        # 4096 bits
    )

    public_key = private_key.public_key()
    return private_key, public_key


def save_keys_to_pem(private_key, public_key):
    # Save PRIVATE key
    with open("student_private.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,             # PEM format ✅
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Save PUBLIC key
    with open("student_public.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,              # PEM format ✅
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


if __name__ == "__main__":
    private_key, public_key = generate_rsa_keypair()
    save_keys_to_pem(private_key, public_key)
    print("✅ RSA 4096-bit key pair generated successfully!")
