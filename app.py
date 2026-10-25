import secrets
from flask_wtf.csrf import CSRFProtect
import io
import zipfile

from flask import send_file
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from werkzeug.utils import secure_filename
import os
import sqlite3
from pathlib import Path
from functools import wraps

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "users.db"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "webp"}
pending_downloads = {}


# Load the strong secret key from the environment
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY environment variable is missing")

# Enable CSRF protection
app.config["WTF_CSRF_ENABLED"] = True
csrf = CSRFProtect(app)




def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.")
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)
    return wrapped_view


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter both username and password.")
            return render_template("register.html")

        if len(username) > 50:
            flash("Username must be 50 characters or fewer.")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        try:
            with get_db() as connection:
                connection.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )
            flash("Registration successful. Please log in.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("That username is already registered.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        with get_db() as connection:
            user = connection.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session.get("username")
    )


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/encrypt", methods=["POST"])
@login_required
def encrypt_image():
    uploaded = request.files.get("image")

    if not uploaded or not uploaded.filename:
        flash("Please select an image.")
        return redirect(url_for("dashboard"))

    filename = secure_filename(uploaded.filename)

    if "." not in filename:
        flash("Invalid image filename.")
        return redirect(url_for("dashboard"))

    extension = filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        flash("Unsupported image format.")
        return redirect(url_for("dashboard"))

    image_data = uploaded.read()

    if not image_data:
        flash("The selected file is empty.")
        return redirect(url_for("dashboard"))

    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    encrypted_data = AESGCM(key).encrypt(
        nonce, image_data, None
    )

    token = secrets.token_urlsafe(32)

    pending_downloads[token] = {
        "encrypted": nonce + encrypted_data,
        "key": key,
        "filename": filename.rsplit(".", 1)[0] + ".enc",
        "key_downloaded": False
    }

    return render_template(
        "download_result.html",
        token=token
    )


@app.route("/download-encrypted/<token>")
@login_required
def download_encrypted(token):
    item = pending_downloads.get(token)

    if item is None:
        flash("Download expired. Please encrypt the image again.")
        return redirect(url_for("dashboard"))

    return send_file(
        io.BytesIO(item["encrypted"]),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name=item["filename"]
    )


@app.route("/download-key/<token>")
@login_required
def download_key(token):
    item = pending_downloads.get(token)

    if item is None or item["key_downloaded"]:
        flash("Key unavailable. Please encrypt the image again.")
        return redirect(url_for("dashboard"))

    item["key_downloaded"] = True

    return send_file(
        io.BytesIO(item["key"]),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name="image_key.key"
    )




@app.route("/decrypt", methods=["POST"])
@login_required
def decrypt_image():
    encrypted_upload = request.files.get("encrypted_file")
    key_upload = request.files.get("key_file")

    if (
        not encrypted_upload or not encrypted_upload.filename
        or not key_upload or not key_upload.filename
    ):
        flash("Select both the encrypted file and its key.")
        return redirect(url_for("dashboard"))

    encrypted_data = encrypted_upload.read()
    key = key_upload.read()

    if len(key) != 32 or len(encrypted_data) < 28:
        flash("Invalid key or encrypted file.")
        return redirect(url_for("dashboard"))

    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    try:
        decrypted_data = AESGCM(key).decrypt(
            nonce, ciphertext, None
        )
    except Exception:
        flash("Decryption failed. Check the key and encrypted file.")
        return redirect(url_for("dashboard"))

    # Identify the decrypted image format.
    if decrypted_data.startswith(b"\x89PNG\r\n\x1a\n"):
        extension = ".png"
        mimetype = "image/png"
    elif decrypted_data.startswith(b"\xff\xd8\xff"):
        extension = ".jpg"
        mimetype = "image/jpeg"
    elif decrypted_data.startswith(b"BM"):
        extension = ".bmp"
        mimetype = "image/bmp"
    elif (
        decrypted_data.startswith(b"RIFF")
        and decrypted_data[8:12] == b"WEBP"
    ):
        extension = ".webp"
        mimetype = "image/webp"
    else:
        flash("Unsupported image format.")
        return redirect(url_for("dashboard"))

    output = io.BytesIO(decrypted_data)
    output.seek(0)

    return send_file(
        output,
        mimetype=mimetype,
        as_attachment=True,
        download_name="decrypted_image" + extension
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)