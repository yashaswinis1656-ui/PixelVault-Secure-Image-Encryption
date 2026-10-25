# 🔐 PixelVault – Secure Image Encryption

**PixelVault** is a Flask-based web application that protects images through encryption. It allows registered users to securely access the application, encrypt images, download encrypted image files and encryption keys, and decrypt images when needed.

## ✨ Features

- **User Authentication:** User registration, login, and logout.
- **Image Encryption:** Encrypt images using AES-256-GCM authenticated encryption.
- **Encrypted Image Download:** Download the encrypted image separately.
- **Encryption Key Download:** Download the key required for decryption.
- **Image Decryption:** Decrypt previously encrypted images using the correct key.
- **Secure Form Handling:** CSRF protection using Flask-WTF.
- **Database Integration:** SQLite database for user account information.
- **Simple Web Interface:** HTML, CSS, and JavaScript-based frontend.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML and CSS | User interface |
| JavaScript | Frontend functionality |
| SQLite | User data storage |
| Cryptography | Image encryption and decryption |
| AES-256-GCM | Authenticated encryption |
| Flask-WTF | CSRF protection |

## 📂 Project Structure

```text
SecureImageEncryption/
├── app.py
├── image_encryption.py
├── requirements.txt
├── .gitignore
├── users.db
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── register.html
    ├── login.html
    ├── dashboard.html
    └── download_result.html
```

**Note:** `users.db` is generated or maintained locally and should not be committed to GitHub.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/yashaswinis1656-ui/PixelVault-Secure-Image-Encryption.git
cd PixelVault-Secure-Image-Encryption
```

### 2. Create a virtual environment

For Windows:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.venv\Scripts\Activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the Flask secret key

The application requires a `SECRET_KEY` environment variable. Generate a secure value using:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Set the generated value in your current PowerShell