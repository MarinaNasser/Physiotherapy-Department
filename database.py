import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123",
  database="sbe2024"
)

mycursor = mydb.cursor()
 
mycursor.execute("CREATE TABLE Doctor ( id INT AUTO_INCREMENT,name VARCHAR(255),department VARCHAR(255),PRIMARY KEY (id))")
mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x) 