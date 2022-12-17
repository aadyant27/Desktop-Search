import sqlite3
from sqlite3 import Error
import os


def create_db():
    # print(os.getcwd(), 'hi')
    # Setting the location where our DataBase 'test.db' would reside.
    # os.chdir('/Users/aadyantsrivastav/Desktop/Desktop-Search')
    conn = sqlite3.connect('test.db')
    create_table(conn)

    return conn


'''
We are creating 3 tables 
Table-1: file_paths ---> [To maintain  - File_Name, File_Extension & File_Path]
Table-2: word_paths ---> [To maintain  - Word & File_Path]
Table-3: file_time_stamps ---> [To maintain  - File_Name, File_Path & TimeStamp]

INDEXING
We are indexing on the file name in file_paths and words in word_paths.
Internally indexing will create b-trees. 
The main purpose of indexing is to reduce the search time to O(logN), where N is 
the number of records in the table.
PRIMARY KEY
We create Primary Key in our Table, just to avoid duplication of rows. 
'''


# CREATING TABLES
def create_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_paths(
    file_name text NOT NULL,
    file_path text,
    PRIMARY KEY(file_name, file_path)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS word_paths(
    words text NOT NULL,
    file_path text,
    PRIMARY KEY(words, file_path)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS file_time_stamps_table(
    file_name text NOT NULL,
    file_path text,
    time_stamp real,
    PRIMARY KEY(file_name, file_path)
    )''')

    create_index(conn)


# CREATING INDEX ON THE TABLES FOR FASTER(O(LOGn)) SEARCH
def create_index(conn):
    c = conn.cursor()
    file_paths_table_index = "CREATE INDEX IF NOT EXISTS file_paths_index ON file_paths(file_name)"
    word_paths_table_index = "CREATE INDEX IF NOT EXISTS word_paths_index ON word_paths(words)"

    c.execute(file_paths_table_index)
    c.execute(word_paths_table_index)


# INSERTION INTO TABLES
def insert_into_file_paths_table(conn, values):
    try:
        c = conn.cursor()
        sql = "INSERT INTO file_paths VALUES (?,?)"
        c.execute(sql, values)
        conn.commit()
    except Error as e:
        return

def insert_into_word_paths_table(conn, values):
    try:
        c = conn.cursor()
        sql = "INSERT INTO word_paths VALUES (?,?)"
        c.execute(sql, values)
        conn.commit()
    except Error as e:
        return

def insert_into_file_time_stamps_table(conn, values):
    try:
        c = conn.cursor()
        sql = "INSERT INTO file_time_stamps_table VALUES (?,?,?)"
        c.execute(sql, values)
        conn.commit()
    except Error as e:
        return


def search_file_paths(conn, name):
    c = conn.cursor()
    print('file to be searched is:', name)
    sql = "SELECT file_path FROM file_paths WHERE file_name LIKE ?"
    name = '%'+name+'%'
    c.execute(sql, (name,))
    # for i in c.fetchall():
    #     print(i[0])
    return c.fetchall()
    # print(c.fetchall())


def search_word_paths(conn, word):
    c = conn.cursor()
    sql = "SELECT file_path FROM word_paths WHERE words = ?"
    c.execute(sql, (word,))
    return c.fetchall()


def search_time_stamps(conn, path):
    c = conn.cursor()
    sql = "SELECT * FROM file_time_stamps_table WHERE file_path = ?"
    c.execute(sql, (path,))
    return c.fetchall()


def query(conn):
    c = conn.cursor()
    # # GETTING LIST OF TABLES IN DB
    # c.execute('''SELECT name FROM sqlite_master
    # WHERE type='table' ''')
    # print(c.fetchall())
    #
    # # PRINTING COL-NAME FOR A PARTICULAR TABLE
    # c.execute('''SELECT * FROM file_paths''')
    # for i in c.description:
    #     print(i[0])
    #
    # # PRINTING INFORMATION ABOUT INDEXING IN SQLITE3(IF IT EXISTS)
    # c.execute("SELECT * FROM sqlite_master WHERE type = 'index'")
    # print(c.fetchall())

    # PRINT file_path TABLE
    count = 0
    c.execute('''SELECT * FROM file_paths''')
    for i in c.fetchall():
        count += 1
    print('Number of files parsed', count//2)


# //////////////////////////////////////////////////////////