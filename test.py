from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import mimetypes, os

gauth = GoogleAuth()
gauth.CommandLineAuth()
# gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile().GetList()
for f in file_list:
    print(f['id'])
