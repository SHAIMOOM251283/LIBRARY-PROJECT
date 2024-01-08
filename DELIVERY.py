import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk

# Create a connection to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS delivery
             (id INTEGER PRIMARY KEY, delivery_no TEXT, order_no TEXT, delivery_date TEXT,
             FOREIGN KEY (order_no) REFERENCES orders (order_no))''')


class DeliveryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Delivery Management")
        self.geometry("420x160")

        # Create labels and entry widgets
        self.lbl_delivery_no = tk.Label(self, text="Delivery No:")
        self.ent_delivery_no = tk.Entry(self, width=55)

        self.lbl_order_no = tk.Label(self, text="Order No:")
        self.order_var = tk.StringVar(self)
        self.combo_order = ttk.Combobox(self, textvariable=self.order_var, values=self.get_orders(), width=52)

        self.lbl_delivery_date = tk.Label(self, text="Delivery Date:")
        self.ent_delivery_date = tk.Entry(self, width=55)

        # Add delivery button
        self.add_delivery_btn = tk.Button(self, text="Add Delivery", command=self.add_delivery)

        # Delete delivery button
        self.del_delivery_btn = tk.Button(self, text="Delete Delivery", command=self.del_delivery)

        # Display all deliveries button
        self.display_all_btn = tk.Button(self, text="Display Deliveries", command=self.display_deliveries)

        # Set grid layout
        self.lbl_delivery_no.grid(row=0, column=0)
        self.ent_delivery_no.grid(row=0, column=1, columnspan=2)

        self.lbl_order_no.grid(row=1, column=0)
        self.combo_order.grid(row=1, column=1, columnspan=2)

        self.lbl_delivery_date.grid(row=2, column=0)
        self.ent_delivery_date.grid(row=2, column=1, columnspan=2)

        self.add_delivery_btn.grid(row=3, column=2, sticky="E")
        self.del_delivery_btn.grid(row=4, column=2, sticky="E")
        self.display_all_btn.grid(row=5, column=2, sticky="E")

    def get_orders(self):
        # Retrieve order numbers from the database
        c.execute("SELECT order_no FROM orders")
        orders = c.fetchall()
        orders_list = [order[0] for order in orders]
        return orders_list

    def add_delivery(self):
        # Get values from entry widgets
        delivery_no = self.ent_delivery_no.get()
        order_no = self.order_var.get()
        delivery_date = self.ent_delivery_date.get()

        # Validate input
        if not delivery_no or not order_no or not delivery_date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Insert values into the delivery table
        c.execute(
            "INSERT INTO delivery (delivery_no, order_no, delivery_date) VALUES (?, ?, ?)",
            (delivery_no, order_no, delivery_date)
        )

        # Clear entry widgets
        self.ent_delivery_no.delete(0, tk.END)
        self.order_var.set('')
        self.ent_delivery_date.delete(0, tk.END)

        # Commit changes to the database
        conn.commit()

        messagebox.showinfo("Success", "Delivery added successfully.")

    def del_delivery(self):
        # Get delivery number to delete
        delivery_no = self.ent_delivery_no.get()

        # Delete delivery from the delivery table
        c.execute("DELETE FROM delivery WHERE delivery_no=?", (delivery_no,))

        # Clear entry widgets
        self.ent_delivery_no.delete(0, tk.END)
        self.order_var.set('')
        self.ent_delivery_date.delete(0, tk.END)

        # Commit changes to the database
        conn.commit()

        messagebox.showinfo("Success", "Delivery deleted successfully.")

    def display_deliveries(self):
        # Fetch all deliveries from the delivery table
        c.execute("SELECT * FROM delivery")
        deliveries = c.fetchall()

        # Create a new window to display deliveries
        deliveries_window = tk.Toplevel(self)
        deliveries_window.title("Deliveries")
        deliveries_window.geometry("340x400")

        # Create a scrollbar
        scrollbar = tk.Scrollbar(deliveries_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox with scrollbar
        listbox = tk.Listbox(deliveries_window, yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)

        # Configure the scrollbar
        scrollbar.config(command=listbox.yview)

        # Insert deliveries into listbox
        for delivery in deliveries:
            listbox.insert(tk.END, f"Delivery No: {delivery[1]} | Order No: {delivery[2]} | Delivery Date: {delivery[3]}")

    def quit_app(self):
        # Close the database connection
        conn.close()
        self.destroy()


# Create and run the DeliveryApp instance
if __name__ == '__main__':
    app = DeliveryApp()
    app.protocol("WM_DELETE_WINDOW", app.quit_app)
    app.mainloop()

