from tkinter import *
from tkinter.ttk import *
from books import *

class AddWindows(Toplevel):
    def __init__(self,main,mainwindow,title,catagorieslsit,readingstatuslist,tagslist,book =None):
        Toplevel.__init__(self,main)
        self.main = mainwindow
        self.catagory = 'Any'
        self.readingstatus = 'Any'
        self.tags = []
        #self.pages=0

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=0)
        self.rowconfigure(5,weight=1)
        

        self.minsize(460 , 320)
        self.title(title)
        #self.config(bg='white')
        self.namelabel = Label(self,text='Name',font=("Courier", 16,'bold'))
        self.namelabel.grid(row=0,column=0,padx=15,pady=15)
        self.catagorylabel = Label(self,text='Catagory',font=("Courier", 16,'bold'))
        self.catagorylabel.grid(row=1,column=0,padx=15,pady=15)
        self.readingstatuslabel = Label(self,text='ReadingStatus',font=("Courier", 16,'bold'))
        self.readingstatuslabel.grid(row=2,column=0,padx=15,pady=15)
        self.tagslabel = Label(self,text='Tags',font=("Courier", 16,'bold'))
        self.tagslabel.grid(row=3,column=0,padx=15,pady=15)
        self.pageslabel =Label(self,text='Pages',font=("Courier", 16,'bold'))
        self.pageslabel.grid(row=4,column=0,padx=15,pady=15)

        self.name = StringVar()
        self.nametxtbx = Entry(self,textvariable=self.name)
        self.nametxtbx.grid(row=0,column=1,padx=15,pady=15,sticky='nsew')
        self.ctg = StringVar()
        self.ctgcmbo = Combobox(self,state="readonly", values =catagorieslsit)
        
        self.ctgcmbo.grid(row=1,column=1,padx=15,pady=15,sticky='nsew')
        self.rdsttscmbo = Combobox(self,state="readonly", values =readingstatuslist)
        
        self.rdsttscmbo.grid(row=2,column=1,padx=15,pady=15,sticky='nsew')
        

        self.pages = IntVar()
        self.pagesspin = Spinbox(self,from_=0,to=2000,textvariable=self.pages)
        self.pagesspin.grid(row=4,column=1,padx=15,pady=15,sticky='nsew')

        self.frame = Frame(self)
        self.frame.grid(row=5,column=1,columnspan=2,padx=15,pady=15)
        self.cancelbtn = Button(self.frame,text='Cancel',command=self.cancelevnt)
        self.cancelbtn.pack(anchor='e',side='right')
        
        self.tgframe = Frame(self)
        self.tgframe.grid(row=3,column=3)
        self.tagsaddbtn =Button(self.tgframe,text='+',width=1,command=self.addtagevent)
        self.tagsaddbtn.pack(side='right')
        self.tagsremovebtn =Button(self.tgframe,text='-',width=1)
        self.tagsremovebtn.pack(side='right')

        self.tgsdrop = Listbox(self,height=2,selectmode=MULTIPLE,exportselection=False)
        #self.tgsdrop.set('1')
        for tag in tagslist:
            self.tgsdrop.insert(END,tag)
        self.tgsdrop.grid(row=3,column=1,padx=15,pady=15,sticky='ew')

        self.ctgcmbo.bind("<<ComboboxSelected>>",self.ctgselectevent)
        self.rdsttscmbo.bind("<<ComboboxSelected>>",self.rdsttsselectevent)
        self.tgsdrop.bind("<<ListboxSelect>>",self.tgsselectevent)
        self.tgsdrop.bind('<Enter>',self.tagsmouseenterevent)
        self.tgsdrop.bind('<Leave>',self.tagsmouseleaveevent)

        style = Style()
        style.map('TCombobox', fieldbackground=[('readonly','white')])
        style.map('TCombobox', selectbackground=[('readonly','grey')])
        
        if book == None:
            self.ctgcmbo.set(catagorieslsit[0])
            self.rdsttscmbo.set(readingstatuslist[0])
            self.addbtn = Button(self.frame,text='Add',command=self.addbookevent)
            self.addbtn.pack(anchor='e',side='right')
            
            
        else:
            self.book = book
            self.name.set(book.Name)
            self.catagory =book.Catagory
            self.readingstatus = book.ReadingStatus
            self.pages.set(book.Pages)
            self.tags = book.Tags
            self.ctgcmbo.set(book.Catagory)
            self.rdsttscmbo.set(book.ReadingStatus)
            self.addbtn = Button(self.frame,text='Modify',command=self.modifybookevent)
            self.addbtn.pack(anchor='e',side='right')
            
            
            
            if book.Tags:
                
                for tg in book.Tags:
                    self.tgsdrop.select_set(tagslist.index(tg))
                
            self.pages.set(book.Pages)
        self.nametxtbx.focus_set()
                
        
    def addbookevent(self):        
        book = Book(self.name.get(),self.pages.get(),self.catagory,self.readingstatus,self.tags)
        self.main.books.AllBooks.append(book)
        self.main.autoSaveevent()
        self.main.getbooks()
        self.destroy()
    def modifybookevent(self):
        #book = next((bk for bk in self.main.books.AllBooks if bk.Name==self.name.get()),None)
        if(self.book == None):
            return
        self.book.Name = self.name.get()
        self.book.Catagory = self.catagory
        self.book.ReadingStatus = self.readingstatus
        self.book.Tags = self.tags
        self.book.Pages = self.pages.get()
        self.main.autoSaveevent()
        self.main.getbooks()
        self.destroy()
    def cancelevnt(self):
        self.destroy()
    def ctgselectevent(self,event):
        self.catagory = self.ctgcmbo.get()
    def rdsttsselectevent(self,event):
        self.readingstatus = self.rdsttscmbo.get()
    def tgsselectevent(self,event):
        w = event.widget
        indexs = w.curselection()
        self.tags.clear()
        for i in indexs:
            self.tags.append(w.get(int(i)))
    def tagsmouseenterevent(self,event):
        self.tgsdrop.grid(row=3,rowspan =3,column=1,padx=15,pady=15,sticky='ew')
        self.tgsdrop.config(height=15)
    def tagsmouseleaveevent(self,event):
        self.tgsdrop.grid(row=3,rowspan =1,column=1,padx=15,pady=15,sticky='ew')
        self.tgsdrop.config(height=2)

    def addtagevent(self):
        self.addtagentry = Entry(self)
        self.addtagentry.grid(row=3,column=1,padx=15,pady=15,sticky='ewsn')
        self.addtagentry.bind('<Return>',self.addtagenter)
        self.addtagentry.bind('<Escape>',self.destroythis)
    def addtagenter(self,event):
            if self.addtagentry.get().strip() == '':
                self.destroythis(event)
                return
            else :
                self.main.books.AllTags.append(self.addtagentry.get())
                self.main.tgslb.insert(END,self.addtagentry.get())
                self.tgsdrop.insert(END,self.addtagentry.get())
                self.destroythis(event)
                
            self.destroythis(event)
    def destroythis(self,event):
            self.addtagentry.destroy()
        
        






