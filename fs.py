# fs.py
# This file implements the backend logic for a simple Virtual File System
# It supports files, directories, and basic file operations (write, read, move, delete, etc.)

import pickle   # Used for saving and loading the filesystem state to a file
import os       # Used to check if the save file exists

# Represents a file inside the virtual file system
class VirtualFile:
    def __init__(self):
        # Initialize the file content as an empty string
        self.content = ""
      
    # Appends new text at the end of the file
    def write(self, text):
        self.content += text

    # Inserts or overwrites text at a specific index in the file
    def write_at(self, index, text):
        self.content = self.content[:index] + text + self.content[index + len(text):]

    # Returns the complete content of the file
    def read(self):
        return self.content

    # Returns a portion of the file content starting at 'start' position and spanning 'size' characters
    def read_from(self, start, size):
        return self.content[start:start+size]

    # Moves a chunk of text within the file from one location to another
    def move_within(self, start, size, target):
        data = self.content[start:start+size]
        self.content = self.content[:start] + self.content[start+size:]
        self.content = self.content[:target] + data + self.content[target:]

    # Truncates the file content to the specified size
    def truncate(self, size):
        self.content = self.content[:size]

# Represents the entire Virtual File System
class VirtualFileSystem:
    def __init__(self, data_file='sample.dat'):
        self.data_file = data_file    # File where filesystem will be saved
        self.fs = self.load_fs()      # Load existing filesystem or initialize new
        self.open_files = {}          # Dictionary to keep track of currently open files
        self.cwd = []                 # Current working directory as a list (path)

    # Save the current filesystem state to disk
    def save_fs(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.fs, f)

    # Load the filesystem state from disk, or create a new empty filesystem if none exists
    def load_fs(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                return pickle.load(f)
        return {'root': {}}
    
    # Create a new file in the current directory
    def create(self, filename):
        path = self.get_path()
        if filename in path:
           return "File already exists."
        else:
           path[filename] = VirtualFile()            # Create new VirtualFile instance
           self.open_files[filename] = path[filename] # Also add to open files
           self.save_fs()
        return f"File '{filename}' created."

    # Insert or overwrite text at a specific position inside a file
    def write_at(self, filename, index, text):
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
           file_obj = path[filename]
           file_obj.write_at(index, text)
           self.save_fs()
           return f"Write at index {index} successful."
        return f"File '{filename}' not found."
    
    # Read a specific range from a file
    def read_from(self, filename, start, size):
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
           return path[filename].read_from(start, size)
        return f"File '{filename}' not found."
    
    # Move a piece of text inside a file from one position to another
    def move_within_file(self, filename, start, size, target):
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
           file_obj = path[filename]
           file_obj.move_within(start, size, target)
           self.save_fs()
           return f"Moved {size} characters from position {start} to {target} in '{filename}'."
        else:
           return f"File '{filename}' not found."

    # Delete a file or directory from the current directory
    def delete(self, filename):
        path = self.get_path()
        if filename in path:
            del path[filename]
            self.save_fs()
            return f"'{filename}' deleted."
        else:
            return "File or directory does not exist."

    # Create a new directory (folder) in the current directory
    def mkdir(self, dirname):
        path = self.get_path()
        if dirname in path:
            return "Directory already exists."
        else:
            path[dirname] = {}  # A directory is just another dictionary
            self.save_fs()
            return f"Directory '{dirname}' created."

    # Change the current working directory
    def chdir(self, dirname):
        if dirname == "..":
            if self.cwd:
                self.cwd.pop()  # Move one level up
        else:
            path = self.get_path()
            if dirname in path and isinstance(path[dirname], dict):
                self.cwd.append(dirname)  # Move into the specified directory
            else:
                return "Directory not found."
        return "Current directory: /" + "/".join(self.cwd)

    # Rename (move) a file or folder
    def move(self, source, target):
        path = self.get_path()
        if source in path:
            path[target] = path.pop(source)
            self.save_fs()
            return f"Moved '{source}' to '{target}'."
        else:
            return "Source file not found."

    # Open a file and add it to the open files dictionary
    def open(self, filename):
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
           self.open_files[filename] = path[filename]
           return path[filename]
        return None

    # Get an already open file (if exists)
    def get_open_file(self, filename):
        if filename in self.open_files:
            return self.open_files[filename], filename
        return None, None

    # List all files and directories in the current directory
    def ls(self):
        return list(self.get_path().keys())

    # Navigate through the filesystem based on current working directory
    def get_path(self):
        path = self.fs['root']
        for d in self.cwd:
            path = path[d]
        return path

    # Show a memory map (tree structure) of the current filesystem
    def show_memory_map(self):
        result = []

        # Recursive helper function to print the tree structure
        def recurse(path, indent=0):
            for name, val in path.items():
                result.append("    " * indent + "├── " + name)
                if isinstance(val, dict):  # If it's a directory, recurse deeper
                    recurse(val, indent + 1)

        recurse(self.fs['root'])
        return "\n".join(result)
    
    # Truncate (cut) a file's content to a specific size
    def truncate(self, filename, size):
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
           path[filename].truncate(size)
           self.save_fs()
           return f"File '{filename}' truncated to size {size}."
        else:
           return f"File '{filename}' not found."
