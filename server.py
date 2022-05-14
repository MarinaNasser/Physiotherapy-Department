import mysql.connector
from flask import Flask, redirect, url_for, request,render_template


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123",
  database="sbe2024"
)

mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def hello_name():
   return render_template('index.html')

@app.route('/addpatient',methods = ['POST', 'GET'])
def addpatient():
   if request.method == 'POST': ##check if there is post data
      Fn = request.form['PatientFName']
      Ln = request.form['PatientLName']
      pn = request.form['Phone number']
      ad = request.form['Address']
      c =  request.form['City']
      a = request.form['Age']
      e = request.form['Email']
      dr =request.form['Doctor name']
      p= request.form['Problem']
      # print(n,d)
      sql = "INSERT INTO Patient (Fname,Lname, phone number, Age, Email) VALUES (%s, %s, %s , %s, %s)"
      val = (Fn,Ln,pn,ad,c,a,e,dr,p)
      # mycursor.execute(sql, val)
      # mydb.commit()   
      return render_template('index.html')
   else:
      return render_template('addpatient.html')

@app.route('/viewpatient')
def viewdoctor():
   mycursor.execute("SELECT * FROM Doctor")
   myresult = mycursor.fetchall()

   return render_template('viewpatient.html', data=myresult)

if __name__ == '__main__':
   app.run()
