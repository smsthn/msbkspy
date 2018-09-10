from tkinter import *

class MsListBox:
    @staticmethod
    def createListview(tk,items):
        ctglb = Listbox(tk)
        for item in items:
            ctglb.insert(END, item)
        return ctglb
