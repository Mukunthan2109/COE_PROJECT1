# AgriShield Security & Data Protection Specification

## 1. Security Overview

AgriShield enforces student-level production-grade security practices across file handling, user authentication, role-based access control (RBAC), database interactions, and session management.

---

## 2. File Upload & Media Handling Safeguards

- **Extension Validation**: Standard whitelist strictly allowing `.jpg`, `.jpeg`, `.png`, and `.webp` extensions (`ALLOWED_EXTENSIONS`). Executable extensions (`.exe`, `.php`, `.py`, `.sh`, `.html`, `.js`) are immediately rejected.
- **Secure File Naming**: Every uploaded file is assigned a unique UUID prefix via Werkzeug `secure_filename()` to prevent directory traversal and path manipulation attacks.
- **File Size Restriction**: Enforced `MAX_CONTENT_LENGTH = 16 * 1024 * 1024` (16MB maximum per upload). Oversized files return HTTP 413 Payload Too Large.
- **MIME & Image Validation**: Python Pillow (`PIL.Image.open()`) verifies binary header integrity. Non-image or corrupted files fail validation and are safely discarded.
- **Zero Script Execution**: The runtime upload directory (`app/static/uploads/`) is designated purely for static media serving without server-side script execution capabilities.

---

## 3. User Authentication & Password Security

- **Password Hashing**: User passwords are never stored in plaintext. Passwords are hashed using Werkzeug PBKDF2 with SHA-256 (`werkzeug.security.generate_password_hash`).
- **Role-Based Access Control (RBAC)**: Custom Flask `@role_required('expert', 'qa_manager')` decorator restricts sensitive endpoints (`/expert`, `/expert/review/<id>`, `/analytics`) to authenticated, authorized users.
- **Session Protection**: Flask sessions are signed using a server-side secret key (`SECRET_KEY`). Production deployments draw secrets dynamically from environment variables.

---

## 4. SQL Injection & Cross-Site Scripting (XSS) Prevention

- **Parameterized Database Queries**: All database operations execute through SQLAlchemy ORM, which handles parameter binding and parameter sanitization to prevent SQL injection vulnerabilities.
- **Output Encoding & Template Escaping**: Jinja2 auto-escaping is active across all HTML templates to prevent Reflected and Stored XSS attacks.
- **Input Validation**: All form inputs (crop name, symptoms, growth stage, notes) undergo stripping and bounds checking before processing.

---

## 5. Privacy, Non-Surveillance & Non-Punitive Design

- **Zero Surveillance**: Continuous GPS tracking, device fingerprinting, and user location tracking are strictly excluded. Region data uses broad administrative zones (*e.g., North Zone, South Zone*).
- **Non-Punitive Data Policy**: Observation data is used exclusively for agricultural crop screening, disease outbreak warning, and expert escalation. Data is never used for automated purchasing rejection, farmer financial scoring, or punitive penalties.
