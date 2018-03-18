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

        font = "-family Impact -size 20 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

        self.verifyButton = tk.Button(self, command=lambda: controller.show_frame(fpWindow))
        self.verifyButton.place(relx=0.33, rely=0.33, height=86, width=177)
        self.verifyButton.configure(activebackground="#d9d9d9")
        self.verifyButton.configure(text='''Verify''')
        self.verifyButton.configure(width=177)

        self.registerButton = tk.Button(self, command=lambda: controller.show_frame(registerWindow))
        self.registerButton.place(relx=0.33, rely=0.62, height=86, width=177)
        self.registerButton.configure(activebackground="#d9d9d9")
        self.registerButton.configure(text='''Register''')

        self.title = tk.Message(self)
        self.title.place(relx=0.03, rely=0.11, relheight=0.13, relwidth=0.94)
        self.title.configure(font=font)
        self.title.configure(text='''Attendance Management System''')
        self.title.configure(width=563)



class registerWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



class fpWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

app = GUI()
app.mainloop()
