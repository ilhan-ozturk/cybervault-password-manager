# Security Notes

## Controls implemented
- Fernet authenticated encryption for credential passwords and notes.
- HMAC-SHA256 password fingerprints for reuse detection.
- User-scoped database queries for object-level authorization.
- Django CSRF middleware and authentication framework.
- HttpOnly / SameSite cookies; Secure cookies and HSTS when debug is disabled.
- Content Security Policy, `X-Frame-Options: DENY`, MIME sniffing protection and restrictive Permissions Policy.
- Audit events that never include plaintext passwords.
- Password generation uses the browser CSPRNG (`crypto.getRandomValues`).

## Threat model (simplified)
CyberVault aims to reduce risk from accidental plaintext storage, basic cross-user IDOR attempts, weak/reused password hygiene, CSRF, clickjacking and insufficient activity visibility.

## Important limitations
This is a portfolio/educational application, not a replacement for a professionally audited password manager. A production design should use a managed KMS/HSM, formal key rotation, MFA, brute-force protection/rate limiting, secure backups, dependency scanning, monitoring, external penetration testing and a deployment-specific hardening review.

Never commit `.env`, `db.sqlite3`, real passwords, encryption keys or production secrets to GitHub.
