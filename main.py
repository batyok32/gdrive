from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import os

# import glob
from pathlib import Path

# CONFIGS
BASE_DIR = Path(__file__).resolve().parent
main_folder = os.path.join(BASE_DIR / "downloads/")


all_folders = [
    main_folder
]


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Safe_Get:
    def __init__(self, list):
        self.list = list

    def get(self, idx, default=" "):
        try:
            return self.list[idx]
        except:
            return default


class Google:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        self.drive = drive

    def list_files(self):
        # Auto-iterate through all files that matches this query
        file_list = self.drive.ListFile(
            {'q': "'root' in parents and trashed=false"}).GetList()
        count = 0
        for file1 in file_list:
            count += 1
            print(f"""
    #               {count}
    ID:             {self.safe_list_get(file1, "id")} {bcolors.OKGREEN}
    Title:          {self.safe_list_get(file1, "title")} {bcolors.ENDC} {bcolors.FAIL}
    File type:      {self.safe_list_get(file1, "fileExtension", "folder")} {bcolors.ENDC}
    Created Date:   {self.safe_list_get(file1, "createdDate")}
    Modified Date:  {self.safe_list_get(file1, "modifiedDate")}
    Download:       {self.safe_list_get(file1, "webContentLink")}
    Size:           {self.safe_list_get(file1, "fileSize")}
            """)

    def sync_folder(self):

        for folder in all_folders:
            # Taking only files from directory (not folders)
            onlyfiles = [
                f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))
            ]

            if len(onlyfiles) > 0:
                for file_item in onlyfiles:
                    print(f"{bcolors.BOLD}{bcolors.WARNING}Started -",
                          file_item, f"{bcolors.ENDC}")
                    gfile = self.drive.CreateFile(
                        {'title': file_item})
                    # Read file and set it as the content of this instance.
                    gfile.SetContentFile(os.path.join(folder, file_item))
                    gfile.Upload()  # Upload the file.
                    print(
                        f"{bcolors.BOLD}{bcolors.OKGREEN}Uploaded{bcolors.ENDC}")

    def delete_files(self):
        for folder in all_folders:
            # Taking only files from directory (not folders)
            onlyfiles = [
                f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))
            ]
            if len(onlyfiles) > 0:
                for file_item in onlyfiles:
                    print(f"{bcolors.BOLD}{bcolors.WARNING}Deleting: ",
                          file_item, f"{bcolors.ENDC}")
                    os.remove(os.path.join(f"{folder}/{file_item}"))
                print(f"{bcolors.BOLD}{bcolors.OKGREEN}Finished{bcolors.ENDC}")

    def safe_list_get(self, l, idx, default=" "):
        try:
            return l[idx]
        except:
            return default


res = eval(input(f"""
    --------------------------------
        Hi it's batyr production
    --------------------------------
    What you want to do?{bcolors.OKGREEN}{bcolors.HEADER}
    1. List Files
    2. Sync folder 
    3. Delete folder {bcolors.ENDC}
    
    Answer: """))
app = Google()

if res == 1:
    app.list_files()
elif res == 2:
    app.sync_folder()
elif res == 3:
    app.delete_files()
else:
    print("No such command...")
