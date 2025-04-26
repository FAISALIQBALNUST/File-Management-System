###################  User Guide: How to Use the System  ################

#########################  Directory Structure  ########################
 The system has a root directory (/).

 You can create files and folders inside root or inside any subfolder.

 Files are instances of VirtualFile, folders are just dictionaries.
#########################################################################

#######################   Using the System ##############################
  Keep both the fs.py and gui.py in same directory and
  Launch the GUI by running gui.py.

  You can:

  Use the command line by entering commands supported, in the text entry box.

  Right-click on a file to Open or Delete.

  Right-click on an empty area to Create File, Create Folder, or get Help.

  Double-click a file to open it or double-click a folder to enter it.

  Click Clear to clear outputs, and Browse Dir to refresh the directory view.
###########################################################################
###########################  Supported Commands  ##########################

you can get these from the help button:

###########################################################################
create <filename> — Create a new file

mkdir <foldername> — Create a new directory

ls — List files/folders

chdir <dirname> — Change directory

del <filename|dirname> — Delete file or directory

open <filename> — Open a file

read <filename> — Read a file

write <filename> <text> — Append text to a file

write_at <filename> <index> <text> — Insert text at specific index

read_start_len <filename> <start> <size> — Read partial content

move_within <filename> <start> <size> <target> — Move part of content inside a file

truncate <filename> <size> — Cut file content to a certain length

memmap — Display memory map of folders and files

Shortcut Features:

Up/Down arrow keys: Navigate command history.

Help button: Quick guide popup.

Exit button: Close the app.
