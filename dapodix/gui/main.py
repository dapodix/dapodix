import tkinter as tk
from dapodik import Dapodik
from typing import Optional

from . import LoginFrame


class MainApplication(tk.Frame):
    def __init__(self, master=None, cnf=None, **kw):
        super().__init__(master=master, cnf=cnf if cnf else {}, **kw)
        self.dapodik: Optional[Dapodik] = None
        self.login = LoginFrame(self, cnf=cnf)
        self.login.pack(side="right", fill="both", expand=True)

    def on_login(self):
        self.dapodik = self.login.dapodik()
