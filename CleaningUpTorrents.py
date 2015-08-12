#!/usr/bin/python3

# this is a quick script to rename stupidly named torrents and their contents to something intelligible
# usage:
# CleaningUpTorrents.py <name of file or directory> <reasonable name>

import sys
import os

# to rename from
badName = sys.argv[1]
# to rename to
goodName = sys.argv[2]

class mediaLibrary:
    def __init__(self, badName, goodName):
        # clean up the trailing / from tab completion
        self.badName = badName.rstrip(os.sep)
        self.goodName = goodName.rstrip(os.sep)
        self.cwd = os.getcwd() + os.sep
        print(self.badName)
        print(self.goodName)
        print(self.cwd)
    def renameEverything(self, fileName = None, inheritedPath = None):
        # I don't like this implementation, but it's the syntax I saw recommended
        # I onlt even go down this road because the recursion requires it
        if fileName == None:
            fileName = self.badName
        if inheritedPath == None:
            inheritedPath = self.cwd
        fullName = inheritedPath + fileName
        isDir = os.path.isdir(fullName)
                
        # crawl through any subdirectories and recurse this function on 
        # every file. Because the recursion happens here, the process goes
        # from bottom to top
        if isDir:
            # to preserve filetypes. Makes more sense when you see it used 
            # on actual files. 
            fileNameRoot = fullName
            fileNameExt = ''
            for child in os.listdir(fullName):
                # recurse, extending the path with the directory that we're
                # presently working on
                self.renameEverything(child, fullName + os.sep)
        else:
            # preserving filetypes
            fileNameSections = os.path.splitext(fileName)
            fileNameRoot = fileNameSections[0]
            fileNameExt = fileNameSections[1]
        # to prevent unbound errors
        whatToDo = False
        # don't ask if it's either the good name or the bad name (we know what to do)
        if fileNameRoot != self.goodName and fileNameRoot != self.badName:
            whatToDo = input('File: ' + fileName + ' does not match known patterns. ' +
                                'Delete? [y/N/r(ename)]')
            if whatToDo == 'y':
                if isDir:
                    try:
                        os.rmdir(fullName)
                    # don't delete empty directories
                    except OSError:
                        print('You actually liked some things in that directory. ' +
                                'Sending you through to review again.')
                        self.renameEverything(fileName, inheritedPath)
                else:
                    os.remove(fullName)
            # if it's exactly the match, or if the user decided to go ahead and 
            # rename anyways
        if fileNameRoot == self.badName or whatToDo == 'r':
            destinationName = self.goodName + fileNameExt
            os.rename(inheritedPath + fileName, inheritedPath + destinationName)
            print('Renamed ' + fileName + ' to ' + destinationName)

if __name__ == "__main__":
    badLibrary = mediaLibrary(badName, goodName)
    badLibrary.renameEverything()
