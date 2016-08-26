#!/usr/bin/python3

# This program takes one argument: a directory path.
# It looks at every file in that directory, and hashes its contents,
# then gives it a name composed of three random words selected 
# deterministically from that hash.

from sys import exit, argv
from hashlib import sha512
import os

# Start by verifying that a words file exists.
def getWords(path='/usr/share/dict/words'):
    try:
        with open(path, 'r') as wordsFile:
            return wordsFile.readlines()
    except FileNotFoundError:
        print('No words file found at {}.'.format(path))
        sys.exit(1)

# Get an int from the hash of file contents.
def hashFile(path):
    with open(path, 'rb') as f:
        # Pipe contents into hash, get hexdump, decode to int.
        #contents = f.read().encode()
        #return int(sha512(contents).hexdigest(), 16)
        return int(sha512(f.read()).hexdigest(), 16)

# Make a name of three words from the words list and an integer.
def makeUpName(filename, words):
    name = ''
    wordslen = len(words)
    seed = hashFile(filename)
    for i in range(3):
        index = seed % wordslen
        seed += index
        word = str(words[index]).capitalize().strip().replace("'", '')
        name += word
    print(name)
    return name

# Main function; renames specified files based on their contents.
def renameFiles(path, words):
    try:
        files = os.listdir(path)
        # If it's a directory, then we need to strip trailing slashes, and
        # prepend the path to each file name.
        path = path.rstrip('/') + os.sep
        for index, f in enumerate(files):
            files[index] = path + f
    except NotADirectoryError:
        files = [path]
        path = ''
    except FileNotFoundError:
        print('Invalid path: {}.'.format(path))
        exit(1)
        
    words = getWords()
    for filename in files:
        # Get the filetype.
        if len(filename.split('.')) > 1:
            ext = '.' + filename.split('.')[-1]
        else:
            ext = ''
        os.rename(filename, path + makeUpName(filename, words) + ext)

if __name__ == '__main__':
    for arg in argv[1:]:
        renameFiles(arg, getWords())
    
