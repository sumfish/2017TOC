import sqlite3

conn = sqlite3.connect('database')
print("Opened database successfully")


conn.execute('CREATE TABLE items (d TEXT,item TEXT,money TEXT)')
print("Table created successfully")


   
conn.close()



