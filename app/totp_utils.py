import base64
import time
import pyotp


def hex_to_base32_seed(hex_seed: str) -> str:
    """
    Convert 64-char hex seed to a base32 string for TOTP.
    """
    hex_seed = hex_seed.strip()
    if len(hex_seed) != 64:
        raise ValueError(f"Expected 64-char hex seed, got {len(hex_seed)} chars")

    try:
        seed_bytes = bytes.fromhex(hex_seed)
    except ValueError as e:
        raise ValueError(f"Invalid hex seed: {e}")

    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")
    return base32_seed


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed.

    Returns:
        6-digit TOTP code as string.
    """
    base32_seed = hex_to_base32_seed(hex_seed)
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6)  # SHA-1 default
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with ±valid_window periods.
    """
    base32_seed = hex_to_base32_seed(hex_seed)
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6)
    return totp.verify(code, valid_window=valid_window)


def get_seconds_remaining(period: int = 30) -> int:
    """
    Get seconds remaining in the current TOTP period.
    """
    now = int(time.time())
    return period - (now % period)
