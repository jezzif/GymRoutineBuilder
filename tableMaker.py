import sqlite3
import csv

def test(conn):
    #myTable = "fx_eg_i"
    #myValue = "0.1"
    print("Testing...")
    cursor = conn.cursor()
    #cursor.execute("SELECT skillName FROM "+myTable+" WHERE skillValue = ? ORDER BY skillNumber", (myValue,))
    cursor.execute("SELECT * FROM fx_eg_iv")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def delete(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE test")
    conn.commit()

def populate(conn):
    cursor = conn.cursor()
    file = open("MAG_CoP\\PH_EG-III-DB.csv")
    contents = csv.reader(file)
    insert_records = "INSERT INTO ph_eg_iii (skillName, skillDescr, skillValue, skillNumber, skillElemGrp, fullSpindleTravels, fullCrossSupTravels, fullRussianTravels) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
    cursor.executemany(insert_records, contents)
    conn.commit()

def make_tables(conn, tableName):
    
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS {}
                    (skillName UNIQUE NOT NULL,
                   skillDescr UNIQUE NOT NULL,
                   skillValue NOT NULL,
                   skillElemGrp NOT NULL,
                   skillNumber PRIMARY KEY UNIQUE NOT NULL)'''.format(tableName))
    conn.commit()

def new_routine_table(cursor, tableName):
    cursor.execute('''CREATE TABLE IF NOT EXISTS {}
                    (skillName UNIQUE NOT NULL,
                   skillDescr UNIQUE NOT NULL,
                   skillValue NOT NULL,
                   skillElemGrp NOT NULL,
                   skillNumber PRIMARY KEY UNIQUE NOT NULL)'''.format(tableName))

        