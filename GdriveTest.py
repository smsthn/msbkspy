from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import  client, tools
from oauth2client import file as fff
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile('mycrid.txt')
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile('mycrid.txt')

    drive = GoogleDrive(gauth)
    dddfile = '/home/smsthn/Downloads/ddd.dat'
    dddfilename = 'ddd.dat'
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    found = False
    for f in file_list:
        if f['title'] == dddfilename :
            f.Delete()
            f2 = drive.CreateFile()
            f2.SetContentFile(dddfile)
            f2['title'] = dddfilename
            f2.Upload()
            found = True
            print('was found')
    if not found:
        f2 = drive.CreateFile()
        f2.SetContentFile(dddfile)
        f2['title'] = dddfilename
        f2.Upload()
        print('was not found')


    
    

if __name__ == '__main__':
    main()