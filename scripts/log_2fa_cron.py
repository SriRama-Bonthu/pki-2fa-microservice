#!/usr/bin/env python3

import sys
from datetime import datetime, timezone
from pathlib import Path

from app.totp_utils import generate_totp_code

# In the container, the seed is stored here (volume mount)
SEED_PATH = Path("/data/seed.txt")


def main():
    try:
        # 1. Read hex seed from persistent storage
        if not SEED_PATH.exists():
            print("Seed file not found; decrypt-seed not called yet.", file=sys.stderr)
            return

        hex_seed = SEED_PATH.read_text().strip()

        # 2. Generate current TOTP code
        code = generate_totp_code(hex_seed)

        # 3. Get current UTC timestamp
        now = datetime.now(timezone.utc)
        ts = now.strftime("%Y-%m-%d %H:%M:%S")

        # 4. Output formatted line to stdout
        #    cron will append this to /cron/last_code.txt
        print(f"{ts} - 2FA Code: {code}")
    except Exception as e:
        print(f"Error in cron script: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
