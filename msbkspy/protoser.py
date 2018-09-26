import newMsBooksProto_pb2 as mspb
import books as msbks
import sys


class protoser:


    @staticmethod
    def derserialize(path):
        books = msbks.Books()

        srbooks = mspb.Books()
        f = open(path,'rb')
        srbooks.ParseFromString(f.read())
        for srbook in srbooks.AllBooks:
            name = srbook.name
            catagory = str(srbook.catagory)
            readingstatus = str(srbook.readingStatus)
            pages = srbook.pages
            tags = []
            for tag in srbook.tags:
                tags.append(str(tag))
            notes = srbook.notes
            book = msbks.Book(name,pages,catagory,readingstatus,tags,notes)
            books.AllBooks.append(book)
        for tag in srbooks.AllTags:
            books.AllTags.append(str(tag))
        for rdstts in srbooks.AllReadingStatus:
            books.AllReadingStatus.append(str(rdstts))
        for ctg in srbooks.AllCatagories:
            books.AllCatagories.append(str(ctg))
        return books
    
    @staticmethod
    def serialize(path, books):
        srbooks = mspb.Books()
        
        for book in books.AllBooks:
            name = book.Name
            ctg = book.Catagory
            rdstts = book.ReadingStatus
            tgs = book.Tags
            pages = book.Pages
            notes = book.Notes
            srbook = srbooks.AllBooks.add()
            srbook.name = name
            srbook.catagory = ctg
            srbook.readingStatus = rdstts
            srbook.pages = pages
            srbook.tags.extend(book.Tags)
            srbook.notes.extend(book.Notes)
            #srbooks.AllBooks.append(srbook)
        srbooks.AllTags.extend(books.AllTags)
        srbooks.AllReadingStatus.extend(books.AllReadingStatus)
        srbooks.AllCatagories.extend(books.AllCatagories)
        f = open(path,'wb')
        f.write(srbooks.SerializeToString())
        f.close()