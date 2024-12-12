# Filelist Info Maker and File Backupper
 Two main scripts to run, one to make a filelist and the metadata, and another to later search the computer for those files and copy them to the previously defined directory structure

## Untested program
This was made for myself only. I do not guarantee that data won't be lost or destroyed. Use at your own risk.

Only tested with Windows 10. It won't work for Unix without some modifications. There's no UI. No commands. Only arguments are in "Filelist backuper configuation.txt" as JSON format.

I haven't tested this outside the scope of my use case. I don't know how it handles absolute paths or anything like that.

This was made for a very specific way of backing up files. I use other backup managers as well, but I quickly made this one. I honestly don't know if anyone else would find it useful. I am just uploading it to GitHub to backup my code.

Something like this might already exist, but I figured I could make this in one evening that I know would work with all the features I wanted. The code isn't great, and the script names, filenames, and variable names aren't good. I wrote it once without any plans to further maintain it other than one or two tweaks if needed.

This program lets the user use the Windows File Explorer as normal to copy the files they want to backup to a new folder (possibly final backup destination), and then generate a JSON .txt file of all the files in that folder(s) with some metadata. So later, you can delete that folder and then run the second .py script and it will search certain directories for files that match that metadata and copy those files to the backup folder(s).

Another way it can be used is without copying the files ahead of time and then move the files each to different new destinations like in different project folders, and later use the backup program to make copies of the files from their new locations and re-creating the folders of where they were before.

Also me or someone else can make a script to modify the JSON .txt file to change the folder structure of where you'd want the files to be backed up to.

You can just use "Filelist backuper.py" to generate the JSON .txt file without using the backup script if you just want a file info list.


Possible use cases:

Scenario 1: You backup manually by copy/paste a lot of files to a USB drive using the regular File Explorer. Run "Filelist backuper.py" to generate the file list "files info for backup.txt". You give away that USB drive or lose it. You get another USB drive, plug it in, and you run "Make backup from files info.py" on there with that file list .txt file and it will search your specified directories on your computer for those files and copies them to the new destination.

Scenario 2: You just want to create file list with their paths and metadata, so you simply run "Filelist backuper.py" to generate the .txt file.

Basically it's useful if files are moved around on your system and they might not be where they were before, and you want them backed up again later.

It's also useful if you prefer using the File Explorer to choose what files you want over the UI of a program. Or if you already manually copy and pasted the files you wanted and then realized you'd want to do the backup again in the future without needing to choose the files again.

There are many downsides, here are two that I thought to mention:
1. Doesn't recognize the file if it changed size by like a byte. This can be fixed by changing a check or tweaking a line. Or file size checks can be removed completely. 
	* or abs(fileInfo["blocksOnDisk"] - searchFileInfo["blocksOnDisk"]) <= 1		#Can be changed to a larger number to give more of a range in file size differences. 
	* fileHalfBlocks = round(math.ceil(os.path.getsize(os.path.join(path, name))/block_size)/2)		#Can be changed to divide by a bigger number like 10 to give the size recognition more range.
2. It's not particularly fast at backing up, but it gets the job done since I don't run it frequently.


You may find this program is 90% of what you want and you can add onto it to get that last 10% you need.


There are two main scripts for the user to run:
1. Filelist backuper.py
	* This will generate "files info for backup.txt" which has all the filenames, relative and absolute directory paths, subpaths, and some metadata.
	* Depending on use case, this script may be useful as is without needing to run the second script.
2. Make backup from files info.py
	* This script loads "files info for backup.txt" and searches specified directories for files that match, and copies them to the previously defined folders.
	* This will overwrite files of the same name in the destination.
	* It will create all the needed paths and subpaths.


Both of these scripts load "Filelist backuper configuation.txt"


Config File "Filelist backuper configuation.txt"
1. directories, the (relative) backedup folder structure
2. ignoreFileNames, what filenames will be ignored for when the first script generates "files info for backup.txt"
3. directoriesToSearch, the absolute paths of the directories you want to search in by the second script
4. blockSize, set this to whatever the block size are for your hard drive. This isn't all too important really.

## Instructions
1. Have the files you want to backup in the folder structure you want the backup to be in. So you'd manually backup the files you want to a backup destination folder using the normal Windows File Explorer.
2. Put the "Filelist backuper.py" script in the same directory as the manually backed up folders, and run it. (I haven't tested absolute paths, so maybe this isn't necessary.)
3. If that script was successful you'll have "files info for backup.txt" and confirm that it looks like it recognized the files you wanted.
4. You'd keep "files info for backup.txt" so later you can run "Make backup from files info.py" which will search in the specified directories (directoriesToSearch) for those files.
5. It will copy those files to the destination, subpaths and all, and will overwrite any existing files of the same name. And it will let you know of the files that it couldn't find.
6. If you later want more files to be backed up, after yoou run that "Make backup from files info.py" script so all the backed up files are present, you can manually copy new files into those directories as needed and then re-run "Filelist backuper.py" to generate the new list.
7. Always double check to make sure the files you want to be backed up are recognized, and double check to make sure that they are all copied over properly. This program doesn't have proper error checking or graceful exiting on crash.

## License
You may use and modify this program in any which way as you wish with or without attribution. You can make derivative works from it. I have no rights reserved and I publish this into the public domain under the CC0 license.

In short: Do whatever you want with it and no attribution needed.

I didn't check the license for the libraries that this program imports. Which are the Python Standard Library and pywin32. So be sure to follow the license for those if it's relevant. CC0 only applies to the source code in this repo.


## This program is untested. I do not guarantee that data won't be lost or destroyed. Use at your own risk.