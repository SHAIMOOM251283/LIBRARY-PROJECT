import tkinter as tk
import sqlite3

from tkinter import ttk

# Create a connection to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create a table to store book information
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY, title TEXT, author TEXT, genre TEXT)''')

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Library Catalogue")
        self.geometry("394x200")

        # Create labels and entry widgets
        self.lbl_id = tk.Label(self, text="Book ID:")
        self.ent_id = tk.Entry(self, width=55)

        self.lbl_title = tk.Label(self, text="Title:")
        self.ent_title = tk.Entry(self, width=55)

        self.lbl_author = tk.Label(self, text="Author:")
        self.ent_author = tk.Entry(self, width=55)

        self.lbl_genre = tk.Label(self, text="Genre:")
        self.ent_genre = tk.Entry(self, width=55)

        # Add book button
        self.add_book_btn = tk.Button(self, text="Add Book", command=self.add_book)

        # Delete book button
        self.del_book_btn = tk.Button(self, text="Delete Book", command=self.del_book)

        # Display all books button
        self.display_all_btn = tk.Button(self, text="Display Books", command=self.display_books)

        # Set grid layout
        self.lbl_id.grid(row=0, column=0)
        self.ent_id.grid(row=0, column=1, columnspan=2)

        self.lbl_title.grid(row=1, column=0)
        self.ent_title.grid(row=1, column=1, columnspan=2)

        self.lbl_author.grid(row=2, column=0)
        self.ent_author.grid(row=2, column=1, columnspan=2)

        self.lbl_genre.grid(row=3, column=0)
        self.ent_genre.grid(row=3, column=1, columnspan=2)

        self.add_book_btn.grid(row=4, column=2, sticky="E")
        self.del_book_btn.grid(row=5, column=2, sticky="E")
        self.display_all_btn.grid(row=6, column=2, sticky="E")

    def add_book(self):
        # Get values from entry widgets
        book_id = self.ent_id.get()
        title = self.ent_title.get()
        author = self.ent_author.get()
        genre = self.ent_genre.get()

        # Insert values into books table
        c.execute("INSERT INTO books (id, title, author, genre) VALUES (?, ?, ?, ?)", (book_id, title, author, genre))

        # Clear entry widgets
        self.ent_id.delete(0, tk.END)
        self.ent_title.delete(0, tk.END)
        self.ent_author.delete(0, tk.END)
        self.ent_genre.delete(0, tk.END)

        # Commit changes to the database
        conn.commit()

    def del_book(self):
        # Get book ID to delete
        book_id = self.ent_id.get()

        # Delete book from books table
        c.execute("DELETE FROM books WHERE id=?", (book_id,))

        # Clear entry widgets
        self.ent_id.delete(0, tk.END)
        self.ent_title.delete(0, tk.END)
        self.ent_author.delete(0, tk.END)
        self.ent_genre.delete(0, tk.END)

        # Commit changes to the database
        conn.commit()

    def display_books(self):
        # Fetch all books from books table
        c.execute("SELECT * FROM books")
        books = c.fetchall()

        # Create a new window to display books
        books_window = tk.Toplevel(self)
        books_window.title("Library Catalogue")
        books_window.geometry("460x300")

        # Create a frame to hold the scrolled listbox and scrollbar
        frame = ttk.Frame(books_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrolled listbox
        listbox = tk.Listbox(frame)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the listbox to use the scrollbar
        listbox.config(yscrollcommand=scrollbar.set)

        # Insert books into listbox
        for book in books:
            listbox.insert(tk.END, f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Genre: {book[3]}")

        # Configure the scrollbar to work with the listbox
        scrollbar.config(command=listbox.yview)

    def destroy(self):
        # Close the database connection
        conn.close()
        super().destroy()

# Create and run the LibraryApp instance
if __name__ == '__main__':
    app = LibraryApp()
    app.mainloop()

