import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
STUDENT_ID = "23A91A0578"  
GITHUB_REPO_URL = "https://github.com/SriRama-Bonthu/pki-2fa-microservice"  


def request_seed(student_id: str, github_repo_url: str, api_url: str):
    """
    Request encrypted seed from instructor API and save to encrypted_seed.txt
    """
    # 1. Read public key from PEM file
    with open("student_public.pem", "r") as f:
        public_key_pem = f.read()

    # 2. Prepare JSON payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_pem,
    }

    # 3. Send POST request
    try:
        resp = requests.post(api_url, json=payload, timeout=10)
    except Exception as e:
        raise SystemExit(f"Request failed: {e}")

    # 4. Check HTTP status
    if resp.status_code != 200:
        raise SystemExit(f"Non-200 response: {resp.status_code} {resp.text}")

    data = resp.json()
    if data.get("status") != "success":
        raise SystemExit(f"API returned error: {data}")

    encrypted_seed = data.get("encrypted_seed")
    if not encrypted_seed:
        raise SystemExit("No 'encrypted_seed' in response")

    # 5. Save encrypted seed to file
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    print("✅ Encrypted seed saved to encrypted_seed.txt")


if __name__ == "__main__":
    request_seed(STUDENT_ID, GITHUB_REPO_URL, API_URL)
