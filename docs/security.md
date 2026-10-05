# AgriShield Security Audit & Hardening Document

This document summarizes the security boundaries, validation mechanisms, threat mitigations, and compliance safeguards implemented in **AgriShield**.

---

## 1. Authentication & Access Control

- **Password Hashing**: User passwords are never stored in plain text. Passwords are hashed using standard `pbkdf2:sha256` via Werkzeug's `generate_password_hash` and verified with `check_password_hash`.
- **Session Management**: Session cookies are signed with Flask's `SECRET_KEY` (configured via environment variable with fallback for development).
- **Role-Based Access Control (RBAC)**:
  - `farmer`: Access to observation forms, history tracking, and quick scan.
  - `expert`: Access to Expert Review Dashboard, diagnostic input, and status escalation updates.
  - `procurement`: Access to batch lot evaluation and analytics.
  - `admin`: Full system oversight.

---

## 2. File Upload & Input Validation

- **Extension Whitelisting**: File uploads restrict accepted extensions strictly to `.jpg`, `.jpeg`, `.png`.
- **MIME & Content-Type Verification**: File headers are validated using Python `Pillow` image header inspection (`Image.open()`) to prevent arbitrary file execution (e.g., polyglot scripts or `.php`/`.exe` disguised as images).
- **Filename Sanitization**: Uploaded files are renamed using `werkzeug.utils.secure_filename` combined with a UUID hash to prevent directory traversal attacks (`../`).
- **File Size Caps**: Upload payload size is enforced via `MAX_CONTENT_LENGTH = 16 * 1024 * 1024` (16 MB maximum per request).

---

## 3. SQL Injection & XSS Mitigations

- **ORM Parameterization**: All database queries are executed via SQLAlchemy standard parameter binding. No dynamic SQL string concatenation is used.
- **HTML Escaping**: Jinja2 automatic contextual HTML escaping is enabled by default across all templates to prevent Cross-Site Scripting (XSS).
- **Input Sanitization**: Free-text form inputs (e.g. `notes`, `farmer_name`) are stripped of script tags and unsafe HTML entities.

---

## 4. Error Handling & Information Leakage

- **Custom Error Handlers**: Custom application handlers for HTTP 404 (`Not Found`) and HTTP 500 (`Internal Server Error`) prevent stack traces, database schema details, or environment variables from leaking to end users.
- **Production Debug Control**: Flask `DEBUG` mode is explicitly toggled off in production deployments (`FLASK_ENV=production`).

---

## 5. Vulnerability Assessment & Compliance

| Security Dimension | Defense Mechanism | Verification Status |
|---|---|---|
| User Credentials | Werkzeug PBKDF2 Hashing | PASSED (Unit tested) |
| SQL Injection | SQLAlchemy ORM Parameterization | PASSED (Zero raw queries) |
| Directory Traversal | `secure_filename()` + UUID | PASSED (Unit tested) |
| Unrestricted File Upload | Pillow Image verification + Extension whitelist | PASSED (Unit tested) |
| Error Traceback Leakage | Custom 404 / 500 Jinja error handlers | PASSED (Verified) |
| Data Integrity / Fake Evidence | Explicit `PENDING INDEPENDENT VALIDATION` tags | PASSED (Strict Rule Compliant) |
