import tkinter as tk
import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Library", font=("Jokerman", 27))
        self.title_label.pack(side="top", pady=10)

        self.program1_button = tk.Button(self)
        self.program1_button["text"] = "Library Catalogue"
        self.program1_button["command"] = self.run_program1
        self.program1_button["width"] = 15           # set the width to 10 characters
        self.program1_button["height"] = 1          # set the height to 2 lines
        self.program1_button["fg"] = "black"         # set the font color to blue
        self.program1_button["bg"] = "white"       # set the background color to yellow
        self.program1_button["font"] = ("Comic Sans MS", 12) # set the font to Arial, size 12
        self.program1_button.pack(side="top")

        self.program2_button = tk.Button(self)
        self.program2_button["text"] = "Member Database"
        self.program2_button["command"] = self.run_program2
        self.program2_button["width"] = 15
        self.program2_button["height"] = 1
        self.program2_button["fg"] = "black"
        self.program2_button["bg"] = "white"
        self.program2_button["font"] = ("Comic Sans MS", 12)
        self.program2_button.pack(side="top")

        self.program3_button = tk.Button(self)
        self.program3_button["text"] = "Order"
        self.program3_button["command"] = self.run_program3
        self.program3_button["width"] = 15
        self.program3_button["height"] = 1
        self.program3_button["fg"] = "black"
        self.program3_button["bg"] = "white"
        self.program3_button["font"] = ("Comic Sans MS", 12)
        self.program3_button.pack(side="top")

        self.program4_button = tk.Button(self)
        self.program4_button["text"] = "Delivery"
        self.program4_button["command"] = self.run_program4
        self.program4_button["width"] = 15
        self.program4_button["height"] = 1
        self.program4_button["fg"] = "black"
        self.program4_button["bg"] = "white"
        self.program4_button["font"] = ("Comic Sans MS", 12)
        self.program4_button.pack(side="top")

        self.program5_button = tk.Button(self)
        self.program5_button["text"] = "Return"
        self.program5_button["command"] = self.run_program5
        self.program5_button["width"] = 15
        self.program5_button["height"] = 1
        self.program5_button["fg"] = "black"
        self.program5_button["bg"] = "white"
        self.program5_button["font"] = ("Comic Sans MS", 12)
        self.program5_button.pack(side="top")

        self.quit_button = tk.Button(self) 
        self.quit_button["text"] = "Quit" 
        self.quit_button["command"] = self.master.destroy
        self.quit_button["width"] = 7
        self.quit_button["height"] = 1
        self.quit_button["fg"] = "red"
        self.quit_button["bg"] = "white"
        self.quit_button["font"] = ("Comic Sans MS", 12)
        self.quit_button.pack(side="bottom")

    def run_program1(self):
        file_path = "C:\\Users\\Shaimoom\\Documents\\PYTHON\\PROJECTS\\LIBRARY\\FOURTH\\LIBRARY CATALOGUE.py"
        subprocess.Popen(["python", file_path])

    def run_program2(self):
        file_path = "C:\\Users\\Shaimoom\\Documents\\PYTHON\\PROJECTS\\LIBRARY\\FOURTH\\MEMBER DATABASE.py"
        subprocess.Popen(["python", file_path])

    def run_program3(self):
        file_path = "C:\\Users\\Shaimoom\\Documents\\PYTHON\\PROJECTS\\LIBRARY\\FOURTH\ORDER.py"
        subprocess.Popen(["python", file_path])

    def run_program4(self):
        file_path = "C:\\Users\\Shaimoom\\Documents\\PYTHON\\PROJECTS\\LIBRARY\\FOURTH\\DELIVERY.py"
        subprocess.Popen(["python", file_path])
    
    def run_program5(self):
        file_path = "C:\\Users\\Shaimoom\\Documents\\PYTHON\\PROJECTS\\LIBRARY\\FOURTH\\RETURN.py"
        subprocess.Popen(["python", file_path])

root = tk.Tk()
root.geometry("500x385")
root.configure(bg="sky blue")
app = Application(master=root)
app.mainloop()