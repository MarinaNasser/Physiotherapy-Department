import email
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="magdynasr",
  database="sherif"
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE sbe2024")
# mycursor.execute("CREATE TABLE patient (Fname VARCHAR(255),Lname VARCHAR(255), phone_number int, Age INT, Email varchar(200))")
sql = "UPDATE DOCTOR SET id = %s WHERE id = %s"
val = (5, 1)

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record(s) affected") 
