# 🔐 RSA Cryptosystem in Python

A Python-based **desktop application** for **RSA key generation, encryption, and decryption** with a simple **Tkinter GUI**.  
This project demonstrates how asymmetric encryption works in practice while offering a user-friendly interface.

## Features
- 🔑 Generate RSA key pairs (public & private) with custom key sizes.
- ✉️ Message encryption & decryption
- ✅ Dark mode modern GUI built with Tkinter. 
- 🧮 Prime number generation using the Rabin-Miller primality test
- 📂 Save & load keys from files

## Modules
- **file1 (Desktop)**: GUI application
- **file2 (KeyGenerator)**: RSA key generation, encryption & decryption
- **file3 (Math)**: Math utilities (GCD, modular inverse)
- **file4 (PrimeNumber)**: Prime number generation & Rabin-Miller test
- **file5 (Assets)**: Icons and logos

## 🛠️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ArianGhanooni/Asymmetric-Key-Encryption.git
   cd Asymmetric-Key-Encryption

2. Install Python (>=3.8).

3. Run the application:
    python desktop.py

4. You can build a single .exe file using PyInstaller:
    ```bash
    pyinstaller --onefile --noconsole --add-data "Assets;Assets" desktop.py

---

> [!warning]
> The executable file must be placed in the same directory as the Assets folder.
> Otherwise, the application may fail to load icons and images correctly.

---

## 📖 How It Works

1. Enter a key size and generate RSA keys.
2. Provide a file name to save keys.
3. Write a message in the "Plain Text" field.
4. Encrypt the message → Cipher text appears.
5. Save the cipher into a file.
6. Decrypt using the saved cipher file → Original text appears.

## 👨‍💻 Author

### Arian Ghanooni
