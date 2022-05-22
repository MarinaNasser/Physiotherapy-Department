import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="85426Mm854267890",
  database="sbe2024"
)

mycursor = mydb.cursor()

sql = "UPDATE DOCTOR SET id = %s WHERE id = %s"
val = (5, 1)

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record(s) affected") 
