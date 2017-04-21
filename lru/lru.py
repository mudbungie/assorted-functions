#!/usr/bin/env python

from sys import stdin, exit
from collections import deque

class Cache():
    def __init__(self, size):
        self.size = size
        self.queue = deque()
        self.items = {}

    def put(self, key, value):
        # Add the item to the queue and dict
        self.queue.append(key)
        self.items[key] = value

        if len(self.queue) > self.size:
            first_out = self.queue.popleft()
            # If it's the only instance of that item in the queue, then clear it.
            if first_out not in self.queue:
                del(self.items[first_out])
    
    def get(self, key):
        # Move the key to the most recent position.
        self.queue.remove(key)
        self.queue.append(key)

        return self.items[key]
    
def read_input():
    # Iterate over input as lists of args
    for line in stdin.readlines():
        line = line.strip().split(' ')
        command = line[0]
        if command == "SIZE":
            try:
                try:
                    cache
                # Make sure that it's not defined already.
                except NameError:
                    cache = Cache(int(line[1]))
                    print("SIZE OK")
            except (ValueError, IndexError):
                print("ERROR")

        elif command == "GET":
            try:
                print("GOT " + cache.get(line[1]))
            except ValueError:
                print("NOTFOUND")
            except (IndexError, NameError):
                print("ERROR")
            
        elif command == "SET":
            try:
                cache.put(line[1], line[2])
                print("SET OK")
            except (IndexError, NameError):
                print('ERROR')

        elif command == "EXIT":
            exit()

        else:
            print("ERROR")

if __name__ == "__main__":
    read_input()
