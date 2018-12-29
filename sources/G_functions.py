from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import mimetypes, os

gauth = GoogleAuth()
gauth.CommandLineAuth()
# gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

class Course():
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.id = ''

    def __str__(self):
        return self.title

    def makeFolder(self):
            f = drive.CreateFile({'title': self.title, 'mimeType': 'application/vnd.google-apps.folder'})
            f.Upload()
            self.id = f['id']
            print('course: {}'.format(self.title))
            print('made folderID: {}'.format(self.id))
            return self.id

    def existFolder(self):
        print('course: {}'.format(self.title))
        print("exsit folder check: {}".format(self.id))
        if not self.id:
            print("{} has no id".format(self.title))
            return False
        else:
            file_list = drive.ListFile().GetList()
            for f in file_list:
                if self.id == f['id']:
                    print('course: {}'.format(self.title))
                    print("same id folder found")
                    return f['id']
            print("There is no folder to {}".format(self.title))
            print("ID: {}".format(self.id))
            return False

class LectureDoc():
    def __init__(self,path,course):
        self.title = os.path.basename(path)
        self.path = path
        self.course = course
        self.id = ''

    def __str__(self):
        return self.title

    def upload(self):
        if not self.course.existFolder():
            self.course.makeFolder()
        f = drive.CreateFile({'title': self.title, 'mimeType': mimetypes.guess_type(self.title), 'parents': [{'id': self.course.id}]})
        f.SetContentFile(self.path)
        f.Upload()
        self.id = f['id']
        return self.id
