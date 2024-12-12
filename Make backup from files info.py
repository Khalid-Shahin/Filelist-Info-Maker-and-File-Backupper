import os
import shutil
from pathlib import Path
import math
from copy import deepcopy
import json
from getFileInfo import getFileInfo

#This will overwrite any files of the same name in the destination

print("Running...")

f = open("Filelist backupper configuation.txt", "r") #Config filename
config = json.loads(f.read())       #The config file format is json like, { "directories": ["Documents", "Photos", "Videos"] }
f.close()

searchDirectories = config["directoriesToSearch"]     #Just an array of full path strings
blockSize = config["blockSize"]

f = open("files info for backup.txt", "r") #File info of what to find and backup
filesInfo = json.loads(f.read())
f.close()

print(str(len(filesInfo)) + " files")

filesToCopy = []

fileInfoDictionary = {}

for fileInfo in filesInfo:
    fileName = fileInfo["name"]
    if fileName not in fileInfoDictionary:
        fileInfoDictionary[fileName] = [fileInfo]
    else:
        fileInfoDictionary[fileName].append(fileInfo)
        print("Not a problem, duplicate filename: " + fileName)

fileNames = fileInfoDictionary.keys()

def propertyCompare(fileInfo, searchFileInfo, propertyName):
    if not fileInfo[propertyName] or fileInfo[propertyName] == searchFileInfo[propertyName]:
        return True
    else:
        return False

def propertiesCompare(fileToCopyInfo, searchFileInfo, properties):
    for propertyName in properties:
        if not propertyCompare(fileToCopyInfo, searchFileInfo, propertyName):
            return False
    return True

def isItAMatch(searchFileInfo, infoEntries, properties = ["duration", "framerate", "width", "height"]):
    index = 0
    for fileInfo in infoEntries:
        if propertyCompare(fileInfo, searchFileInfo, "fileSize") or abs(fileInfo["blocksOnDisk"] - searchFileInfo["blocksOnDisk"]) <= 1:
            if propertiesCompare(fileInfo, searchFileInfo, properties): #Checks to make sure the properties match (if it's available)
                searchFileInfo["originalInfo"] = fileInfo
                filesToCopy.append(deepcopy(searchFileInfo))    #I probably don't need to make a deepcopy
                infoEntries.pop(index) #Removes from the entry from the array in the dictionary as they find it
                return True
        index += 1
    return False

for directory in searchDirectories:
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if name in fileNames:
                searchFileInfo = getFileInfo(name, path, directory, blockSize)
                if isItAMatch(searchFileInfo, fileInfoDictionary[name], ["duration", "framerate", "width", "height"]):
                    if len(fileInfoDictionary[name]) == 0:  #if array is length 0 remove the filename entry
                        del fileInfoDictionary[name]

fileInfoDictionaryByHalfBlocks = {}

#Tries to find a match a different way
#If same File Size or Same Number of Blocks, AND same file extension, AND same width and height, same frame rate, same duration
#And maybe one of the following can be a property it checks (not written yet): Date Modified OR same comment if there's one
for fileName in fileInfoDictionary:     #If there's any filenames left, that means there are still files that are unfound, perhaps a filename change so it attempts to find them using different methods
    filesInfo = fileInfoDictionary[fileName]
    for fileInfo in filesInfo:
        fileSize = fileInfo["fileSize"]
        fileHalfBlocks = round(fileInfo["blocksOnDisk"]/2)
        
        if fileHalfBlocks not in fileInfoDictionaryByHalfBlocks:
            fileInfoDictionaryByHalfBlocks[fileHalfBlocks] = [fileInfo]
        else:
            fileInfoDictionaryByHalfBlocks[fileHalfBlocks].append(fileInfo)
            print("Not a problem, duplicate file size in half blocks found: " + fileName)

for directory in searchDirectories:
    for path, subdirs, files in os.walk(directory):
        for name in files:
            fileHalfBlocks = round(math.ceil(os.path.getsize(os.path.join(path, name))/blockSize)/2)
            if fileHalfBlocks in fileInfoDictionaryByHalfBlocks:
                searchFileInfo = getFileInfo(name, path, directory, blockSize)
                fileExtension = name.split(".")[-1]
                for fileInfo in fileInfoDictionaryByHalfBlocks[fileHalfBlocks]:
                    if fileInfo["name"].split(".")[-1] == fileExtension:
                        if isItAMatch(searchFileInfo, fileInfoDictionaryByHalfBlocks[fileHalfBlocks], ["duration", "framerate", "width", "height"]):
                            if len(fileInfoDictionaryByHalfBlocks[fileHalfBlocks]) == 0:  #if array is length 0 remove the filename entry
                                del fileInfoDictionaryByHalfBlocks[fileHalfBlocks]

if len(fileInfoDictionaryByHalfBlocks.keys()):
    print("Files that couldn't be found: " + str(fileInfoDictionaryByHalfBlocks.keys()))        #Couldn't find some files for one reason or another perhaps the files were deleted
else:
    print("Found all the files!")

print("Now copying them to the new location.")

for file in filesToCopy:
    fileName = file["name"]
    if len(file["originalInfo"]["name"]) > len(fileName):
        fileName = file["originalInfo"]["name"]

    paths = file["originalInfo"]["directoryAndFilename"].split("\\")[:-1]

    Path("\\".join(paths)).mkdir(parents=True, exist_ok=True)   #Creates the directories
    shutil.copy2(file["absoluteDirectoryAndFileName"], file["originalInfo"]["directoryAndFilename"]) #Copies the files while preserving the metadata

print("Done.")
