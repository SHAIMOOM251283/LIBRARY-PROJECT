import tkinter as tk
import sqlite3

# Create a connection to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create a table to store member information
c.execute('''CREATE TABLE IF NOT EXISTS members
             (id INTEGER PRIMARY KEY, member_id TEXT, name TEXT, address TEXT, email TEXT, phone TEXT)''')

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Library Members")
        self.geometry("410x200")

        # Create labels and entry widgets
        self.lbl_member_id = tk.Label(self, text="Member ID:")
        self.ent_member_id = tk.Entry(self, width=55)

        self.lbl_name = tk.Label(self, text="Name:")
        self.ent_name = tk.Entry(self, width=55)

        self.lbl_address = tk.Label(self, text="Address:")
        self.ent_address = tk.Entry(self, width=55)

        self.lbl_email = tk.Label(self, text="Email:")
        self.ent_email = tk.Entry(self, width=55)

        self.lbl_phone = tk.Label(self, text="Phone:")
        self.ent_phone = tk.Entry(self, width=55)

        # Add member button
        self.add_member_btn = tk.Button(self, text="Add Member", command=self.add_member)

        # Delete member button
        self.del_member_btn = tk.Button(self, text="Delete Member", command=self.del_member)

        # Display all members button
        self.display_all_btn = tk.Button(self, text="Display Members", command=self.display_members)

        # Set grid layout
        self.lbl_member_id.grid(row=0, column=0)
        self.ent_member_id.grid(row=0, column=1, columnspan=2)

        self.lbl_name.grid(row=1, column=0)
        self.ent_name.grid(row=1, column=1, columnspan=2)

        self.lbl_address.grid(row=2, column=0)
        self.ent_address.grid(row=2, column=1, columnspan=2)

        self.lbl_email.grid(row=3, column=0)
        self.ent_email.grid(row=3, column=1, columnspan=2)

        self.lbl_phone.grid(row=4, column=0)
        self.ent_phone.grid(row=4, column=1, columnspan=2)

        self.add_member_btn.grid(row=5, column=2, sticky="E")
        self.del_member_btn.grid(row=6, column=2, sticky="E")
        self.display_all_btn.grid(row=7, column=2, sticky="E")

    def add_member(self):
        # Get values from entry widgets
        member_id = self.ent_member_id.get()
        name = self.ent_name.get()
        address = self.ent_address.get()
        email = self.ent_email.get()
        phone = self.ent_phone.get()

        # Insert values into members table
        c.execute("INSERT INTO members (member_id, name, address, email, phone) VALUES (?, ?, ?, ?, ?)",
                  (member_id, name, address, email, phone))

        # Clear entry widgets
        self.ent_member_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_address.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)

        # Commit changes to the database
        conn.commit()

    def del_member(self):
        # Get member ID to delete
        member_id = self.ent_member_id.get()

        # Delete member from members table
        c.execute("DELETE FROM members WHERE member_id=?", (member_id,))

        # Clear entry widgets
        self.ent_member_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_address.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)

        # Commit changes to the database
        conn.commit()

    def display_members(self):
        # Fetch all members from members table
        c.execute("SELECT * FROM members")
        members = c.fetchall()

        # Create a new window to display members
        members_window = tk.Toplevel(self)
        members_window.title("Library Members")
        members_window.geometry("865x400")

        # Create a scrollbar
        scrollbar = tk.Scrollbar(members_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox with scrollbar
        listbox = tk.Listbox(members_window, yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)

        # Configure the scrollbar
        scrollbar.config(command=listbox.yview)

        # Insert members into listbox
        for member in members:
            listbox.insert(tk.END, f"ID: {member[1]} | Name: {member[2]} | Address: {member[3]} | Email: {member[4]} | Phone: {member[5]}")

# Create and run the LibraryApp instance
if __name__ == '__main__':
    app = LibraryApp()
    app.mainloop()

# Close the database connection
conn.close()

       
