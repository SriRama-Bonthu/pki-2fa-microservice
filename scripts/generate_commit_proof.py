import sys
from pathlib import Path

# Add project root to PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))


import base64
import subprocess

from app.crypto_utils import sign_message, encrypt_with_instructor_public_key


def get_latest_commit_hash() -> str:
    """
    Get the latest git commit hash (40-character hex string).
    """
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def main():
    # 1. Get current commit hash
    commit_hash = get_latest_commit_hash()
    print("Commit Hash:", commit_hash)

    # 2. Sign commit hash with student private key (RSA-PSS-SHA256)
    signature = sign_message(commit_hash)

    # 3. Encrypt signature with instructor public key (RSA/OAEP-SHA256)
    encrypted_sig = encrypt_with_instructor_public_key(signature)

    # 4. Base64 encode encrypted signature (single line)
    b64 = base64.b64encode(encrypted_sig).decode("utf-8")

    print("Encrypted Signature (Base64):")
    print(b64)


if __name__ == "__main__":
    main()
