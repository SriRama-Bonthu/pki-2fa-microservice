from pathlib import Path
import base64
import binascii

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature


# =========================
# Key File Paths
# =========================

# Base directory = project root (pki-2fa-microservice)
BASE_DIR = Path(__file__).resolve().parent.parent

STUDENT_PRIVATE_KEY_PATH = BASE_DIR / "student_private.pem"
STUDENT_PUBLIC_KEY_PATH = BASE_DIR / "student_public.pem"
INSTRUCTOR_PUBLIC_KEY_PATH = BASE_DIR / "instructor_public.pem"


# =========================
# Key Loaders
# =========================

def load_student_private_key():
    """
    Load the student's RSA private key from student_private.pem
    """
    with open(STUDENT_PRIVATE_KEY_PATH, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
        )
    return private_key


def load_student_public_key():
    """
    Load the student's RSA public key from student_public.pem
    """
    with open(STUDENT_PUBLIC_KEY_PATH, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key


def load_instructor_public_key():
    """
    Load the instructor's RSA public key from instructor_public.pem
    """
    with open(INSTRUCTOR_PUBLIC_KEY_PATH, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key


# =========================
# Seed Decryption (RSA/OAEP)
# =========================

def decrypt_seed(encrypted_seed_b64: str) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP with SHA-256

    Returns:
        64-character hexadecimal seed string
    """
    try:
        private_key = load_student_private_key()

        # 1. Base64 decode
        encrypted_bytes = base64.b64decode(encrypted_seed_b64)

        # 2. RSA/OAEP-SHA256 decryption
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # 3. Decode to string
        hex_seed = decrypted_bytes.decode("utf-8").strip()

        # 4. Validate: 64-character hex string
        if len(hex_seed) != 64:
            raise ValueError("Invalid seed length")

        try:
            binascii.unhexlify(hex_seed)
        except Exception:
            raise ValueError("Seed is not valid hex")

        return hex_seed

    except Exception as e:
        raise RuntimeError("Decryption failed") from e


# =========================
# Commit Proof: SIGN
# RSA-PSS with SHA-256
# =========================

def sign_message(message: str) -> bytes:
    """
    Sign a message using RSA-PSS with SHA-256.

    CRITICAL:
    - Message must be ASCII/UTF-8 string
    - Do NOT sign binary hex bytes
    """
    private_key = load_student_private_key()

    # Sign ASCII string, NOT bytes.fromhex
    message_bytes = message.encode("utf-8")

    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


# =========================
# Commit Proof: ENCRYPT
# RSA-OAEP with SHA-256
# =========================

def encrypt_with_instructor_public_key(data: bytes) -> bytes:
    """
    Encrypt data using instructor public key with RSA/OAEP-SHA256
    """
    public_key = load_instructor_public_key()

    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext
