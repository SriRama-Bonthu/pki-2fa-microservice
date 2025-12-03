from app.crypto_utils import load_private_key, decrypt_seed

if __name__ == "__main__":
    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()

    private_key = load_private_key()
    hex_seed = decrypt_seed(encrypted_seed_b64, private_key)

    with open("seed_local.txt", "w") as f:
        f.write(hex_seed)

    print("✅ Decrypted seed saved to seed_local.txt")
    print("Hex seed:", hex_seed)
    print("Length:", len(hex_seed))
