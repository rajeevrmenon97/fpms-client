#!bin/python
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from utils import fpms
import threading
from multiprocessing import Queue

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

        self.controller = controller

        font = "-family Impact -size 20 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

        self.verifyButton = tk.Button(self, command=self.verify )
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
        self.threadQueue = Queue()

        self.matchedID = ""
        self.matchedName = ""


    def checkRead(self):
        if self.threadQueue.empty():
            self.after(100, self.checkRead)
        else:
            ret = self.threadQueue.get(0)
            if ret is -1:
                tk.messagebox.showinfo("Error", "Scanner error")
            elif ret is -2:
                tk.messagebox.showinfo("Error", "Database error!")
            elif ret is -3:
                tk.messagebox.showinfo("Error", "No matching fingerprint found!")
            elif ret is -4:
                tk.messagebox.showinfo("Error", "Matching error!")
            elif ret is 0:
                tk.messagebox.showinfo("Success", "Fingerprint read for " + self.matchedName)
            self.controller.show_frame(mainWindow)

    def verifyAttendance(self):
        ret = fpObj.markAttendance()
        if ret is -1:
            self.threadQueue.put(-1)
        elif ret is -2:
            self.threadQueue.put(-2)
        elif ret is -3:
            self.threadQueue.put(-3)
        elif ret is -4:
            self.threadQueue.put(-4)
        else:
            self.threadQueue.put(0)
            self.matchedID = fpObj.matchedID
            self.matchedName = fpObj.matchedName

    def verify(self):
        self.matchedID = ""
        self.matchedName = ""
        self.new_thread = threading.Thread(target=self.verifyAttendance)
        self.new_thread.start()
        self.after(100, self.checkRead)
        self.controller.show_frame(fpWindow)





class registerWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        font = "-family Impact -size 15 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

        self.rollno = tk.Entry(self)
        self.rollno.place(relx=0.3, rely=0.25,height=40, relwidth=0.41)
        self.rollno.configure(background="white")
        self.rollno.configure(font="TkFixedFont")
        self.rollno.configure(width=246)

        self.name = tk.Entry(self)
        self.name.place(relx=0.3, rely=0.4,height=40, relwidth=0.41)
        self.name.configure(background="white")
        self.name.configure(font="TkFixedFont")
        self.name.configure(selectbackground="#c4c4c4")

        self.phone = tk.Entry(self)
        self.phone.place(relx=0.3, rely=0.53,height=40, relwidth=0.41)
        self.phone.configure(background="white")
        self.phone.configure(font="TkFixedFont")
        self.phone.configure(selectbackground="#c4c4c4")

        self.email = tk.Entry(self)
        self.email.place(relx=0.3, rely=0.67,height=40, relwidth=0.41)
        self.email.configure(background="white")
        self.email.configure(font="TkFixedFont")
        self.email.configure(selectbackground="#c4c4c4")

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

        self.registerButton = tk.Button(self, command=self.getFingerprint)
        self.registerButton.place(relx=0.2, rely=0.82, height=46, width=147)
        self.registerButton.configure(activebackground="#d9d9d9")
        self.registerButton.configure(text='''Register''')
        self.registerButton.configure(width=147)

        self.backButton = tk.Button(self, command=lambda: controller.show_frame(mainWindow))
        self.backButton.place(relx=0.6, rely=0.82, height=46, width=147)
        self.backButton.configure(activebackground="#d9d9d9")
        self.backButton.configure(text='''Back''')
        self.backButton.configure(width=147)

        self.threadQueue = Queue()


    def checkRead(self):
        if self.threadQueue.empty():
            self.after(100, self.checkRead)
        else:
            ret = self.threadQueue.get(0)
            if ret is -1:
                tk.messagebox.showinfo("Error", "Scanner error")
            elif ret >= 0:
                tk.messagebox.showinfo("Success", "Fingerprint " + str(ret) + "/5 read!")

            if ret is 5:
                fpObj.combineTemplates()
                fpObj.register(
                                self.rollno.get(),
                                self.name.get(),
                                self.phone.get(),
                                self.email.get(),
                                "temp/temp.xyt"
                                )
                tk.messagebox.showinfo("Success", "Inserted Data")
                fpObj.getFingerprintData()
                self.controller.show_frame(mainWindow)
            elif ret >= 0:
                self.getFingerprint(self.fpCount)


    def scanFingerprint(self):
        ret = fpObj.getFingerprint("temp" + str(self.fpCount))
        if ret is -1:
            self.threadQueue.put(-1)
        else:
            self.threadQueue.put(self.fpCount)
            self.fpCount = self.fpCount + 1

    def getFingerprint(self, count=1):
        self.fpCount = count
        self.new_thread = threading.Thread(target=self.scanFingerprint)
        self.new_thread.start()
        self.after(100, self.checkRead)
        self.controller.show_frame(fpWindow)

class fpWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        font = "-family Impact -size 15 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

        image = Image.open("scan.png")
        image = image.resize((100,100),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.fpImage = tk.Label(self,image=photo)
        self.fpImage.image = photo
        self.fpImage.place(relx=0.4, rely=0.22)

        self.title = tk.Message(self)
        self.title.place(relx=0.15, rely=0.55, relheight=0.2, relwidth=0.69)
        self.title.configure(font=font)
        self.title.configure(text='''Place your finger on scanner''')
        self.title.configure(width=413)

        self.backButton = tk.Button(self, command=lambda: controller.show_frame(mainWindow))
        self.backButton.place(relx=0.37, rely=0.82, height=46, width=147)
        self.backButton.configure(activebackground="#d9d9d9")
        self.backButton.configure(text='''Home''')
        self.backButton.configure(width=147)




if __name__ == "__main__":
    global fpObj
    fpObj = fpms()
    if fpObj.getFingerprintData() is -1:
        tk.messagebox.showinfo("Error", "Sorry, error occured while connecting")
    app = GUI()
    app.mainloop()
