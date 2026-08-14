# CyberVault — Secure Password Manager

CyberVault is a portfolio-focused Django password manager built around practical web-security controls. It encrypts secrets before database storage, analyzes password hygiene, detects password reuse with keyed fingerprints, and records security-relevant activity.

## Highlights

- Encrypted password and note storage with **Fernet authenticated encryption**
- Per-user object authorization — users cannot access another user's vault records
- **Security Center** with password score, entropy estimate, weak/reused/old credential detection
- Password reuse detection via **HMAC-SHA256 fingerprinting** (no plaintext comparison field)
- Cryptographically secure client-side password generator using `crypto.getRandomValues()`
- Audit log for login, logout, create, edit, delete, reveal and security-center events
- CSRF protection, HttpOnly cookies, CSP, clickjacking protection and restrictive browser permissions
- Responsive dark cybersecurity dashboard
- Automated security tests
- GitHub Actions CI + scheduled dependency vulnerability audit
- Dependabot configuration for Python and GitHub Actions dependencies

## Stack

Python · Django · SQLite · Cryptography/Fernet · HTML · CSS · JavaScript

## Quick start (Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Paste the generated key into `VAULT_ENCRYPTION_KEY` in `.env`, then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Run tests

```bash
python manage.py test
```

## Security design

CyberVault is intentionally designed to demonstrate multiple layers of application security. Django authentication and CSRF defenses protect the web layer; every credential query is constrained by the authenticated user; sensitive fields are encrypted before persistence; reuse detection stores only a keyed HMAC; and security events provide an audit trail.

For a real production password manager, additional controls would be required, including a dedicated secrets-management/KMS strategy, independent security review, stronger key derivation and key rotation, MFA, rate limiting, backup/recovery design and hardened deployment infrastructure.

See [`SECURITY.md`](SECURITY.md) and [`ARCHITECTURE.md`](ARCHITECTURE.md).

## Portfolio note

This project demonstrates secure CRUD design, authentication/authorization, cryptography integration, security telemetry, threat-aware password analysis and defensive HTTP configuration in Django.
