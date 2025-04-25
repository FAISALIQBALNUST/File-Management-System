# fs.py
import pickle
import os

class VirtualFile:
    def __init__(self):
        self.content = ""
      

    def write(self, text):
        self.content += text

    def write_at(self, index, text):
        self.content = self.content[:index] + text + self.content[index + len(text):]

    def read(self):
        return self.content

    def read_from(self, start, size):
        return self.content[start:start+size]

    def move_within(self, start, size, target):
        data = self.content[start:start+size]
        self.content = self.content[:start] + self.content[start+size:]
        self.content = self.content[:target] + data + self.content[target:]

    def truncate(self, size):
        self.content = self.content[:size]

class VirtualFileSystem:
    def __init__(self, data_file='sample.dat'):
        self.data_file = data_file
        self.fs = self.load_fs()
        self.open_files = {}
        self.cwd = []
        
    def save_fs(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.fs, f)

    def load_fs(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                return pickle.load(f)
        return {'root': {}}
    
    def create(self, filename):
        path = self.get_path()
        if filename in path:
           return "File already exists."
        else:
           path[filename] = VirtualFile()
           self.open_files[filename] = path[filename]  # Add to open_files as well
           self.save_fs()
        return f"File '{filename}' created."


    def write_at(self, filename, index, text):
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
           file_obj = path[filename]
           file_obj.write_at(index, text)
           self.save_fs()
           return f"Write at index {index} successful."
        return f"File '{filename}' not found."
    def read_from(self, filename, start, size):
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
           return path[filename].read_from(start, size)
        return f"File '{filename}' not found."
    
    def move_within_file(self, filename, start, size, target):
    # Check if the file exists in the correct location (open_files or files)
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
           file_obj = path[filename]
           file_obj.move_within(start, size, target)
           self.save_fs()
           return f"Moved {size} characters from position {start} to {target} in '{filename}'."
        else:
           return f"File '{filename}' not found."



    
    def delete(self, filename):
        path = self.get_path()
        if filename in path:
            del path[filename]
            self.save_fs()
            return f"'{filename}' deleted."
        else:
            return "File or directory does not exist."

    def mkdir(self, dirname):
        path = self.get_path()
        if dirname in path:
            return "Directory already exists."
        else:
            path[dirname] = {}
            self.save_fs()
            return f"Directory '{dirname}' created."

    def chdir(self, dirname):
        if dirname == "..":
            if self.cwd:
                self.cwd.pop()
        else:
            path = self.get_path()
            if dirname in path and isinstance(path[dirname], dict):
                self.cwd.append(dirname)
            else:
                return "Directory not found."
        return "Current directory: /" + "/".join(self.cwd)

    def move(self, source, target):
        path = self.get_path()
        if source in path:
            path[target] = path.pop(source)
            self.save_fs()
            return f"Moved '{source}' to '{target}'."
        else:
            return "Source file not found."

    def open(self, filename):
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
        # Add to open_files to track open files
           self.open_files[filename] = path[filename]
           return path[filename]
        return None



    def get_open_file(self, filename):
        if filename in self.open_files:
            return self.open_files[filename], filename
        return None, None


    def ls(self):
        return list(self.get_path().keys())

    def get_path(self):
        path = self.fs['root']
        for d in self.cwd:
            path = path[d]
        return path

    def show_memory_map(self):
        result = []

        def recurse(path, indent=0):
            for name, val in path.items():
                result.append("    " * indent + "├── " + name)
                if isinstance(val, dict):
                    recurse(val, indent + 1)

        recurse(self.fs['root'])
        return "\n".join(result)
    
 
    def truncate(self, filename, size):
        path = self.get_path()
        if filename in path and isinstance(path[filename], VirtualFile):
           path[filename].truncate(size)
           self.save_fs()
           return f"File '{filename}' truncated to size {size}."
        else:
           return f"File '{filename}' not found."
