from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.crypto_utils import decrypt_seed_with_loaded_key
from app.totp_utils import generate_totp_code, verify_totp_code, get_seconds_remaining

app = FastAPI()

# IMPORTANT: For final Docker, this must be /data/seed.txt
SEED_PATH = Path("/data/seed.txt")


# ---------- Request Models ----------

class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str | None = None


# ---------- Endpoint 1: POST /decrypt-seed ----------

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(payload: DecryptRequest):
    """
    1) Accept base64-encoded encrypted seed
    2) Decrypt using student private key (RSA/OAEP-SHA256)
    3) Validate 64-char hex
    4) Save to /data/seed.txt
    5) Return {"status": "ok"} on success
    """
    try:
        # Decrypt and validate using helper from crypto_utils
        hex_seed = decrypt_seed_with_loaded_key(payload.encrypted_seed)

        # Ensure /data directory exists
        SEED_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Save seed persistently
        SEED_PATH.write_text(hex_seed)

        return {"status": "ok"}
    except Exception:
        # Return exactly what spec wants
        return JSONResponse(
            status_code=500,
            content={"error": "Decryption failed"},
        )


# ---------- Endpoint 2: GET /generate-2fa ----------

@app.get("/generate-2fa")
def generate_2fa():
    """
    1) Check if /data/seed.txt exists
    2) Read hex seed
    3) Generate TOTP code (SHA-1, 30s, 6 digits)
    4) Calculate remaining validity seconds
    5) Return {"code": "...", "valid_for": N}
    """
    if not SEED_PATH.exists():
        return JSONResponse(
            status_code=500,
            content={"error": "Seed not decrypted yet"},
        )

    try:
        hex_seed = SEED_PATH.read_text().strip()
        code = generate_totp_code(hex_seed)
        valid_for = get_seconds_remaining(30)

        return {"code": code, "valid_for": valid_for}
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to generate 2FA code"},
        )


# ---------- Endpoint 3: POST /verify-2fa ----------

@app.post("/verify-2fa")
def verify_2fa(payload: VerifyRequest):
    """
    1) Validate 'code' exists in request
    2) Ensure /data/seed.txt exists
    3) Verify TOTP with ±1 period (valid_window=1)
    4) Return {"valid": true/false}
    """
    # Missing code -> 400
    if payload.code is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing code"},
        )

    # Seed not decrypted -> 500
    if not SEED_PATH.exists():
        return JSONResponse(
            status_code=500,
            content={"error": "Seed not decrypted yet"},
        )

    try:
        hex_seed = SEED_PATH.read_text().strip()
        is_valid = verify_totp_code(hex_seed, payload.code, valid_window=1)
        return {"valid": is_valid}
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error": "Verification failed"},
        )


# Optional health check
@app.get("/health")
def health():
    return {"status": "ok"}
