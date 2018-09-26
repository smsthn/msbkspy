from tkinter import *
from tkinter import ttk
from books import Book

class BookDetailsFrame(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)

        
        #self.config(bg='white')
        self.namelabel = Label(self,text='Name:',font=("Courier", 10,'bold'),fg='grey',width=14,height=3)
        self.namelabel.grid(row=0,column=0,padx=5,pady=15)
        self.catagorylabel = Label(self,text='Catagory:',font=("Courier", 10,'bold'),fg='grey',width=14,height=1)
        self.catagorylabel.grid(row=1,column=0,padx=5,pady=15)
        self.readingstatuslabel = Label(self,text='ReadingStatus:',font=("Courier", 10,'bold'),fg='grey',width=14,height=1)
        self.readingstatuslabel.grid(row=2,column=0,padx=5,pady=15)
        self.tagslabel = Label(self,text='Tags',font=("Courier:", 10,'bold'),fg='grey',width=14,height=1)
        self.tagslabel.grid(row=3,column=0,padx=5,pady=15)
        self.pageslabel =Label(self,text='Pages',font=("Courier:", 10,'bold'),fg='grey',width=14,height=1)
        self.pageslabel.grid(row=4,column=0,padx=5,pady=15)

        self.name = Text(self,font=("Courier", 10),width=25,height=3)
        self.name.grid(row=0,column=1)
        self.catagory = Text(self,font=("Courier", 10),width=25,height=2)
        self.catagory.grid(row=1,column=1)
        self.readingstatus = Text(self,font=("Courier", 10),width=25,height=2)
        self.readingstatus.grid(row=2,column=1)
        self.tgsdrop = Listbox(self,height=3,selectmode=NONE,bg='#d8d8d8',width=25,font=("Courier", 10))
       
        self.tgsdrop.grid(row=3,column=1)
        self.pages =Text(self,font=("Courier", 10),width=25,height=2)
        self.pages.grid(row=4,column=1)

        
    def addbook(self,book):
        self.name.delete('1.0',END)
        self.name.insert(END,book.Name)
        self.catagory.delete('1.0',END)
        self.catagory.insert(END,book.Catagory)
        self.readingstatus.delete('1.0',END)
        self.readingstatus.insert(END,book.ReadingStatus)
        self.pages.delete('1.0',END)
        self.pages.insert(END,book.Pages)
        self.tgsdrop.delete(0,END)
        for tag in book.Tags:
            self.tgsdrop.insert(END,tag)








#bk = Book(name='names',catagory='ctg',readingstatus='anyyy',tags=['tg1','tg2','tg3','tg4','tg5','tg6'])
#root = Tk()
#
#dt2 = BookDetailsFrame(root)
#dt2.addbook(bk)
#dt2.pack()
#root.mainloop()