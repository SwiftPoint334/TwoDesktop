import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import random

root = tk.Tk()
root.title("Member Management System")
root.state("zoomed")  # Maximize the main window

conn = sqlite3.connect('user_accounts.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL PRIMARY KEY, password TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS people (id TEXT NOT NULL PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, dob TEXT NOT NULL, gender TEXT NOT NULL, eligibility TEXT NOT NULL, active_contact INTEGER, notes TEXT)''')

home_frame = None  # Define home_frame as a global variable

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
        create_home_menu()
    else:
        messagebox.showerror("Login", "Login failed. Incorrect username or password.")

def create_home_menu():
    global home_frame
    background_frame.destroy()  # Clear the login elements

    home_frame = tk.Frame(root, bg="grey")
    home_frame.place(relwidth=1, relheight=1)

    welcome_label = tk.Label(home_frame, text="Welcome to the Home Menu!", font=("Helvetica", 16), bg="grey")
    welcome_label.pack(pady=20)

    buttons_frame = tk.Frame(home_frame, bg="grey")
    buttons_frame.pack()

    search_button = tk.Button(buttons_frame, text="Search Members", command=search_members)
    search_button.pack(side="left", padx=10)

    add_person_button = tk.Button(buttons_frame, text="Add New Person", command=create_person_form)
    add_person_button.pack(side="left", padx=10)

def create_person_form():
    global home_frame
    home_frame.destroy()  # Clear the home menu elements

    person_frame = tk.Frame(root, bg="grey")
    person_frame.place(relwidth=1, relheight=1)

    person_heading = tk.Label(person_frame, text="Add New Person", font=("Helvetica", 16), bg="grey")
    person_heading.pack(pady=20)

    first_name_label = tk.Label(person_frame, text="First Name:", bg="grey")
    first_name_label.pack()

    first_name_entry = tk.Entry(person_frame)
    first_name_entry.pack(padx=10, pady=5, ipadx=5, ipady=5)

    last_name_label = tk.Label(person_frame, text="Last Name:", bg="grey")
    last_name_label.pack()

    last_name_entry = tk.Entry(person_frame)
    last_name_entry.pack(padx=10, pady=5, ipadx=5, ipady=5)

    dob_label = tk.Label(person_frame, text="Date of Birth (YYYY-MM-DD):", bg="grey")
    dob_label.pack()

    dob_entry = tk.Entry(person_frame)
    dob_entry.pack(padx=10, pady=5, ipadx=5, ipady=5)

    gender_label = tk.Label(person_frame, text="Gender:", bg="grey")
    gender_label.pack()

    gender_var = tk.StringVar(person_frame)
    gender_var.set("Male")  # Default value
    gender_choices = ["Male", "Female", "Other"]
    gender_menu = tk.OptionMenu(person_frame, gender_var, *gender_choices)
    gender_menu.pack(padx=10, pady=5, ipadx=5, ipady=5)

    eligibility_label = tk.Label(person_frame, text="Eligibility:", bg="grey")
    eligibility_label.pack()

    eligibility_var = tk.StringVar(person_frame)
    eligibility_var.set("Personal")  # Default value
    eligibility_choices = ["Personal", "Work", "Hostile", "Personal-L", "Other"]
    eligibility_menu = tk.OptionMenu(person_frame, eligibility_var, *eligibility_choices)
    eligibility_menu.pack(padx=10, pady=5, ipadx=5, ipady=5)

    active_contact_var = tk.IntVar()
    active_contact_checkbox = tk.Checkbutton(person_frame, text="Active Contact", variable=active_contact_var, bg="grey")
    active_contact_checkbox.pack()

    notes_label = tk.Label(person_frame, text="Notes:", bg="grey")
    notes_label.pack()

    notes_entry = tk.Text(person_frame, height=5, width=40)  # Adjust size
    notes_entry.pack(padx=10, pady=5, ipadx=5, ipady=5)

    add_button = tk.Button(person_frame, text="Add Person", command=lambda: add_person(first_name_entry.get(), last_name_entry.get(), dob_entry.get(), gender_var.get(), eligibility_var.get(), active_contact_var.get(), notes_entry.get("1.0", "end-1c")))
    add_button.pack()

    back_button = tk.Button(person_frame, text="Back", command=create_home_menu)
    back_button.pack()

