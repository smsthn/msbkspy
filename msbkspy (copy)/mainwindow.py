#!/usr/bin/env python

import tkinter as tk
from tkinter import filedialog
from mslistbox import MsListBox
from protoser import protoser
from books import Books, Book
from configparser import SafeConfigParser
import os.path
import addwindows


class mainwindow:
    books = Books()
    currentcatagory = 'Any'
    currentreadingstatus = 'Any'
    currenttags = []
    booksearchtext = ''

    def __init__(self):
        #labels and listboxes
        self.root = tk.Tk()
        self.root.title("Counting Seconds")
        self.root.geometry("900x600")
        self.ctglabel = tk.Label(self.root, text='Catagories').grid(
            row=0, column=0, padx=10, pady=10)
        self.ctglabel
        self.rdsttslabel = tk.Label(self.root, text='ReadingStatus')
        self.rdsttslabel.grid(row=0, column=1, padx=10, pady=10)
        self.tagsLabel = tk.Label(self.root, text='Tags')
        self.tagsLabel.grid(row=0, column=2, padx=10, pady=10)
        self.booksLabel = tk.Label(self.root, text='Books')
        self.booksLabel.grid(row=2, column=1, padx=10, pady=10)

        self.ctglb = tk.Listbox(self.root, exportselection=False)
        self.ctglb.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.rdsttslb = tk.Listbox(self.root, exportselection=False)
        self.rdsttslb.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        self.tgslb = tk.Listbox(
            self.root, selectmode="multiple", exportselection=False)
        self.tgslb.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
        self.bkssearch = tk.Entry(self.root)
        self.bkssearch.grid(row=2, column=1, padx=30, pady=10, sticky='nsew')
        self.bkslb = tk.Listbox(self.root, exportselection=False)
        self.bkslb.grid(row=3, column=1, padx=30, pady=10, sticky='nsew')

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        self.root.rowconfigure(3, weight=1)
        # end labels and listboxes

        self.btnframe = tk.Frame(self.root)
        self.addbtn = tk.Button(
            self.btnframe, justify="center", text='Add', command=self.createaddwindow)
        self.addbtn.grid(row=1, column=1, padx=10, pady=10, sticky='we')
        self.removebtn = tk.Button(
            self.btnframe, justify="center", text='Remove')
        self.removebtn.grid(row=2, column=1, padx=10, pady=10, sticky='we')
        self.savebtn = tk.Button(
            self.btnframe, justify="center", text='Save', command=self.saveevent)
        self.savebtn.grid(row=3, column=1, padx=10, pady=10, sticky='we')
        self.editbtn = tk.Button(
            self.btnframe, justify="center", text='Edit', command=self.createmodifywindow)
        self.editbtn.grid(row=4, column=1, padx=10, pady=10, sticky='we')
        self.loadbtn = tk.Button(
            self.btnframe, justify="center", text='Load', command=self.msOpenFile)
        self.loadbtn.grid(row=5, column=1, padx=10, pady=10, sticky='we')
        self.btnframe.grid(row=3, column=0)
        self.btnframe.columnconfigure(0, weight=1)
        self.btnframe.columnconfigure(1, weight=1)
        self.btnframe.columnconfigure(2, weight=1)
    # btnframe.place(anchor='center',)
        self.addeventlisteners()
        self.tryloadfileonstartup()
        self.root.mainloop()

    def addeventlisteners(self):
        self.ctglb.bind("<<ListboxSelect>>", self.catagoryselectedevent)
        self.rdsttslb.bind("<<ListboxSelect>>",
                           self.readingstatusselectedevent)
        self.tgslb.bind("<<ListboxSelect>>", self.tagsselectedevent)
        self.bkslb.bind('<Double-Button-1>', self.createmodifywindowdblclk)
        self.bkssearch.bind('<Key>', self.bookssearchevent)
        self.bkssearch.bind('<FocusIn>', self.bookssearchgotfocus)
        self.bkssearch.bind('<BackSpace>', self.bookssearchbackspace)

    def bookssearchevent(self, event):
        self.booksearchtext += event.char
        self.getbooks()

    def bookssearchgotfocus(self, event):
        self.booksearchtext = ''
        self.bkssearch.delete(0, tk.END)
        self.getbooks()

    def bookssearchbackspace(self, event):
        self.booksearchtext = self.bkssearch.get()
        # self.bkssearch.config(text=self.booksearchtext)
        self.getbooks()

    def catagoryselectedevent(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        self.currentcatagory = w.get(index)
        self.getbooks()

    def readingstatusselectedevent(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        self.currentreadingstatus = w.get(index)
        self.getbooks()

    def tagsselectedevent(self, evt):
        w = evt.widget
        indexs = w.curselection()
        self.currenttags.clear()
        for i in indexs:
            self.currenttags.append(w.get(int(i)))

        self.getbooks()

    def getbooks(self):
        books = self.books.get_filtered_books_list(
            name=self.booksearchtext, catagory=self.currentcatagory, readingstatus=self.currentreadingstatus, tags=self.currenttags)
        self.bkslb.delete(0, tk.END)
        for book in books:
            self.bkslb.insert(tk.END, book.Name)

    def tryloadfileonstartup(self):
        config = SafeConfigParser()
        if not os.path.isfile('config.ini'):
            return
        config.read('config.ini')
        if not config.has_section('path'):
            return

        filename = config.get('path', 'prevopenpath')
        self.books = protoser.derserialize(filename)
        for ctg in self.books.AllCatagories:
            self.ctglb.insert(tk.END, ctg)
        for rdstts in self.books.AllReadingStatus:
            self.rdsttslb.insert(tk.END, rdstts)
        for tag in self.books.AllTags:
            self.tgslb.insert(tk.END, tag)
        for book in self.books.AllBooks:
            self.bkslb.insert(tk.END, book.Name)

    def createaddwindow(self):
        self.addwnd = addwindows.AddWindows(
            self.root, self, 'Add Book', self.books.AllCatagories, self.books.AllReadingStatus, self.books.AllTags)

    def createmodifywindowdblclk(self, event):
        if not self.bkslb.curselection():
            return
        book = next((bk for bk in self.books.AllBooks if bk.Name ==
                     self.bkslb.get(self.bkslb.curselection()[0])), None)
        self.addwnd = addwindows.AddWindows(
            self.root, self, 'Add Book', self.books.AllCatagories, self.books.AllReadingStatus, self.books.AllTags, book)

    def createmodifywindow(self):
        if not self.bkslb.curselection():
            return
        book = next((bk for bk in self.books.AllBooks if bk.Name ==
                     self.bkslb.get(self.bkslb.curselection()[0])), None)
        self.addwnd = addwindows.AddWindows(
            self.root, self, 'Add Book', self.books.AllCatagories, self.books.AllReadingStatus, self.books.AllTags, book)

    def saveevent(self):
        filename = filedialog.asksaveasfilename(
            initialdir="/home/smsthn/Downloads/", title='Save', filetypes=(('Dat Files', "*.dat"),))
        protoser.serialize(filename, self.books)
        if not os.path.isfile('config.ini'):
            f = open('config.ini', 'w+')
            f.close()
        config = SafeConfigParser()
        config.read('config.ini')
        if not config.has_section('path'):
            config.add_section('path')
        config.set('path', 'prevsavepath', filename)
        with open('config.ini', 'w') as f:
            config.write(f)

    def autoSaveevent(self):
        if self.books.AllBooks:
            config = SafeConfigParser()
            if not os.path.isfile('config.ini'):
                return
            config.read('config.ini')

            if not config.has_section('path'):
                return
            if not config.has_option('path', 'prevsavepath'):
                return
            filename = config.get('path', 'prevsavepath')
            protoser.serialize(filename, self.books)

    def removeevent(self):
        book = next((bk for bk in self.books.AllBooks if bk.Name ==
                     self.bkslb.get(self.bkslb.curselection()[0])), None)
        if book == None:
            return
        self.books.AllBooks.remove(book)
        self.getbooks()
        self.autoSaveevent()

    def msOpenFile(self):
        filename = filedialog.askopenfilename(
            initialdir="/home/smsthn/Downloads/", title='Open', filetypes=(('Dat Files', "*.dat"),))
        if not os.path.isfile('config.ini'):
                f = open('config.ini', 'w+')
                f.close()
        config = SafeConfigParser()
        config.read('config.ini')
        if not config.has_section('path'):
            config.add_section('path')
        config.set('path', 'prevopenpath', filename)
        with open('config.ini', 'w') as f:
            config.write(f)

        del self.books.AllBooks[:]
        del self.books.AllCatagories[:]
        del self.books.AllReadingStatus[:]
        del self.books.AllTags[:]
        books = protoser.derserialize(filename)
        self.books.AllBooks.extend(books.AllBooks)
        self.books.AllCatagories.extend(books.AllCatagories)
        self.books.AllReadingStatus.extend(books.AllReadingStatus)
        self.books.AllTags.extend(books.AllTags)
        self.ctglb.delete(0, tk.END)
        for ctg in self.books.AllCatagories:
            self.ctglb.insert(tk.END, ctg)
        self.rdsttslb.delete(0, tk.END)
        for rdstts in self.books.AllReadingStatus:
            self.rdsttslb.insert(tk.END, rdstts)
        self.tgslb.delete(0, tk.END)
        for tag in self.books.AllTags:
            self.tgslb.insert(tk.END, tag)
        self.bkslb.delete(0, tk.END)
        for book in self.books.AllBooks:
            self.bkslb.insert(tk.END, book.Name)


window = mainwindow()
