import base64
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


BASE_DIR = Path(__file__).resolve().parent.parent
PRIVATE_KEY_PATH = BASE_DIR / "student_private.pem"


def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )
    return private_key
def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP-SHA256.

    Args:
        encrypted_seed_b64: Base64-encoded ciphertext
        private_key: RSA private key object

    Returns:
        Decrypted hex seed (64-character lowercase hex string)
    """
    # 1. Base64 decode the encrypted seed
    try:
        ciphertext = base64.b64decode(encrypted_seed_b64)
    except Exception as e:
        raise ValueError(f"Invalid base64 for encrypted seed: {e}")

    # 2. RSA/OAEP decrypt with SHA-256, MGF1(SHA-256), label=None
    try:
        plaintext_bytes = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        # This usually means wrong key or parameters
        raise ValueError(f"RSA decryption failed: {e}")

    # 3. Decode bytes to UTF-8 string
    try:
        hex_seed = plaintext_bytes.decode("utf-8").strip()
    except Exception as e:
        raise ValueError(f"Decrypted bytes are not valid UTF-8: {e}")

    # 4. Validate: must be 64-character hex string
    if len(hex_seed) != 64:
        raise ValueError(f"Decrypted seed length is {len(hex_seed)}, expected 64")

    allowed = set("0123456789abcdef")
    if any(ch not in allowed for ch in hex_seed):
        raise ValueError("Decrypted seed contains non-hex characters")

    # 5. Return hex seed
    return hex_seed
def decrypt_seed_with_loaded_key(encrypted_seed_b64: str) -> str:
    """
    Helper that loads the private key and decrypts the seed.
    """
    private_key = load_private_key()
    return decrypt_seed(encrypted_seed_b64, private_key)
