from win32com.propsys import propsys
from win32com.shell import shellcon
import os
import time
import math

propkeywords = propsys.PSGetPropertyKeyFromName("System.Keywords")
propcomment = propsys.PSGetPropertyKeyFromName("System.Comment")
proprating = propsys.PSGetPropertyKeyFromName("System.Rating")
propcopyright = propsys.PSGetPropertyKeyFromName("System.Copyright")
propwidth = propsys.PSGetPropertyKeyFromName("System.Video.FrameWidth")
propheight = propsys.PSGetPropertyKeyFromName("System.Video.FrameHeight")
propframerate = propsys.PSGetPropertyKeyFromName("System.Video.FrameRate")
propduration = propsys.PSGetPropertyKeyFromName("System.Media.Duration")

def getFileInfo(name, path, parentDirectory = "", blockSize = 512):
    directoryAndFilename = os.path.join(path, name)
    absoluteDirectoryAndFileName = os.path.abspath(directoryAndFilename)
    createdTime = os.path.getctime(directoryAndFilename)        #For my use case the created time isn't too useful, just use the modified time
    modifiedTime = os.path.getmtime(directoryAndFilename)
    createdTimePlain = time.ctime(createdTime)
    modifiedTimePlain = time.ctime(modifiedTime)
    tags = None
    comment = None
    rating = None
    ratingPlain = None
    copyrightValue = None
    width = None
    height = None
    framerate = None
    duration = None
    durationSeconds = None
    durationMinuteSecondsPlain = None

    try:
        propstore = propsys.SHGetPropertyStoreFromParsingName(directoryAndFilename, None, shellcon.GPS_READWRITE, propsys.IID_IPropertyStore)

        tags = propstore.GetValue(propkeywords).GetValue()
        comment = propstore.GetValue(propcomment).GetValue()
        copyrightValue = propstore.GetValue(propcopyright).GetValue()
        width = propstore.GetValue(propwidth).GetValue()
        height = propstore.GetValue(propheight).GetValue()
        framerate = propstore.GetValue(propframerate).GetValue()

        rating = propstore.GetValue(proprating).GetValue()
        if rating == 1:
            ratingPlain = 1
        elif rating == 25:
            ratingPlain = 2
        elif rating == 50:
            ratingPlain = 3
        elif rating == 75:
            ratingPlain = 4
        elif rating == 99:
            ratingPlain = 5
            
        duration = propstore.GetValue(propduration).GetValue()

        if duration:
            durationSeconds = duration/10000000
            durationMinutesNoSeconds = math.floor(durationSeconds/60)
            if durationMinutesNoSeconds:
                durationMinuteSecondsPlain = str(durationMinutesNoSeconds) + " minutes "
            else:
                durationMinuteSecondsPlain = ""
            durationMinuteSecondsPlain += str(math.floor(((durationSeconds/60)-durationMinutesNoSeconds)*60)) + " seconds"

    except:
        pass

    fileSize = os.path.getsize(directoryAndFilename)
    fileSizeOnDisk = math.ceil(fileSize/blockSize)
    
    fileInfo = {
        "name": name,
        "path": path,
        "subPath": path[len(parentDirectory)+1:],                   #Redundant
        "parentDirectory": parentDirectory,                         #Redundant
        "directoryAndFilename": directoryAndFilename,
        "absoluteDirectoryAndFileName": absoluteDirectoryAndFileName,
        "fileSize": fileSize,
        "blocksOnDisk": fileSizeOnDisk,                             #Redundant
        "createdTime": createdTime,
        "modifiedTime": modifiedTime,
        "createdTimePlain": createdTimePlain,                       #Redundant
        "modifiedTimePlain": modifiedTimePlain,                     #Redundant
        "tags": tags,
        "comment": comment,
        "rating": rating,
        "ratingPlain": ratingPlain,                                 #Redundant
        "copyright": copyrightValue,
        "width": width,
        "height": height,
        "framerate": framerate,
        "duration": duration,
        "durationSeconds": durationSeconds,                         #Redundant
        "durationMinuteSecondsPlain": durationMinuteSecondsPlain    #Redundant
    }

    return fileInfo
