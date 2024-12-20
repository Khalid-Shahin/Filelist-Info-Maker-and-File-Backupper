import os
import json
from getFileInfo import getFileInfo

print("Running...")

f = open("Filelist backupper configuation.txt", "r") #Config filename
config = json.loads(f.read())       #The config file format is json like, { "directories": ["Documents", "Pictures", "Videos"], "ignoreFileNames": ["desktop.ini"], "blockSize": 512 }
f.close()

directories = config["directories"]     #Just an array of directory name strings
ignoreFileNames = config["ignoreFileNames"] #An array of filenames to ignore
blockSize = config["blockSize"]

filesAndInfo = []

for parentDirectory in directories:
    for path, subdirs, files in os.walk(parentDirectory):
        for name in files:
            if name not in ignoreFileNames:
                fileInfo = getFileInfo(name, path, parentDirectory, blockSize)
                filesAndInfo.append(fileInfo)

print(str(len(filesAndInfo)) + " files")

filesInfoJsonString = json.dumps(filesAndInfo)

f = open("files info for backup.txt", "w")
f.write(filesInfoJsonString)
f.close()

print("Done.")
