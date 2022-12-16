import os
import glob
import re

from DB_file import create_db, insert_into_file_paths_table, insert_into_word_paths_table,\
    insert_into_file_time_stamps_table, query
from text_extractor import pdf_reader, docx_reader, text_reader


# INPUT FROM USER
# dir_path = '/Users/aadyantsrivastav/Desktop/'
dir_path = input('Enter Absolute-file-path for which you want to search the files\n[NOTE] : You can use pwd command \
to get Absolute file path of current working directory!\n=> ')

print('Wait while files are being processed...\n')
# CREATING DB
conn = create_db()

'''
--PARSE FOLDER AND SCRAPE FILE
-We will be parsing json, pdfs, docx, txt, py, js, csv, ipynb, html files
-NAME OF FILE will limit input to be 3 or less characters i.e. WORDS[1, 2, 3]

-We need to parse CONTENT OF THE FILES & store it in "word_paths" table
-"word_paths" table will also have words obtained from splitting "file_names"
-"time_stamp" table will be used solely to filter out final result based on timestamp/creation time
'''
os.chdir(dir_path)

# Parsing all files in the cwd
unique_file_names = []
all_files = dict()

# SEARCH FOR FILES IN CWD
for i in glob.glob("**//*.*", recursive=True):
    if re.search(".json$|.pdf$|.docx$|.txt$|.py$|.csv$|.ipynb$|.html$", i):
        file_name = i.split('/')[-1]
        if all_files.get(file_name) is None:
            all_files[file_name] = [1]
            all_files[file_name].append(i)
        else:
            all_files[file_name][0] += 1
# ANOTHER WAY TO SPLIT FILE NAMES & FILE PATHS(by using "os.path()")
# for i in glob.glob("**//*.*", recursive=True):
#     file_path, file_name = os.path.split(i)
#     print(file_path)

# REMOVING DUPLICATES FILES(files such as, those in node_modules folder, which are common, are removed)
for k, v in all_files.items():
    if v[0] == 1:
        res = []
        res.append(k)
        res.append(v[1])
        unique_file_names.append(res)


# POPULATING 'file_paths' & 'file_time_stamp_table'
for i in unique_file_names:
    # POPULATING file_path TABLE with (file_name + file_extension) & file_path
    name, path = i
    path = dir_path + path
    ext = os.path.splitext(path)[1]
    f_name = os.path.splitext(path)[0].split('/')[-1]
    insert_into_file_paths_table(conn, [f_name.lower(), path])
    insert_into_file_paths_table(conn, [ext, path])

    # Populating file_time_stamps_table with file_name, file_path & time_stamp
    # Getting 'last-modified-time' of the files for 'file_time_stamps_table'
    time_stamp = os.path.getctime(path)
    insert_into_file_time_stamps_table(conn, [f_name.lower(), path, time_stamp])

'''
--PREPROCESSING
-Extracting text from files(by parsing files individually) is done in "textExtractor.py"
-Removing Stop-Words is also done in "textExtractor.py"
-Creating uni/bi/tri-grams
-Since this is a text based search, we remove non-alphabet symbols from the files

-os.path.getctime() method in Python is used to get system’s ctime of the specified path.
 Here ctime refers to the last metadata change for specified path in UNIX 

'''
# Counts total no of words to be inserted in 'words_path' table i.e. uni + bi + tri grams.
count = 0


# Function to convert bi/tri-grams out of extracted uni-gram words
def convert_bi_tri_grams(uni_grams, count):
    # Create Bi-grams & append them to 'words' array
    bi_grams = []
    for i in range(len(uni_grams)-2):
        temp = uni_grams[i] + ' ' + uni_grams[i+1]
        bi_grams.append(temp)

    # Create Tri-grams & append them to 'words' array
    tri_grams = []
    for i in range(len(uni_grams)-3):
        temp = uni_grams[i] + ' ' + uni_grams[i+1] + ' ' + uni_grams[i+2]
        tri_grams.append(temp)

    words = uni_grams + bi_grams + tri_grams
    count += len(words)
    return words, count


for name, path in unique_file_names:
    extension = os.path.splitext(path)[1]
    path = dir_path + path
    uni_grams = []

    if extension == '.pdf':
        uni_grams = pdf_reader(path)
    elif extension == '.txt':
        uni_grams = text_reader(path)
    elif extension == '.docx':
        uni_grams = docx_reader(path)

    # Create Bi/Tri-grams
    if uni_grams:
        words, count = convert_bi_tri_grams(uni_grams, count)

        # Populating word_paths table
        for i in words:
            insert_into_word_paths_table(conn, [i, path])


print('Total words parsed', count)
query(conn)

# //////////////////////////////////////////////END/////////////////////////////////////////////////////


# ///////////TASK COMPLETED
'''
1. [done] CREATION OF DB
2. [done] PARSING OF ALL THE FILE IN THE CWD/PATH(user_defined)
3. [done] INSERT (FILE_NAME + FILE_EXTENSION) & FILE PATH IN 'file_paths' TABLE
4. [done] INSERT WORDS & FILE PATHS IN 'word_paths' TABLE
    4.1 [done] FIRST WE WILL PARSE WORDS FOR 'txt', 'docx' & 'pdf' FILES ONLY
    4.2 [done] CREATE BI/TRI GRAMS & APPEND IT TO UNI-GRAMS ARRAY
    4.3 [done] INSERT IN words_path TABLE
    4.4 [NOT-DONE] AFTER SUCCESSFUL COMPLETION, WE WILL PARSE FOR REST OF THE EXTENTIONS
5. [done] INSERT INTO TIME-STAMP TABLE
6. [done] CREATE PRIMARY KEYS FOR EACH DATABASE, TO AVOID DUPLICATION
7. [done] RETRIEVAL OF INFORMATION WHEN USER SEARCHES
8. [done] PRINT TOTAL FILE THAT WERE PROCESSED
9. [done] ADD REDIRECTING FUNCTIONALITY 
    9.1 STORE 5 RESULTS IN AN ARRAY
    9.2 ASK USER TO INPUT, WHICH FILE THEY WANT TO GO TO FROM 1-5
    9.3 BASED ON THE INPUT SELECT THE PATH OF THE FILE FROM THE ARRAY 
    9.4 REDIRECT (to open a file from terminal, we use "open file_path")
'''