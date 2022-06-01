import email
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="A_0l1a2a3",
  database="felcode"
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE sbe2024")
# mycursor.execute("CREATE TABLE patient (Fname VARCHAR(255),Lname VARCHAR(255), phone_number int, Age INT, Email varchar(200))")
#mycursor.execute("CREATE TABLE appointment(appNo INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,startT VARCHAR(255) NOT NULL,endT VARCHAR(255) NOT NULL,dt varchar(255), name varchar(255))")

sql = "UPDATE DOCTOR SET id = %s WHERE id = %s"
val = (5, 1)

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record(s) affected") 
