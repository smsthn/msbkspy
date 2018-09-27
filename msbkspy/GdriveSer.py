from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GdriveSer:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile('mycrid.txt')
        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()
        self.gauth.SaveCredentialsFile('mycrid.txt')

        self.drive = GoogleDrive(self.gauth)

    def uploadfile(self,filepath, filename):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        found = False
        for f in file_list:
            if f['title'] == filename :
                f.Delete()
                f2 = self.drive.CreateFile()
                f2.SetContentFile(filepath)
                f2['title'] = filename
                f2.Upload()
                found = True
        if not found:
            f2 = self.drive.CreateFile()
            f2.SetContentFile(filepath)
            f2['title'] = filename
            f2.Upload()
    
    def downloadfile(self,filepath, filename):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        found = False
        thefile = None
        for f in file_list:
            if f['title'] == filename :
                found = True
                import os
                if os.path.isfile(filepath):
                    os.remove(filepath)
                thefile = f.GetContentFile(filepath)
                break
        if not found:
            raise ValueError('sdasda')
        