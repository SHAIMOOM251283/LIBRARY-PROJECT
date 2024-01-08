import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk

# Create a connection to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS orders
             (id INTEGER PRIMARY KEY, order_no TEXT, member_id INTEGER, member_name TEXT, book_id INTEGER, book_title TEXT, issue_date TEXT, return_date TEXT,
             FOREIGN KEY (member_id) REFERENCES members (id),
             FOREIGN KEY (book_id) REFERENCES books (id))''')

class OrderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Order Management")
        self.geometry("415x200")

        # Create labels and comboboxes
        self.lbl_order_no = tk.Label(self, text="Order No:")
        self.ent_order_no = tk.Entry(self, width=55)

        self.lbl_member = tk.Label(self, text="Member ID:")
        self.member_var = tk.StringVar(self)
        self.combo_member = ttk.Combobox(self, textvariable=self.member_var, values=self.get_members(), width=52)

        self.lbl_book = tk.Label(self, text="Book ID:")
        self.book_var = tk.StringVar(self)
        self.combo_book = ttk.Combobox(self, textvariable=self.book_var, values=self.get_books(), width=52)

        self.lbl_issue_date = tk.Label(self, text="Issue Date:")
        self.ent_issue_date = tk.Entry(self, width=55)

        self.lbl_return_date = tk.Label(self, text="Return Date:")
        self.ent_return_date = tk.Entry(self, width=55)

        # Add order button
        self.add_order_btn = tk.Button(self, text="Add Order", command=self.add_order)

        # Delete order button
        self.del_order_btn = tk.Button(self, text="Delete Order", command=self.del_order)

        # Display all orders button
        self.display_all_btn = tk.Button(self, text="Display Orders", command=self.display_orders)

        # Set grid layout
        self.lbl_order_no.grid(row=0, column=0)
        self.ent_order_no.grid(row=0, column=1, columnspan=2)

        self.lbl_member.grid(row=1, column=0)
        self.combo_member.grid(row=1, column=1, columnspan=2)

        self.lbl_book.grid(row=2, column=0)
        self.combo_book.grid(row=2, column=1, columnspan=2)

        self.lbl_issue_date.grid(row=3, column=0)
        self.ent_issue_date.grid(row=3, column=1, columnspan=2)

        self.lbl_return_date.grid(row=4, column=0)
        self.ent_return_date.grid(row=4, column=1, columnspan=2)

        self.add_order_btn.grid(row=5, column=2, sticky="E")
        self.del_order_btn.grid(row=6, column=2, sticky="E")
        self.display_all_btn.grid(row=7, column=2, sticky="E")

    def get_members(self):
        # Retrieve member IDs and names from the database
        c.execute("SELECT id, name FROM members")
        members = c.fetchall()
        members_list = [f"{member[0]} - {member[1]}" for member in members]
        return members_list

    def get_books(self):
        # Retrieve book IDs and titles from the database
        c.execute("SELECT id, title FROM books")
        books = c.fetchall()
        books_list = [f"{book[0]} - {book[1]}" for book in books]
        return books_list

    def add_order(self):
        # Get values from entry widgets
        order_no = self.ent_order_no.get()
        member = self.member_var.get()
        book = self.book_var.get()
        
        issue_date = self.ent_issue_date.get()
        return_date = self.ent_return_date.get()
        
        # Validate input
        if not order_no or not member or not book or not issue_date or not return_date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        # Extract member ID and book ID from the selected options
        member_id = member.split(" - ")[0]
        book_id = book.split(" - ")[0]
        
        # Fetch member_name and book_title from the database
        c.execute("SELECT name FROM members WHERE id=?", (member_id,))
        member_name = c.fetchone()[0]
        c.execute("SELECT title FROM books WHERE id=?", (book_id,))
        book_title = c.fetchone()[0]
        
        # Insert values into the orders table
        c.execute(
            "INSERT INTO orders (order_no, member_id, member_name, book_id, book_title, issue_date, return_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (order_no, member_id, member_name, book_id, book_title, issue_date, return_date)
        )
        
        # Clear entry widgets
        self.ent_order_no.delete(0, tk.END)
        self.member_var.set('')
        self.book_var.set('')
        self.ent_issue_date.delete(0, tk.END)
        self.ent_return_date.delete(0, tk.END)
        
        # Commit changes to the database
        conn.commit()
        
        messagebox.showinfo("Success", "Order added successfully.")

    def del_order(self):
        # Get order number to delete
        order_no = self.ent_order_no.get()

        # Delete order from the orders table
        c.execute("DELETE FROM orders WHERE order_no=?", (order_no,))

        # Clear entry widgets
        self.ent_order_no.delete(0, tk.END)
        self.member_var.set('')
        self.book_var.set('')
        self.ent_issue_date.delete(0, tk.END)
        self.ent_return_date.delete(0, tk.END)

        # Commit changes to the database
        conn.commit()

        messagebox.showinfo("Success", "Order deleted successfully.")

    def display_orders(self):
        # Fetch all orders from the orders table
        c.execute("SELECT * FROM orders")
        orders = c.fetchall()

        # Create a new window to display orders
        orders_window = tk.Toplevel(self)
        orders_window.title("Orders")
        orders_window.geometry("890x400")

        # Create a scrollbar
        scrollbar = tk.Scrollbar(orders_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox with scrollbar
        listbox = tk.Listbox(orders_window, yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)

        # Configure the scrollbar
        scrollbar.config(command=listbox.yview)

        # Insert orders into listbox
        for order in orders:
            listbox.insert(tk.END, f"Order No: {order[1]} | Member ID: {order[2]} | Member Name: {order[3]} | Book ID: {order[4]} | Book Title: {order[5]} | Issue Date: {order[6]} | Return Date: {order[7]}")

    def quit_app(self):
        # Close the database connection
        conn.close()
        self.destroy()

# Create and run the OrderApp instance
if __name__ == '__main__':
    app = OrderApp()
    app.protocol("WM_DELETE_WINDOW", app.quit_app)
    app.mainloop()

