import sqlite3

def create_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    create_table(conn)

    return conn

'''
We are creating 3 tables 
Table-1: file_paths ---> [To maintain  - File_Name, File_Extension & File_Path]
Table-2: word_paths ---> [To maintain  - Word & File_Path]
Table-3: file_time_stamps ---> [To maintain  - File_Name, File_Path & TimeStamp]

We are indexing on the file name in file_paths and words in word_paths.
Internally indexing will create b-trees. 
The main purpose of indexing is to reduce the search time to O(logN), where N is 
the number of records in the table.
'''

# CREATING TABLES
def create_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_paths(
    file_name text,
    file_path text
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS word_paths(
    word text,
    file_path text
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS file_time_stamps_table(
    file_name text,
    file_path text,
    time_stamp real
    )''')

    create_index(conn)

# CREATING INDEX ON THE TABLES FOR FASTER(O(LOGn)) SEARCH
def create_index(conn):
    c = conn.cursor()
    file_paths_table_index = "CREATE INDEX IF NOT EXISTS file_paths_index ON file_paths(file_name)"
    word_paths_table_index = "CREATE INDEX IF NOT EXISTS word_paths_index ON word_paths(word)"

    c.execute(file_paths_table_index)
    c.execute(word_paths_table_index)


# INSERTION INTO TABLES
def insert_into_file_paths_table(conn, values):
    c = conn.cursor()
    sql = "INSERT INTO file_paths VALUES (?,?)"
    c.execute(sql, values)
    conn.commit()
    print('done')

def insert_into_word_paths_table(conn, values):
    c = conn.cursor()
    sql = "INSERT INTO word_paths VALUES (?,?)"
    c.execute(sql, values)
    conn.commit()

def insert_into_file_time_stamps_table(conn, values):
    c = conn.cursor()
    sql = "INSERT INTO file_time_stamps_table VALUES (?,?,?)"
    c.execute(sql, values)
    conn.commit()



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
        print(i)
        count += 1
    print(count)


c = create_db()





