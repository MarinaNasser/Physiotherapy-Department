from flask import Flask, render_template,request,session,url_for

print('started')

app = Flask(__name__)
# app.secret_key = "very secret key"
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="N#@98wrft45",
  database="sbe2024"
)

mycursor = mydb.cursor()

@app.route('/')
def base():
   print('base')
   return render_template('Base.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        userEmail = request.form['email']
        password = request.form['password']
        mycursor.execute("SELECT * FROM USERS WHERE email = %s AND password = %s",(userEmail,password))
        record = mycursor.fetchone()
        
        if record:
            # session['user'] = userEmail
            # session['loggedIn'] = True
            return render_template('base.html')
        else:
            print(111111)
            return render_template('login.html',msg = True)
    else:
        print(0000000)
        return render_template('login.html',msg = False)


@app.route('/signUp')
def signUp():
    return render_template('signUp.html')



@app.route('/adddoctor',methods = ['POST','GET'])
def adddoctor():
    if request.method == 'POST':
        name = request.form['name1']
        dep = request.form['dep1']
        sql = "INSERT INTo DOCTOR (name,department) VALUES (%s,%s)"
        val = (name,dep)
        mycursor.execute(sql,val)
        mydb.commit()
        return render_template('base.html')
    else:
        print('get')
        return render_template('adddoctor.html')


@app.route('/viewdoctor')
def viewdoctor():
   sql = "SELECT * FROM DOCTOR"
   mycursor.execute(sql)
   result = mycursor.fetchall()
   return render_template('viewdoctor.html',data = result)

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
      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('base.html')
   else:
      return render_template('addpatient.html')

@app.route('/viewpatient')
def viewpatient():
    mycursor.execute("SELECT * FROM Patient")
    myresult = mycursor.fetchall()

    return render_template('viewpatient.html', data=myresult)


@app.route('/contact_us')
def contact():
    return render_template('contact_us.html')


if __name__ == '__main__':
    app.run(debug = True)
