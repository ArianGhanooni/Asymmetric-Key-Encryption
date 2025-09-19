# 🔐 RSA Cryptosystem in Python

A Python-based **desktop application** for **RSA key generation, encryption, and decryption** with a simple **Tkinter GUI**.  
Now enhanced with **SQLite database integration** for user authentication, message storage, and key management.

## Features
- 🔑 Generate RSA key pairs (public & private) with custom key sizes.
- 👤 User authentication system (Signup, Login, Logout).
- 🗝️ Store multiple public/private keys per user in the database.
- ✉️ Send and receive encrypted messages (saved in DB with status `send/receive`).
- ✅ Dark mode modern GUI built with Tkinter. 
- 🧮 Prime number generation using the Rabin-Miller primality test.
- 📂 Save & load keys from files.

## Modules
- **file1 (Desktop.py)**: GUI application + database integration (SQLite).
- **file2 (KeyGenerator.py)**: RSA key generation, encryption & decryption logic.
- **file3 (Math.py)**: Math utilities (GCD, modular inverse).
- **file4 (PrimeNumber.py)**: Prime number generation & Rabin-Miller test.
- **file5 (Assets/)**: Icons and logos.

## 🛠️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ArianGhanooni/Asymmetric-Key-Encryption.git
   cd Asymmetric-Key-Encryption
   ```

2. Install Python (>=3.8).

3. Run the application:
   ```bash
   python desktop.py
   ```

4. You can build a single .exe file using PyInstaller:
   ```bash
   pyinstaller --onefile --noconsole --add-data "Assets;Assets" desktop.py
   ```

---

> [!warning]
> The executable file must be placed in the same directory as the **Assets** folder and the **SQLite database file**.
> Otherwise, the application may fail to load icons, images, or user data correctly.

---

## 📖 How It Works

1. **User Authentication**  
   - Signup → Create a new account with username & password.  
   - Login → Authenticate and start a session.  
   - Logout → End current session.  

2. **Key Management**  
   - Generate RSA key pairs with custom sizes.  
   - Save keys to files or store them in the database.  
   - Select public/private keys when encrypting or decrypting.  

3. **Message Handling**  
   - Encrypt a message using another user’s public key → message saved in DB with status `send`.  
   - Decrypt received messages using your private key → message saved in DB with status `receive`.  
   - View all sent/received messages linked to your account.  

---

## 👨‍💻 Author

### Arian Ghanooni  
