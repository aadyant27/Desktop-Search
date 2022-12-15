import sqlite3
from DB_file import search_file_paths, search_time_stamps, search_word_paths
from subprocess import call

conn = sqlite3.connect('test.db')

"""
1. Input == 1 => file/ext search
2. Input == 2 => word search
    2.1 If Input == 2, Enter 1 to 3 words to commence search
"""


# TO REDIRECT/OPEN FILE, CHOSEN BY USER
def redirect(path):
    call(["open", "{0}".format(path)])


print('[NOTE] : You can search for .txt, .pdf, .docx files only')
search_type = int(input('Press 1 for search by file-name/file-extension.\nPress 2 for search by word.\n=> '))
if search_type == 1:
    # File-name/.ext type search
    name = input('Enter file-name or file-extension\n=> ').lower()

    # Searching for file-paths
    files = search_file_paths(conn, name)
    file_paths = []
    for i in files:
        file_paths.append(i[0])

    # Searching for timestamps associated with file-names
    ts = []  # ts will contain file-name, file-path, file-timestamp
    for i in file_paths:
        ts += search_time_stamps(conn, i)

    # Sort in Descending Order i.e. file that has the greatest time stamp will be the most-recently-edited file
    ts.sort(key=lambda x: x[2], reverse=True)

    # Displaying Top-5 files(sorted by timestamp) i.e. top-5 files which are most-recently-edited
    i = 0
    files = []
    for file in ts:
        if i >= 6:
            break
        print(i, file[1])
        files.append(file[1])
        i += 1

    # REDIRECTING(OPENING) THE FILE OF CHOICE
    # Choosing a file to open/redirect
    choice = int(input('Enter id associated with the file you want to select: '))
    # Redirecting/opening the chosen file
    redirect(files[choice])


elif search_type == 2:
    # Word type search
    words = input('Enter 1-3 words\n=> ').lower()
    # Searching for file paths
    files = search_word_paths(conn, words)

    file_paths = []
    for i in files:
        file_paths.append(i[0])

    # SORTING BASED ON TIME STAMP
    ts = []
    for i in file_paths:
        ts += search_time_stamps(conn, i)
    ts.sort(key=lambda x: x[2], reverse=True)

    # SELECTING TOP-5
    files = []
    i = 0
    for file in ts:
        if i >= 6:
            break
        files.append(file[1])
        print(i, file[1])
        i += 1

    # REDIRECTING(OPENING) THE FILE
    choice = int(input('Enter id associated with the file you want to select: '))
    redirect(files[choice])

