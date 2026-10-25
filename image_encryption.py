
from pathlib import Path
import os
from tkinter import Tk, filedialog, messagebox
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_image():
    root = Tk()
    root.withdraw()

    image_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp")]
    )

    if not image_path:
        root.destroy()
        return

    try:
        image_data = Path(image_path).read_bytes()

        # Generate a secure 256-bit AES key
        key = AESGCM.generate_key(bit_length=256)

        # Generate a unique 12-byte nonce
        nonce = os.urandom(12)

        # Encrypt and authenticate the image data
        aes = AESGCM(key)
        encrypted_data = aes.encrypt(nonce, image_data, None)

        output_path = filedialog.asksaveasfilename(
            title="Save encrypted image",
            defaultextension=".enc",
            initialfile=Path(image_path).name + ".enc"
        )

        if not output_path:
            root.destroy()
            return

        # Store the nonce before the encrypted data
        Path(output_path).write_bytes(nonce + encrypted_data)

        key_path = filedialog.asksaveasfilename(
            title="Save the secret key",
            defaultextension=".key",
            initialfile="image_secret.key"
        )

        if not key_path:
            messagebox.showwarning(
                "Key not saved",
                "Encrypted file saved, but the key was not saved. "
                "The image cannot be recovered without the key."
            )
            root.destroy()
            return

        Path(key_path).write_bytes(key)

        messagebox.showinfo(
            "Success",
            "Image encrypted successfully!\n\n"
            f"Encrypted file: {output_path}\n"
            f"Secret key: {key_path}\n\n"
            "Keep your key safe."
        )

    except Exception as error:
        messagebox.showerror("Error", str(error))

    finally:
        root.destroy()


def decrypt_image():
    root = Tk()
    root.withdraw()

    encrypted_path = filedialog.askopenfilename(
        title="Select encrypted file",
        filetypes=[("Encrypted files", "*.enc")]
    )

    if not encrypted_path:
        root.destroy()
        return

    key_path = filedialog.askopenfilename(
        title="Select the matching secret key",
        filetypes=[("Key files", "*.key")]
    )

    if not key_path:
        root.destroy()
        return

    try:
        key = Path(key_path).read_bytes()
        data = Path(encrypted_path).read_bytes()

        if len(key) != 32 or len(data) < 28:
            raise ValueError("Invalid key or encrypted file.")

        nonce = data[:12]
        ciphertext = data[12:]

        # Decryption fails if the key is wrong or data was changed
        aes = AESGCM(key)
        original_data = aes.decrypt(nonce, ciphertext, None)

        output_path = filedialog.asksaveasfilename(
            title="Save recovered image",
            initialfile="recovered_image.png",
            defaultextension=".png"
        )

        if not output_path:
            root.destroy()
            return

        Path(output_path).write_bytes(original_data)

        messagebox.showinfo(
            "Success",
            f"Image decrypted successfully!\n{output_path}"
        )

    except Exception:
        messagebox.showerror(
            "Decryption failed",
            "Check that you selected the correct key and encrypted file."
        )

    finally:
        root.destroy()


def main():
    root = Tk()
    root.withdraw()

    choice = messagebox.askyesnocancel(
        "Secure Image Encryption",
        "YES = Encrypt image\nNO = Decrypt image\nCANCEL = Exit"
    )
    root.destroy()

    if choice is True:
        encrypt_image()
    elif choice is False:
        decrypt_image()


if __name__ == "__main__":
    main()
