#!/usr/bin/python3.4

# this is a quick script to rename stupidly named torrents and their contents to something intelligible
# usage:
# CleaningUpTorrents.py <name of file or directory> <reasonable name>

import sys
import os

# to rename from
badName = sys.argv[1]
# to rename to
goodName = sys.argv[2]

def chaffCleanup(fileName):
    print('File: ' + fileName + ' does not match known patterns. Delete? [y/N]')
    if input() == 'y':
        os.remove(fileName)

class mediaLibrary:
    def __init__(self, badName, goodName):
        # clean up the trailing / from tab completion
        self.badName = badName.rstrip(os.sep)
        self.goodName = goodName.rstrip(os.sep)
        self.cwd = os.getcwd()
        print(self.badName)
        print(self.goodName)
        print(self.cwd)
    def renameEverything(self, fileName = None, inheritedPath = None):
        # I don't like this implementation, but it's the syntax I saw recommended
        if fileName == None:
            fileName = self.badName
        if inheritedPath == None:
            inheritedPath = self.cwd
        
        # crawl through the directory and recurse this function on every file
        # because the recursion happens here, all of the modification of files
        # occurs from the bottom of the file structure up, not vise-versa
        try:
            for child in os.listdir(inheritedPath + os.sep + fileName):
                self.renameEverything(child, inheritedPath + os.sep + fileName)
        except NotADirectoryError:
            pass
        # make sure not to strip off the filename extension
        # splitext returns an empty string for directories, 
        # so no worries there. If it matches the bad name, 
        # rename it to the good one
        fileNameSections = os.path.splitext(fileName)
        for section in fileNameSections:
            print(section)
        print('goodName: ' + self.goodName)
        print('badName: ' + self.badName)
        if fileNameSections[0] == self.badName:
            destinationName = self.goodName + fileNameSections[1]
            os.rename(inheritedPath + os.sep + fileName, inheritedPath + os.sep + destinationName)
        elif fileNameSections[0] != self.goodName:
            chaffCleanup(inheritedPath + os.sep + fileName)

# by which I don't mean clean, but make sane 
def sanitizeLibrary(badName, goodName):
    badLibrary = mediaLibrary(badName, goodName)
    badLibrary.renameEverything()

if __name__ == "__main__":
    sanitizeLibrary(badName, goodName)
