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

        font = "-family Impact -size 15 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

        self.rollno = tk.Entry(self)
        self.rollno.place(relx=0.3, rely=0.25,height=40, relwidth=0.41)
        self.rollno.configure(background="white")
        self.rollno.configure(font="TkFixedFont")
        self.rollno.configure(width=246)

        self.email = tk.Entry(self)
        self.email.place(relx=0.3, rely=0.67,height=40, relwidth=0.41)
        self.email.configure(background="white")
        self.email.configure(font="TkFixedFont")
        self.email.configure(selectbackground="#c4c4c4")

        self.phone = tk.Entry(self)
        self.phone.place(relx=0.3, rely=0.53,height=40, relwidth=0.41)
        self.phone.configure(background="white")
        self.phone.configure(font="TkFixedFont")
        self.phone.configure(selectbackground="#c4c4c4")

        self.name = tk.Entry(self)
        self.name.place(relx=0.3, rely=0.4,height=40, relwidth=0.41)
        self.name.configure(background="white")
        self.name.configure(font="TkFixedFont")
        self.name.configure(selectbackground="#c4c4c4")

        self.msgRollno = tk.Message(self)
        self.msgRollno.place(relx=0.12, rely=0.28, relheight=0.04, relwidth=0.17)

        self.msgRollno.configure(text='''Roll Number''')
        self.msgRollno.configure(width=103)

        self.msgName = tk.Message(self)
        self.msgName.place(relx=0.13, rely=0.42, relheight=0.04, relwidth=0.14)
        self.msgName.configure(text='''Name''')
        self.msgName.configure(width=83)

        self.msgPhone = tk.Message(self)
        self.msgPhone.place(relx=0.13, rely=0.56, relheight=0.04, relwidth=0.16)
        self.msgPhone.configure(text='''Phone Number''')
        self.msgPhone.configure(width=93)

        self.msgEmail = tk.Message(self)
        self.msgEmail.place(relx=0.14, rely=0.69, relheight=0.04, relwidth=0.14)
        self.msgEmail.configure(text='''Email ID''')
        self.msgEmail.configure(width=83)

        self.title = tk.Message(self)
        self.title.place(relx=0.37, rely=0.09, relheight=0.07, relwidth=0.25)
        self.title.configure(font=font)
        self.title.configure(text='''Register''')
        self.title.configure(width=150)

        self.registerButton = tk.Button(self)
        self.registerButton.place(relx=0.2, rely=0.82, height=46, width=147)
        self.registerButton.configure(activebackground="#d9d9d9")
        self.registerButton.configure(text='''Register''')
        self.registerButton.configure(width=147)

        self.backButton = tk.Button(self, command=lambda: controller.show_frame(mainWindow))
        self.backButton.place(relx=0.6, rely=0.82, height=46, width=147)
        self.backButton.configure(activebackground="#d9d9d9")
        self.backButton.configure(text='''Back''')
        self.backButton.configure(width=147)



class fpWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

app = GUI()
app.mainloop()
