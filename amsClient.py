import tkinter as tk
from PIL import ImageTk, Image


class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.geometry("600x450+345+17")
        self.title("Attendance Management System")
        self.resizable(0,0)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (mainWindow, registerWindow, fpWindow):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(mainWindow)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class mainWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)



class registerWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



class fpWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

app = GUI()
app.mainloop()
