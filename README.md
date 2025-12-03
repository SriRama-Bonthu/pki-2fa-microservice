This project implements a secure, containerized Two-Factor Authentication (2FA) microservice using Public Key Infrastructure (PKI) and Time-based One-Time Passwords (TOTP).
It demonstrates enterprise-grade security practices including:
RSA 4096-bit encryption
RSA-PSS digital signatures
TOTP-based authentication
Secure persistent storage using Docker volumes
Automated 2FA logging using Cron jobs
Multi-stage Docker builds

This system securely decrypts a deterministic seed, generates time-based one-time passwords, verifies user codes with tolerance, and logs 2FA codes every minute using a scheduled Cron task.

🎯 Objectives
Implement RSA/OAEP decryption using SHA-256
Generate and verify TOTP codes using SHA-1
Build secure REST API endpoints using FastAPI
Automate 2FA logging with Cron in Docker
Ensure data persistence across container restarts using volumes
Use multi-stage Docker builds for optimized container images
Generate cryptographic proof of work using RSA-PSS signatures

🔑 Cryptographic Features
RSA Key Size: 4096 bits
Public Exponent: 65537
Decryption: RSA/OAEP with SHA-256
Signature: RSA-PSS with SHA-256
TOTP Algorithm: SHA-1
TOTP Period: 30 seconds
TOTP Digits: 6
Verification Tolerance: ±30 seconds (±1 period)


🗂️ Project Structure
pki-2fa-microservice/
│
├── app/
│   ├── main.py
│   ├── crypto_utils.py
│   └── totp_utils.py
│
├── scripts/
│   ├── log_2fa_cron.py
│   └── generate_commit_proof.py
│
├── cron/
│   └── 2fa-cron
│
├── student_private.pem
├── student_public.pem
├── instructor_public.pem
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── .gitattributes
└── README.md

🔒 Security Notes
All private keys in this repository are for academic use only
Keys are public for evaluation purposes
Do NOT reuse these keys for real production systems
Encrypted seed is never committed to GitHub
