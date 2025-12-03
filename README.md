# 🔐 PKI-Based 2FA Microservice

This project is a secure, containerized **Two-Factor Authentication (2FA) microservice** built using **Public Key Infrastructure (PKI)** and **Time-based One-Time Passwords (TOTP)**.  
It demonstrates how encrypted data can be securely decrypted and used for real-time 2FA generation and verification.

The system decrypts a deterministic encrypted seed, generates time-based OTPs, verifies user codes with tolerance, and logs 2FA codes automatically every minute using a Cron job.

---

## 🎯 Objectives

- Implement RSA/OAEP decryption using SHA-256  
- Generate and verify TOTP codes using SHA-1  
- Build secure REST API endpoints using FastAPI  
- Automate 2FA logging using Cron in Docker  
- Ensure data persistence using Docker volumes  
- Use multi-stage Docker builds for optimized container images  
- Generate cryptographic proof using RSA-PSS signatures  

---

## 🔑 Cryptographic Features

- **RSA Key Size:** 4096 bits  
- **Public Exponent:** 65537  
- **Decryption:** RSA/OAEP with SHA-256  
- **Signature:** RSA-PSS with SHA-256  
- **TOTP Algorithm:** SHA-1  
- **TOTP Period:** 30 seconds  
- **TOTP Digits:** 6  
- **Verification Tolerance:** ±30 seconds  

---
---

## 🔒 Security Notes

- All cryptographic keys in this repository are generated **only for academic evaluation**
- Keys are **public for verification purposes**
- Do **NOT** reuse these keys for real production systems
- The encrypted seed is **never committed** to GitHub

---