def add_person(first_name, last_name, dob, gender, eligibility, active_contact, notes):
    if first_name and last_name and dob and gender and eligibility:
        unique_id = generate_unique_id()
        c.execute("INSERT INTO people (id, first_name, last_name, dob, gender, eligibility, active_contact, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (unique_id, first_name, last_name, dob, gender, eligibility, active_contact, notes))
        conn.commit()
        messagebox.showinfo("Success", "Person added successfully!")
        #return to home screen
        create_home_menu()
    else:
        messagebox.showerror("Error", "Please fill in required fields.")

def generate_unique_id():
    while True:
        unique_id = "B-" + ''.join(str(random.randint(0, 9)) for _ in range(4))
        c.execute("SELECT * FROM people WHERE id = ?", (unique_id,))
        if not c.fetchone():
            return unique_id

def get_members_list(search_query):
    c.execute("SELECT * FROM people WHERE id LIKE ? OR first_name LIKE ? OR last_name LIKE ?", (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    return c.fetchall()

def search_members():
    global home_frame
    home_frame.destroy()  # Clear the home menu elements

    search_frame = tk.Frame(root, bg="grey")
    search_frame.place(relwidth=1, relheight=1)

    search_heading = tk.Label(search_frame, text="Search Members", font=("Helvetica", 16), bg="grey")
    search_heading.pack(pady=20)

    search_entry = tk.Entry(search_frame)
    search_entry.pack(padx=10, pady=5, ipadx=5, ipady=5)

    search_button = tk.Button(search_frame, text="Search", command=lambda: display_member_list(search_entry.get()))
    search_button.pack()

    back_button = tk.Button(search_frame, text="Back", command=create_home_menu)
    back_button.pack()

def display_member_list(search_query):
    members = get_members_list(search_query)
    if members:
        listbox = tk.Listbox(root, font=("Helvetica", 12), bg="grey")
        listbox.pack(fill=tk.BOTH, expand=True)

        for member in members:
            listbox.insert(tk.END, f"{member[0]} - {member[1]} {member[2]}")

        def on_member_select(event):
            selected_index = listbox.curselection()
            if selected_index:
                member_id = listbox.get(selected_index[0]).split()[0]
                display_member_details(member_id)

        listbox.bind("<Double-Button-1>", on_member_select)  # Extract ID from selected entry

        back_button = tk.Button(root, text="Back", command=create_home_menu)
        back_button.pack()
    else:
        messagebox.showerror("Error", "No members found.")

def display_member_details(member_id):
    member = get_member_details(member_id)
    if member:
        popup = tk.Toplevel()
        popup.title("Member Details")
        popup.geometry("300x200")

        details_label = tk.Label(popup, text=f"ID: {member[0]}\nFirst Name: {member[1]}\nLast Name: {member[2]}\nDate of Birth: {member[3]}\nGender: {member[7]}\nActive Contact: {'Yes' if member[6] else 'No'}\nNotes: {member[4]}", font=("Helvetica", 12))
        details_label.pack(pady=10)

        edit_button = tk.Button(popup, text="Edit", command=lambda: edit_member(member_id))
        edit_button.pack()

        delete_button = tk.Button(popup, text="Delete", command=lambda: delete_member(member_id))
        delete_button.pack()

def get_member_details(member_id):
    c.execute("SELECT * FROM people WHERE id = ?", (member_id,))
    return c.fetchone()

def edit_member(member_id):
    member = get_member_details(member_id)
    if member:
        edit_frame = tk.Toplevel()
        edit_frame.title("Edit Member")
        edit_frame.geometry("300x300")

        edit_heading = tk.Label(edit_frame, text="Edit Member", font=("Helvetica", 16))
        edit_heading.pack(pady=10)

        # Create entry fields and labels for editing
        first_name_label = tk.Label(edit_frame, text="First Name:")
        first_name_label.pack()
        first_name_entry = tk.Entry(edit_frame)
        first_name_entry.insert(0, member[1])
        first_name_entry.pack(pady=5)

        last_name_label = tk.Label(edit_frame, text="Last Name:")
        last_name_label.pack()
        last_name_entry = tk.Entry(edit_frame)
        last_name_entry.insert(0, member[2])
        last_name_entry.pack(pady=5)

        dob_label = tk.Label(edit_frame, text="Date of Birth (YYYY-MM-DD):")
        dob_label.pack()
        dob_entry = tk.Entry(edit_frame)
        dob_entry.insert(0, member[3])
        dob_entry.pack(pady=5)

        gender_label = tk.Label(edit_frame, text="Gender:")
        gender_label.pack()
        gender_var = tk.StringVar()
        gender_var.set(member[5])
        gender_choices = ["Male", "Female", "Other"]
        gender_menu = tk.OptionMenu(edit_frame, gender_var, *gender_choices)
        gender_menu.pack(pady=5)

        eligibility_label = tk.Label(edit_frame, text="Eligibility:")
        eligibility_label.pack()
        eligibility_var = tk.StringVar()
        eligibility_var.set(member[6])
        eligibility_choices = ["Personal", "Work", "Hostile", "Personal-L", "Other"]
        eligibility_menu = tk.OptionMenu(edit_frame, eligibility_var, *eligibility_choices)
        eligibility_menu.pack(pady=5)

        active_contact_var = tk.IntVar()
        active_contact_checkbox = tk.Checkbutton(edit_frame, text="Active Contact", variable=active_contact_var)
        active_contact_checkbox.pack()

        notes_label = tk.Label(edit_frame, text="Notes:")
        notes_label.pack()
        notes_entry = tk.Text(edit_frame, height=5, width=40)
        notes_entry.insert("1.0", member[4])
        notes_entry.pack(pady=5)

        def save_changes():
            updated_first_name = first_name_entry.get()
            updated_last_name = last_name_entry.get()
            updated_dob = dob_entry.get()
            updated_gender = gender_var.get()
            updated_eligibility = eligibility_var.get()
            updated_active_contact = active_contact_var.get()
            updated_notes = notes_entry.get("1.0", "end-1c")

            c.execute("UPDATE people SET first_name=?, last_name=?, dob=?, gender=?, eligibility=?, active_contact=?, notes=? WHERE id=?",
                      (updated_first_name, updated_last_name, updated_dob, updated_gender, updated_eligibility, updated_active_contact, updated_notes, member_id))
            conn.commit()
            messagebox.showinfo("Success", "Member updated successfully!")
            edit_frame.destroy()

        save_button = tk.Button(edit_frame, text="Save Changes", command=save_changes)
        save_button.pack(pady=10)

def delete_member(member_id):
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this member?")
    if confirm:
        c.execute("DELETE FROM people WHERE id=?", (member_id,))
        conn.commit()
        messagebox.showinfo("Success", "Member deleted successfully!")


# Create a "Login" heading label
background_frame = tk.Frame(root, bg="grey")
background_frame.place(relwidth=1, relheight=1)

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

