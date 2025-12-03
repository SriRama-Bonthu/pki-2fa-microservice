from pathlib import Path
from app.totp_utils import generate_totp_code, verify_totp_code, get_seconds_remaining

SEED_PATH = Path("seed_local.txt")  # just for testing, or use /data/seed.txt later

if __name__ == "__main__":
    hex_seed = SEED_PATH.read_text().strip()
    code = generate_totp_code(hex_seed)
    print("Code:", code)
    print("Valid for:", get_seconds_remaining(), "seconds")

    print("Verify correct code:", verify_totp_code(hex_seed, code))
    print("Verify wrong code (000000):", verify_totp_code(hex_seed, "000000"))
