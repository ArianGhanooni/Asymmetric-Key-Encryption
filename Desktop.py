#Imports
import webbrowser
from tkinter import *
from tkinter import filedialog
from KeyGenerator import *
from tkinter import messagebox
import sqlite3

Current_User = None

conn = sqlite3.connect("RSA_App_Database.db")
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Public_key TEXT,
    Private_key TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Sender_ID INTEGER,
    Receiver_ID INTEGER,
    Message TEXT,
    Status TEXT,
    FOREIGN KEY(Sender_ID) REFERENCES users(ID) ON DELETE CASCADE,
    FOREIGN KEY(Receiver_ID) REFERENCES users(ID) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()

# ----------------------------
# Event Handlers (to be implemented later)
# ----------------------------
def Generate_Key_Button():
    """Handle Generate Key button click."""
    def Confirm_Key():
        try:
            keySize = int(entry_keysize.get())
            fileName = Entry_Key.get()
            
            if not fileName:
                messagebox.showwarning("Warning", "Please enter a file name in the main window!")
                return
            
            # Call Key Generator function
            publicKey, privateKey = generateKeys(keySize, log = True)
            writeKeysToFile(keySize, publicKey, privateKey, fileName)  
            
            messagebox.showinfo("Success", f"Key generated successfully!\nFile: {fileName}")
            top.destroy()
        except ValueError:
            messagebox.showerror("Error", "Key size must be a number!")

    # Create popup window
    top = Toplevel(root)
    top.title("Key Size")
    top.geometry("300x150")
    top.resizable(False, False)
    top.config(bg="#121212")

    Label(top, text="Enter Key Size:", font=("Inter", 12, "bold"),
          bg="#121212", fg="#ffffff").pack(pady=10)

    entry_keysize = Entry(top, font=("Inter", 12), bg="#262626", fg="#ffffff", width=15)
    entry_keysize.pack(pady=5)

    Button(top, text="Generate", font=("Inter", 12, "bold"),
           bg="#d32f2f", fg="#ffffff",
           activebackground="#ffffff", activeforeground="#d32f2f",
           command=Confirm_Key).pack(pady=15)
    
def Encrypt_Button():
    """Handle Encrypt button click."""
    # Step 1: Check for key filename
    filename = Entry_Key.get().strip()
    if not filename:
        messagebox.showwarning("Warning", "Please enter a file name in the 'File Name' field!")
        return

    # Step 2: Check for plain text
    plaintext = Plain_Text.get("1.0", END).strip()
    if not plaintext:
        messagebox.showwarning("Warning", "Please enter a message in the Plain Text field!")
        return

    # Step 3: Save cipher if Entry_Decrypt is provided
    cipher_filename = Entry_Decrypt.get().strip()
    if not cipher_filename:
        messagebox.showwarning("Warning", "Please enter a name for save cipher file in the 'Encrypted File' field!")
        return
    
    try:
        # Step 4: Encrypt message (adjust to your encryption function)
        public, private = readKeysFromFile(filename)
        encrypt(plaintext, public, cipher_filename)
        messagebox.showinfo("Success", f"Message encrypted and saved as {cipher_filename}")

        # Step 5: Clear Cipher_Text and insert result
        encrypted_path = os.path.join(BASE_DIR, cipher_filename)
        with open(encrypted_path, 'r') as file:
              Cipher = file.read()

        Cipher_Text.delete("1.0", END)
        Cipher_Text.insert("1.0", Cipher)

    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed:\n{e}")

def Decrypt_Button():
    """Handle Decrypt button click."""
    # Step 1: Check for key filename
    filename = Entry_Key.get().strip()
    if not filename:
        messagebox.showwarning("Warning", "Please enter a file name in the 'File Name' field!")
        return

    # Step 2: Check for cipher file name
    cipher_filename = Entry_Decrypt.get().strip()
    if not cipher_filename:
        messagebox.showwarning("Warning", "Please enter the encrypted file name in the 'Encrypted File' field!")
        return

    try:
        # Step 3: Read cipher text from file
        public, private = readKeysFromFile(filename)
        original_File = decrypt(cipher_filename, private)

        # Step 4: Clear Original_Text and insert result
        Original_Text.delete("1.0", END)
        Original_Text.insert("1.0", original_File)

        messagebox.showinfo("Success", "Message decrypted successfully!")

    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{cipher_filename}.txt' not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed:\n{e}")

def Open_Link(event=None):
    """Open GitHub link in default browser."""
    url = "https://github.com/ArianGhanooni"
    webbrowser.open_new_tab(url)

