import tkinter as tk
from dapodik import __semester__


class LoginFrame(tk.Frame):
    def __init__(self, master=None, cnf=None, **kw):
        super(LoginFrame, self).__init__(master, cnf=cnf if cnf else {}, **kw)
        self.geometry("400x150")
        self.title("Dapodix Login")
        # Email Form
        self.emailLabel = tk.Label(self, text="Email")
        self.emailLabel.grid(row=0, column=0)
        self.email = tk.StringVar(self)
        self.emailEntry = tk.Entry(self, textvariable=self.email)
        self.emailEntry.grid(row=0, column=1)
        # Password Form
        self.passwordLabel = tk.Label(self, text="Password")
        self.passwordLabel.grid(row=1, column=0)
        self.password = tk.StringVar(self)
        self.passwordEntry = tk.Entry(self, textvariable=self.password, show="*")
        self.passwordEntry.grid(row=1, column=1)
        # Semester Form
        self.semesterLabel = tk.Label(self, text="Semester")
        self.semesterLabel.grid(row=2, column=0)
        self.semester = tk.StringVar(self, value=__semester__)
        self.semesterEntry = tk.Entry(self, textvariable=self.semester)
        self.semesterEntry.grid(row=2, column=1)
        # Server Form
        self.semesterLabel = tk.Label(self, text="Server")
        self.semesterLabel.grid(row=3, column=0)
        self.semester = tk.StringVar(self, value="http://localhost:5774/")
        self.semesterEntry = tk.Entry(self, textvariable=self.semester)
        self.semesterEntry.grid(row=3, column=1)
        # Button
        self.loginButton = tk.Button(self, text="Masuk", command=self.login)
        self.loginButton.grid(row=5, column=0)

    def login(self, email: str, password: str):
        print(f"{email} {password}")
