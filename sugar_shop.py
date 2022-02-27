import sqlite3
from sqlite3 import Error
import glob
import csv
import os


def create_database(database_file, sql_file): 
    '''
    CREATES NEW DATABASE FILE WITH TABLES
    '''      
    db_connection = None
    try:
        sql_file = open(sql_file, 'r')
        sql = sql_file.read()
        # print(sql)
        db_connection = sqlite3.connect(database_file)
        print(sqlite3.version)
        db_connection.executescript(sql)
        db_connection.commit()
        print(f'Sugar Shop Database successfully created in file {database_file}')
    except Error as e:
        print(e)
    finally:
        if db_connection:
            db_connection.close()

def insert_data(db_file, folder_name):
    '''
    READS DATA FROM GIVEN FOLDER AND INSERTS THEIR VALUE INTO
    CORRESPONDING TABLES
    '''
    # Collect list of csv data files
    files = glob.glob(folder_name + "\*.csv")
    files.sort()
    # print(files)
    
    for file in files:
        # Get table name from csv file name
        filename = os.path.basename(file)
        table_name = filename[2:-4]
        
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            # Get headers of csv files
            header = next(reader)
            # Build insert sql statement
            headers_str = ', '.join(header)
            question_marks = ', '.join('?' for i in header)
            sql = "INSERT INTO " + table_name + '('+ headers_str + ') VALUES (' + question_marks + ')'
            # print(sql)
            # Build a list of value tuples
            values = []
            for row in reader:
                value_tuple = tuple(row)
                values.append(value_tuple)
            db_connection = sqlite3.connect(db_file)
            
            # Insert all values from csv files into corresponding tables
            cur = db_connection.cursor()
            cur.executemany(sql, values)
            db_connection.commit()
            cur.close()
            print(f'Successfuly inserted data from file {filename}')
            
                
if __name__ == '__main__':
    create_database(database_file='sugario.db', sql_file='sugario.sql')
    insert_data(db_file='sugario.db', folder_name='data')
    

    