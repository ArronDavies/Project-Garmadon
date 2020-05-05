import sqlite3 as sql
import os
import csv
from sqlite3 import Error

try:
  conn=sql.connect('../../PikaChewniverse.sqlite')
  cur = conn.cursor()
  cur.execute('''SELECT * FROM Characters''')
  rows = cur.fetchall()
   
  for row in rows:
      print(row)

  print "Exporting data into CSV............"
  cursor = conn.cursor()
  cursor.execute("select * from Characters")
  with open("character_data.csv", "w") as csv_file:
      csv_writer = csv.writer(csv_file, delimiter="\t")
      csv_writer.writerow([i[0] for i in cursor.description])
      csv_writer.writerows(cursor)

  dirpath = os.getcwd() + "character_data.csv"
  print "Data exported Successfully into {}".format(dirpath)

except Error as e:
  print(e)

finally:
  conn.close()