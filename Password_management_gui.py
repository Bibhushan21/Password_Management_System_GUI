import base64
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Predefined master password
CORRECT_MASTER_PASSWORD = "bbsn"

class PasswordManager:
    def __init__(self, master_password):
        self.key = self._generate_key(master_password)
        self.fernet = Fernet(self.key)
        self.passwords = {}

    def _generate_key(self, master_password):
        salt = b'fixed_salt_for_demo'  # Fixed salt for demonstration
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    def add_password(self, account, password):
        encrypted_password = self.fernet.encrypt(password.encode())
        self.passwords[account] = encrypted_password

    def get_password(self, account):
        if account in self.passwords:
            encrypted_password = self.passwords[account]
            decrypted_password = self.fernet.decrypt(encrypted_password)
            return decrypted_password.decode()
        else:
            return None

    def delete_password(self, account):
        if account in self.passwords:
            del self.passwords[account]
            return True
        return False

    def list_accounts(self):
        return list(self.passwords.keys())

class PasswordManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        self.master.geometry("300x200")
        self.pm = None

        self.create_widgets()

    def create_widgets(self):
        self.master_password_label = tk.Label(self.master, text="Enter master password:")
        self.master_password_label.pack(pady=10)

        self.master_password_entry = tk.Entry(self.master, show="*")
        self.master_password_entry.pack()

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        entered_password = self.master_password_entry.get()
        if entered_password == CORRECT_MASTER_PASSWORD:
            self.pm = PasswordManager(entered_password)
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Incorrect master password")

    def show_main_menu(self):
        # Clear existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Create main menu buttons
        tk.Button(self.master, text="Add Password", command=self.add_password).pack(pady=5)
        tk.Button(self.master, text="Get Password", command=self.get_password).pack(pady=5)
        tk.Button(self.master, text="Delete Password", command=self.delete_password).pack(pady=5)
        tk.Button(self.master, text="List Accounts", command=self.list_accounts).pack(pady=5)

    def add_password(self):
        account = simpledialog.askstring("Add Password", "Enter account name:")
        if account:
            password = simpledialog.askstring("Add Password", "Enter password:", show="*")
            if password:
                self.pm.add_password(account, password)
                messagebox.showinfo("Success", "Password added successfully!")
            else:
                messagebox.showerror("Error", "Password cannot be empty")
        else:
            messagebox.showerror("Error", "Account name cannot be empty")

    def get_password(self):
        account = simpledialog.askstring("Get Password", "Enter account name:")
        if account:
            password = self.pm.get_password(account)
            if password:
                messagebox.showinfo("Password", f"Password for {account}: {password}")
            else:
                messagebox.showerror("Error", "Account not found")
        else:
            messagebox.showerror("Error", "Account name cannot be empty")

    def delete_password(self):
        account = simpledialog.askstring("Delete Password", "Enter account name:")
        if account:
            if self.pm.delete_password(account):
                messagebox.showinfo("Success", "Password deleted successfully!")
            else:
                messagebox.showerror("Error", "Account not found")
        else:
            messagebox.showerror("Error", "Account name cannot be empty")

    def list_accounts(self):
        accounts = self.pm.list_accounts()
        if accounts:
            account_list = "\n".join(accounts)
            messagebox.showinfo("Stored Accounts", f"Stored accounts:\n{account_list}")
        else:
            messagebox.showinfo("Stored Accounts", "No accounts stored.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
