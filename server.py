import email
from genericpath import exists
from unittest import result
from flask import Flask, redirect, render_template,request,session,url_for
from pymysql import NULL
from sqlalchemy import false
from flask_mysqldb import MySQL
import mysql.connector
import re

print('started')

app = Flask(__name__)
app.secret_key = "very secret key"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="magdynasr",
    database="sherif"
)

mycursor = mydb.cursor()

@app.route('/')
def base():
    print('')
    return render_template('startPage.html')

@app.route('/homePage')
def homePage():
    return render_template('homePage.html')

@app.route('/preSignUp')
def preSignUp():
    return render_template('preSignUp.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        userEmail = request.form['email']
        password = request.form['password']
        mycursor.execute("SELECT * FROM USERS WHERE email = %s AND password = %s",(userEmail,password))
        record = mycursor.fetchone()
        
        if record:
            if record[2] == 'patient':
                session['user_patient'] = userEmail
                session['loggedIn'] = True
                return redirect(url_for('homePage'))
            elif record[2] == 'doctor':
                session['user_doctor'] = userEmail
                session['loggedIn'] = True
                return redirect(url_for('homePage')) 
            else:
                session['user_admin'] = userEmail
                session['loggedIn'] = True
                return redirect(url_for('homePage'))      
        else:
            print(111111)
            return render_template('login.html',msg = True)
    else:
        print(0000000)
        return render_template('login.html',msg = False)

@app.route('/signUp')
def signUp():
    if request.method == 'GET':
        return render_template('signUp.html')
    else:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        
        mycursor.execute("INSET INTO USERS (email,password) VALUES (%s,%s)",(email,password))
        mydb.commit()
        
        session['name'] = name
        session['email'] = email
        return redirect(url_for('base'))

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('user',None)
    session.clear()
    # return render_template('Base.html')
    return redirect(url_for('base'))



@app.route('/adddoctor',methods = ['POST','GET'])
def adddoctor():

    if request.method == 'POST':

        #requesting data form
        name = request.form['name1']
        ssn=request.form['ssn']
        sex = request.form['sex']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        birth_date = request.form['birth_date']
        degree = request.form['degree']
        Specialization= request.form['specialization']
        salary = request.form['salary']

        #setting a buffered cursor => to accept one value in the input
        emailCursor =mydb.cursor(buffered=True)
        emailCursor.execute(""" SELECT * FROM doctor WHERE email = %s """ , (email,))
        emailExist = emailCursor.fetchone()

        ssnCursor =mydb.cursor(buffered=True)
        ssnCursor.execute(""" SELECT * FROM doctor WHERE ssn = %s """ , (ssn,))
        ssnExist = ssnCursor.fetchone()

        if emailExist and ssnExist :
            return render_template('adddoctor.html', emailExisits = True , ssnExisits=True)
        elif emailExist or ssnExist :
            if emailExist :
                return render_template('adddoctor.html', emailExisits = True , ssnExisits=False)
            else:
                return render_template('adddoctor.html', emailExisits = False , ssnExisits=True)        
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return render_template('adddoctor.html', emailExisits = False , emailInvalid=True )        
        else:    
            sql = """INSERT INTO doctor (name,ssn,sex,email,password,address,birth_date,degree,specialization,salary) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            val = (name,ssn,sex,email,password,address,birth_date,degree,Specialization,salary)
            mycursor.execute(sql,val)
            mydb.commit()
            return redirect(url_for('homePage'))
    else:
        print('get')
        return render_template('adddoctor.html')
        mycursor.close()

@app.route('/viewdoctor')
def viewdoctor():
    sql = "SELECT * FROM DOCTOR"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return render_template('viewdoctor.html',data = result)

@app.route('/adddevice')
def services():
    return render_template('adddevice.html')

@app.route('/doctors')
def doctors():
    return render_template('doctor.html')



@app.route('/addpatient', methods = ['POST', 'GET'])
def addpatient():
    if request.method == 'POST': ##check if there is post data
        id = request.form['id']
        name = request.form['name']
        ssn = request.form['ssn']
        sex = request.form['sex']
        email = request.form['email']
        userName =  request.form['userName']
        password = request.form['password']
        address = request.form['address']
        birthDate = request.form['birthDate']
        creditCard = request.form['creditCard']
        insuranceNumber = request.form['insuranceNumber']
        maritalStatus = request.form['maritalStatus']
        job = request.form['job']
        age = request.form['age']

        sql = """INSERT INTO Patient (id, name, ssn, sex, email, username, password, address, birth_date, credit_card, insurance_num, marital_status, job, age) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (id,name,ssn,sex,email,userName,password,address, birthDate, creditCard, insuranceNumber, maritalStatus, job, age)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('homePage'))
    else:
        print('get')
        return render_template('addpatient.html')

@app.route('/viewpatient')
def viewpatient():
    mycursor.execute("SELECT * FROM Patient")
    myresult = mycursor.fetchall()
    return render_template('viewpatient.html', data = myresult)


@app.route('/contact_us')
def contact():
    return render_template('contact_us.html')

@app.route('/homePage/profile')
def profile():
    if 'loggedIn' in session:
        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT * FROM USERS WHERE email = %s', (session['user_patient'],))
        result = cursor.fetchall()
        
        return render_template('profile.html', data = result)
    return redirect(url_for('homePage'))

@app.route('/adminViewDoctor')
def adminViewDoctor():
    sql = "SELECT * FROM DOCTOR"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return render_template('adminViewDoctor.html',result=result)        

if __name__ == '__main__':
    app.run(debug = True)    