def Login():
    login_win = Toplevel(root)
    login_win.title("Login")
    login_win.geometry("300x220")
    login_win.resizable(False, False)
    login_win.config(bg="#121212")

    Label(login_win, text="Username :", font=("Inter", 12, "bold"),
          bg="#121212", fg="#ffffff").pack(pady=10)
    
    username_entry = Entry(login_win, font=("Inter", 12), bg="#262626", fg="#ffffff", width=15)
    username_entry.pack(pady=5)

    Label(login_win, text="Password :", font=("Inter", 12, "bold"),
          bg="#121212", fg="#ffffff").pack(pady=10)
    
    pass_entry = Entry(login_win, show="*", font=("Inter", 12), bg="#262626", fg="#ffffff", width=15)
    pass_entry.pack(pady=5)

    def do_login():
        global Current_User

        username = username_entry.get()
        password = pass_entry.get()

        conn = sqlite3.connect("RSA_App_Database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            Current_User = user
            messagebox.showinfo("Success", f"Logged in as {username}")
            root.title(f"RSA Encryption Tool {Current_User[1]}")
            login_win.destroy()

        else:
            messagebox.showerror("Error", "Invalid username or password")

    Button(login_win, text="Signup", font=("Inter", 12, "bold"),
           bg="#d32f2f", fg="#ffffff",
           activebackground="#ffffff", activeforeground="#d32f2f",
           command=do_login).pack(pady=15)

def Logout():
    global Current_User
    
    if Current_User:
        messagebox.showinfo("Logout", f"User {Current_User[1]} logged out")
        root.title("RSA Encryption Tool")
        Current_User = None
    else:
        messagebox.showwarning("Warning", "No user logged in!")

def Signup():
    signup_win = Toplevel(root)
    signup_win.title("Signup")
    signup_win.geometry("300x300")
    signup_win.resizable(False, False)
    signup_win.config(bg="#121212")

    Label(signup_win, text="Username :", font=("Inter", 12, "bold"),
          bg="#121212", fg="#ffffff").pack(pady=10)
    
    username_entry = Entry(signup_win, font=("Inter", 12), bg="#262626", fg="#ffffff", width=15)
    username_entry.pack(pady=5)

    Label(signup_win, text="Password :", font=("Inter", 12, "bold"),
          bg="#121212", fg="#ffffff").pack(pady=10)
    
    pass1_entry = Entry(signup_win, show="*", font=("Inter", 12), bg="#262626", fg="#ffffff", width=15)
    pass1_entry.pack(pady=5)

    Label(signup_win, text="Confirm Password :", font=("Inter", 12, "bold"),
          bg="#121212", fg="#ffffff").pack(pady=10)

    pass2_entry = Entry(signup_win, show="*", font=("Inter", 12), bg="#262626", fg="#ffffff", width=15)
    pass2_entry.pack(pady=5)

    def register():
        username = username_entry.get()
        pass1 = pass1_entry.get()
        pass2 = pass2_entry.get()

        if not username or not pass1 or not pass2:
            messagebox.showerror("Error", "All fields are required!")
            return

        if pass1 != pass2:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            conn = sqlite3.connect("RSA_App_Database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, pass1))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully!")
            signup_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    Button(signup_win, text="Signup", font=("Inter", 12, "bold"),
           bg="#d32f2f", fg="#ffffff",
           activebackground="#ffffff", activeforeground="#d32f2f",
           command=register).pack(pady=15)

def Sent_Messages():
    pass

def Received_Messages():
    pass

def Public_Keys():
    pass

def Private_Keys():
    pass

# ----------------------------
# Main Window Configuration
# ----------------------------
root = Tk()

root.geometry("520x750+0+0")   # Window size
root.resizable(False, False)   # Disable resizing
root.config(background="#121212")
root.title("RSA Encryption Tool")

# ----------------------------
# Menu Bar
# ----------------------------
menubar = Menu(root)
account_menu = Menu(menubar, tearoff=0,  font=("Inter", 10, "bold"))
account_menu.add_command(label="Login", command=Login)
account_menu.add_command(label="Logout", command=Logout)
account_menu.add_separator()
account_menu.add_command(label="Signup", command=Signup)
menubar.add_cascade(label="Account", menu=account_menu)

selection_menu = Menu(menubar, tearoff=0,  font=("Inter", 10, "bold"))
selection_menu.add_command(label="Sent Messages", command=Sent_Messages)
selection_menu.add_command(label="Received Messages", command=Received_Messages)
selection_menu.add_separator()
selection_menu.add_command(label="Public Keys", command=Public_Keys)
selection_menu.add_command(label="Private Keys", command=Private_Keys)
menubar.add_cascade(label="Selection", menu=selection_menu)

root.config(menu=menubar)

# ----------------------------
# Window Icon
# ----------------------------
Icon_Path = os.path.join(BASE_DIR, "Assets/Lock Icon.png")
Icon = PhotoImage(file = Icon_Path)
root.iconphoto(True, Icon)

# ----------------------------
# App Logo
# ----------------------------
RSA_Logo_Path = os.path.join(BASE_DIR, "Assets/RSA Encryption Tool Logo.png")
RSA_Logo = PhotoImage(file = RSA_Logo_Path)
RSA_Logo_widget = Label(root, image = RSA_Logo, bg = "#121212")
RSA_Logo_widget.image = RSA_Logo
RSA_Logo_widget.grid(row=0, column=0, columnspan=4, pady=(15, 25))

# ----------------------------
# Key Management Section
# ----------------------------
Label(root, text="Key Management", font=("Inter", 15, "bold"),
      bg="#121212", fg="#ffffff").grid(row=1, column=0, columnspan=4, pady=(0, 5))

Button(root, text="Generate Key", font=("Inter", 12, "bold"),
       bg="#d32f2f", fg="#ffffff",
       activebackground="#ffffff", activeforeground="#d32f2f",
       width=12, height=1,
       command=Generate_Key_Button).grid(row=2, column=0, padx=(0, 38))

Label(root, text="File Name : ", font=("Inter", 14),
      bg="#121212", fg="#ffffff").grid(row=2, column=2, padx=(40, 0))

Entry_Key = Entry(root, font=("Inter", 12),
                  bg="#262626", fg="#ffffff", width=12)
Entry_Key.grid(row=2, column=3, padx= (0, 10))

# ----------------------------
# Encryption Section
# ----------------------------
Label(root, text="Encryption", font=("Inter", 15, "bold"),
      bg="#121212", fg="#ffffff").grid(row=3, column=0, columnspan=4, pady=(10, 5))

Label(root, text="Plain Text : ", font=("Inter", 14),
      bg="#121212", fg="#ffffff").grid(row=4, column=0, sticky=W, padx=(15, 0))

Plain_Text = Text(root, font=("Inter", 13),
                  bg="#262626", fg="#ffffff", height=2, width=40)
Plain_Text.grid(row=5, column=0, columnspan=4, pady=5, padx= 15)

Button(root, text="Encrypt", font=("Inter", 12, "bold"),
       bg="#d32f2f", fg="#ffffff",
       activebackground="#ffffff", activeforeground="#d32f2f",
       width=12, height=1,
       command=Encrypt_Button).grid(row=6, column=0, columnspan=4, sticky=W, padx=(15, 0))

Label(root, text="Cipher Text : ", font=("Inter", 14),
      bg="#121212", fg="#ffffff").grid(row=7, column=0, sticky=W, padx=(15, 0), pady=(7, 0))

Cipher_Text = Text(root, font=("Inter", 13),
                   bg="#262626", fg="#ffffff", height=2, width=40)
Cipher_Text.grid(row=8, column=0, columnspan=4, pady=5, padx=15)

# ----------------------------
# Decryption Section
# ----------------------------
Label(root, text="Decryption", font=("Inter", 14, "bold"),
      bg="#121212", fg="#ffffff").grid(row=9, column=0, columnspan=4, pady=(10, 10))

Button(root, text="Decrypt", font=("Inter", 12, "bold"),
       bg="#d32f2f", fg="#ffffff",
       activebackground="#ffffff", activeforeground="#d32f2f",
       width=12, height=1,
       command=Decrypt_Button).grid(row=10, column=0, padx=(0, 35))

Label(root, text="Encrypted File : ", font=("Inter", 14),
      bg="#121212", fg="#ffffff").grid(row=10, column=2, sticky=W, padx=(0, 0))

Entry_Decrypt = Entry(root, font=("Inter", 12),
                      bg="#262626", fg="#ffffff", width=11)
Entry_Decrypt.grid(row=10, column=3, padx= (0, 10))

Label(root, text="Original Text : ", font=("Inter", 14),
      bg="#121212", fg="#ffffff").grid(row=11, column=0, sticky=W, padx=(15, 0), pady=(7, 0))

Original_Text = Text(root, font=("Inter", 13),
                     bg="#262626", fg="#ffffff", height=2, width=40)
Original_Text.grid(row=12, column=0, columnspan=4, padx=15)

# ----------------------------
# Footer Section
# ----------------------------
Label(root, text="Developed by Arian Ghanooni",
      bg="#121212", fg="#ffffff", font=("Inter", 10)).grid(row=13, column=0, sticky=W, padx=(15, 0), pady=(65, 0))

GitHub_Logo_Path = os.path.join(BASE_DIR, "Assets/GitHub Logo.png")
GitHub_Logo = PhotoImage(file = GitHub_Logo_Path)
GitHub_Logo_widget = Label(root, image = GitHub_Logo, bg = "#121212", cursor="hand2")
GitHub_Logo_widget.image = GitHub_Logo
GitHub_Logo_widget.bind("<Button-1>", Open_Link)
GitHub_Logo_widget.grid(row=13, column=3, sticky=E, padx=(0, 10), pady=(65, 0))

# ----------------------------
# Start Main Loop
# ----------------------------
root.mainloop()