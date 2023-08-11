import tkinter as tk
from tkinter import messagebox
import sqlite3

root = tk.Tk()
root.title("Login Screen")
root.geometry("400x300")  # Set a larger size for the window

# Create a grey background
background_frame = tk.Frame(root, bg="grey")
background_frame.place(relwidth=1, relheight=1)

conn = sqlite3.connect('user_accounts.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL PRIMARY KEY, password TEXT NOT NULL)''')

def on_username_click(event):
    if login_username.get() == "Username":
        login_username.delete(0, "end")
        login_username.config(fg="black")

def on_password_click(event):
    if login_password.get() == "Password":
        login_password.delete(0, "end")
        login_password.config(fg="black", show="*")

def login():
    username = login_username.get()
    password = login_password.get()

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()

    if user:
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Login failed. Incorrect username or password.")

# Create a "Login" heading label
login_heading = tk.Label(background_frame, text="Login", font=("Helvetica", 20), bg="grey")
login_heading.pack(pady=20)

login_label = tk.Label(background_frame, text="Login:", bg="grey")
login_label.pack()

login_username = tk.Entry(background_frame, fg="grey")
login_username.insert(0, "Username")
login_username.bind("<Button-1>", on_username_click)
login_username.pack(padx=10, pady=5, ipadx=5, ipady=5)  # Adjust padding and internal padding

login_password = tk.Entry(background_frame, fg="grey")
login_password.insert(0, "Password")
login_password.bind("<Button-1>", on_password_click)
login_password.pack(padx=10, pady=5, ipadx=5, ipady=5)  # Adjust padding and internal padding

login_button = tk.Button(background_frame, text="Login", command=login, highlightthickness=0)  # Remove the border
login_button.pack(pady=10)

root.mainloop()
conn.close()


