import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk

# Create a connection to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS returns
             (id INTEGER PRIMARY KEY, return_no TEXT, delivery_no TEXT, return_date TEXT, fine TEXT,
             FOREIGN KEY (delivery_no) REFERENCES delivery (delivery_no))''')


class ReturnApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Return Management")
        self.geometry("415x180")

        # Create labels and entry widgets
        self.lbl_return_no = tk.Label(self, text="Return No:")
        self.ent_return_no = tk.Entry(self, width=55)

        self.lbl_delivery_no = tk.Label(self, text="Delivery No:")
        self.delivery_var = tk.StringVar(self)
        self.combo_delivery = ttk.Combobox(self, textvariable=self.delivery_var, values=self.get_deliveries(), width=52)

        self.lbl_return_date = tk.Label(self, text="Return Date:")
        self.ent_return_date = tk.Entry(self, width=55)

        self.lbl_fine = tk.Label(self, text="Fine:")
        self.ent_fine = tk.Entry(self, width=55)

        # Add return button
        self.add_return_btn = tk.Button(self, text="Add Return", command=self.add_return)

        # Delete return button
        self.del_return_btn = tk.Button(self, text="Delete Return", command=self.del_return)

        # Display all returns button
        self.display_all_btn = tk.Button(self, text="Display Returns", command=self.display_returns)

        # Set grid layout
        self.lbl_return_no.grid(row=0, column=0)
        self.ent_return_no.grid(row=0, column=1, columnspan=2)

        self.lbl_delivery_no.grid(row=1, column=0)
        self.combo_delivery.grid(row=1, column=1, columnspan=2)

        self.lbl_return_date.grid(row=2, column=0)
        self.ent_return_date.grid(row=2, column=1, columnspan=2)

        self.lbl_fine.grid(row=3, column=0)
        self.ent_fine.grid(row=3, column=1, columnspan=2)

        self.add_return_btn.grid(row=4, column=2, sticky="E")
        self.del_return_btn.grid(row=5, column=2, sticky="E")
        self.display_all_btn.grid(row=6, column=2, sticky="E")

    def get_deliveries(self):
        # Retrieve delivery numbers from the database
        c.execute("SELECT delivery_no FROM delivery")
        deliveries = c.fetchall()
        deliveries_list = [delivery[0] for delivery in deliveries]
        return deliveries_list

    def add_return(self):
        # Get values from entry widgets
        return_no = self.ent_return_no.get()
        delivery_no = self.delivery_var.get()
        return_date = self.ent_return_date.get()
        fine = self.ent_fine.get()

        # Validate input
        if not return_no or not delivery_no or not return_date or not fine:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Insert values into the returns table
        c.execute(
            "INSERT INTO returns (return_no, delivery_no, return_date, fine) VALUES (?, ?, ?, ?)",
            (return_no, delivery_no, return_date, fine)
        )

        # Clear entry widgets
        self.ent_return_no.delete(0, tk.END)
        self.delivery_var.set('')
        self.ent_return_date.delete(0, tk.END)
        self.ent_fine.delete(0, tk.END)

        # Commit changes to the database
        conn.commit()

        messagebox.showinfo("Success", "Return added successfully.")

    def del_return(self):
        # Get return number to delete
        return_no = self.ent_return_no.get()

        # Delete return from the returns table
        c.execute("DELETE FROM returns WHERE return_no=?", (return_no,))

        # Clear entry widgets
        self.ent_return_no.delete(0, tk.END)
        self.delivery_var.set('')
        self.ent_return_date.delete(0, tk.END)
        self.ent_fine.delete(0, tk.END)

        # Commit changes to the database
        conn.commit()

        messagebox.showinfo("Success", "Return deleted successfully.")

    def display_returns(self):
        # Fetch all returns from the returns table
        c.execute("SELECT * FROM returns")
        returns = c.fetchall()

        # Create a new window to display returns
        returns_window = tk.Toplevel(self)
        returns_window.title("Returns")
        returns_window.geometry("400x400")

        # Create a scrollbar
        scrollbar = tk.Scrollbar(returns_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox with scrollbar
        listbox = tk.Listbox(returns_window, yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)

        # Configure the scrollbar
        scrollbar.config(command=listbox.yview)

        # Insert returns into listbox
        for ret in returns:
            listbox.insert(tk.END, f"Return No: {ret[1]} | Delivery No: {ret[2]} | Return Date: {ret[3]} | Fine: {ret[4]}")

    def quit_app(self):
        # Close the database connection
        conn.close()
        self.destroy()


# Create and run the ReturnApp instance
if __name__ == '__main__':
    app = ReturnApp()
    app.protocol("WM_DELETE_WINDOW", app.quit_app)
    app.mainloop()

