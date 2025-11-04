import tkinter as tk
from tkinter import messagebox
import requests

BASE = "http://127.0.0.1:9000"
TIMEOUT = 3

session = requests.Session()

def login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showwarning("Input error", "Please enter both username and password.")
        return

    try:
        r = session.post(f"{BASE}/login",
                         data={"username": username, "password": password},
                         timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Connection error", "Cannot connect to backend server.")
        return

    if r.status_code == 200:
        messagebox.showinfo("Login success", "You are now logged in.")
        login_frame.pack_forget()
        show_main_frame()
    elif r.status_code == 401:
        messagebox.showerror("Unauthorized", "Invalid username or password.")
    else:
        messagebox.showerror("Error", f"Unexpected status: {r.status_code}")

def check_protected():
    try:
        r = session.get(f"{BASE}/protected", timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Connection error", "Cannot connect to backend server.")
        return

    if r.status_code == 200:
        messagebox.showinfo("Protected", "Access granted ✅")
    elif r.status_code == 401:
        messagebox.showwarning("Unauthorized", "Session expired or invalid.")
    else:
        messagebox.showerror("Error", f"Unexpected status: {r.status_code}")

def logout():
    global session
    session = requests.Session()  # reset session (clear cookies)
    main_frame.pack_forget()
    show_login_frame()
    messagebox.showinfo("Logout", "You have been logged out.")

def show_login_frame():
    login_frame.pack(padx=20, pady=20)

def show_main_frame():
    main_frame.pack(padx=20, pady=20)

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("WeApRous Login System")
root.geometry("350x250")
root.resizable(False, False)

# --- Login Frame ---
login_frame = tk.Frame(root)

tk.Label(login_frame, text="Username:").pack(anchor="w")
username_entry = tk.Entry(login_frame, width=30)
username_entry.pack()

tk.Label(login_frame, text="Password:").pack(anchor="w")
password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.pack()

tk.Button(login_frame, text="Login", command=login, bg="#4CAF50", fg="white", width=20).pack(pady=10)

# --- Main Frame (after login) ---
main_frame = tk.Frame(root)

tk.Label(main_frame, text="Welcome! You are logged in ✅", font=("Arial", 12)).pack(pady=10)
tk.Button(main_frame, text="Access /protected", command=check_protected, bg="#2196F3", fg="white", width=20).pack(pady=5)
tk.Button(main_frame, text="Logout", command=logout, bg="#f44336", fg="white", width=20).pack(pady=5)

# Start at login frame
show_login_frame()
root.mainloop()
