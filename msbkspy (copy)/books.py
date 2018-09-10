


class Book:
   
    def __init__(self,name,pages=0,catagory='Any',readingstatus='Any',tags=[],notes=[]):
        
        self.Name = name
        self.ReadingStatus = readingstatus
        self.Catagory = catagory
        self.Tags = tags
        self.Pages = pages 
        self.Notes = notes

class Books:
    def __init__(self):
        self.AllBooks = []
        self.AllCatagories = []
        self.AllReadingStatus = []
        self.AllTags = []
    
    def containslist(self,main,sub):
        if not sub:
            return True
        for item in sub:
            if item not in main:
                return False
        return True

    def get_filtered_books_list(self ,name = None,catagory = 'Any',readingstatus = 'Any',tags=[]) :
        self.AllBooks = sorted(self.AllBooks,key = lambda bk : bk.Name)
        
        resultlist = []
        for book in self.AllBooks:
            if catagory == 'Any' or catagory == book.Catagory:
                if readingstatus == 'Any' or readingstatus == book.ReadingStatus:
                    if not tags:
                        if name.strip()  == '' or name.strip().lower() in book.Name.lower():
                            resultlist.append(book)
                            continue
                    if self.containslist(book.Tags,tags):
                        if name.strip()  == '' or name.strip().lower() in book.Name.lower():
                            resultlist.append(book)
                            continue
        return resultlist
       