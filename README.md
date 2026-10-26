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


## How to Run the Application

Follow these steps to run PixelVault on your local computer.

### 1. Clone the Repository

Open a terminal or Command Prompt and run:

```bash
git clone https://github.com/yashaswinis1656-ui/PixelVault-Secure-Image-Encryption.git
```

### 2. Navigate to the Project Folder

```bash
cd PixelVault-Secure-Image-Encryption
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows (Command Prompt):**

```bat
.venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure the Flask Secret Key

The application requires a `SECRET_KEY` environment variable.

**Windows (Command Prompt):**

```bat
set SECRET_KEY=replace-with-a-long-random-secret
```

**Windows (PowerShell):**

```powershell
$env:SECRET_KEY = "replace-with-a-long-random-secret"
```

For local testing, use a long, randomly generated secret. Do not commit real secret keys to GitHub.

### 7. Run the Application

```bash
python app.py
```

If the application starts successfully, Flask will display a local address in the terminal, commonly:

```text
http://127.0.0.1:5000
```

Open that address in your web browser to use PixelVault.

### 8. Stop the Application

Return to the terminal and press:

```text
Ctrl + C
```

### Troubleshooting

- If Python is not recognized, install Python and ensure it is available in your system PATH.
- If a dependency is missing, activate the virtual environment and run `python -m pip install -r requirements.txt` again.
- If the application reports that `SECRET_KEY` is missing, configure the environment variable in the same terminal before starting Flask.
- Keep your encryption keys safe. Losing the required key may prevent recovery of the original image.

