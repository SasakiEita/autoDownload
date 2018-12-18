from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import mimetypes, os

gauth = GoogleAuth()
gauth.CommandLineAuth()
# gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

def G_upload(path):
    title = os.path.basename(path)
    f = drive.CreateFile({'title': title, 'mimeType': mimetypes.guess_type(title)})
    f.SetContentFile(path)
    f.Upload()
    print(os.getcwd())

def G_makeFolder(title):
    f = drive.CreateFile({'title': title, 'mimeType': 'application/vnd.google-apps.folder'})
    f.Upload()

def G_fileExist(title):
    file_list = drive.ListFile().GetList()
    for f in file_list:
        if title == f['title']:
            return True
        return False

def G_listFiles():
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print ('title: %s, id: %s' % (file1['title'], file1['id']))
    return
