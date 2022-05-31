import email
import pandas as pd
from datetime import datetime
from genericpath import exists
from unittest import result
from flask import Flask, redirect, render_template,request,session,url_for
# from pymysql import NULL
# from sqlalchemy import false
# from flask_mysqldb import MySQL
import mysql.connector
import re
import os
import secrets
# import sqlalchemy

app = Flask(__name__)
app.secret_key = "very secret key"
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Ahmed9112",
    database="hospital"
)
mycursor = mydb.cursor()

@app.route('/')
@app.route('/home')

def index():
    sql = "SELECT name,id FROM DOCTOR"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return render_template("index.html",data = result)

# ------------------------------------------------------------------------Pre Sign Up---------------------------------------------------------------------
@app.route('/preSignUp')
def preSignUp():
    return render_template('preSignUp.html')

# ------------------------------------------------------------------------My Tips---------------------------------------------------------------------
@app.route('/myTips')
def myTips():
    return render_template('myTips.html')

# ------------------------------------------------------------------------Profile and more info---------------------------------------------------------------------
@app.route('/profileh')
def profileh():
    if 'loggedIn' in session and 'user_patient' in session :
        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT * FROM patient WHERE email = %s', (session['user_patient'],))
        result = cursor.fetchall()
    elif 'loggedIn' in session and 'user_doctor' in session :
        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT * FROM doctor WHERE email = %s', (session['user_doctor'],))
        result = cursor.fetchall()
    else:
        return render_template('profileh.html')

    return render_template('profileh.html',data = result)

@app.route('/moreInfo')
def moreInfo():
    return render_template('moreInfo.html')

# ------------------------------------------------------------------------Login---------------------------------------------------------------------

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
                return redirect(url_for('index'))
            elif record[2] == 'doctor':
                session['user_doctor'] = userEmail
                session['loggedIn'] = True
                return redirect(url_for('index')) 
            else:
                session['user_admin'] = userEmail
                session['loggedIn'] = True
                return redirect(url_for('index'))      
        else:
            return render_template('login.html',msg = True)
    else:
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
        return redirect(url_for('index'))

# ------------------------------------------------------------------------Log Out-------------------------------------------------------------------

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('user',None)
    session.clear()
    # return render_template('Base.html')
    return redirect(url_for('index'))

# ------------------------------------------------------------------------Add Doctor----------------------------------------------------------------

@app.route('/adddoctor',methods = ['POST','GET'])
def adddoctor():

    if request.method == 'POST':

        #requesting data form

        name = request.form['name']
        ssn=request.form['ssn']
        sex = request.form['sex']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        birth_date = request.form['birth_date']
        degree = request.form['degree']
        Specialization= request.form['specialization']
        phone = request.form['phone']
        photo = request.files['photo']
        pic_path = save_picture(photo)

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
            sql = """INSERT INTO doctorPreRequest (name,ssn,sex,email,password,address,birth_date,degree,specialization,phone,photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            val = (name,ssn,sex,email,password,address,birth_date,degree,Specialization,phone,pic_path)
            mycursor.execute(sql,val)
            mydb.commit()
            return redirect(url_for('index'))
    else:
        print('get')
        return render_template('adddoctor.html')
        mycursor.close()

# ------------------------------------------------------------------------View Doctor---------------------------------------------------------------------

@app.route('/viewdoctor')
def viewdoctor():
    sql = "SELECT * FROM DOCTOR"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return render_template('viewdoctor.html',data = result)

# ------------------------------------------------------------------------Add Device----------------------------------------------------------------

def save_picture(form_picture):
    fname = secrets.token_hex(16) #new name
    _, f_ext = os.path.splitext(form_picture.filename) #get rid of old name
    picture_fn = fname + f_ext #combine extention "png for example" with new name
    picture_path = os.path.join( 'static/imgs/uploads', picture_fn) #combine path with name
    picture_path = picture_path.replace('\\','/')
    form_picture.save(picture_path)
    return picture_path

@app.route('/adddevice', methods = ['GET','POST'])

def adddevice():
    if request.method == 'POST':
        if request.form:
            device_number = request.form['device_num']
            device_name = request.form['device_name']
            device_model = request.form['device_model']
            technician_id = request.form['technician_id']
            count = request.form['count']
            description = request.form['description']
            photo = request.files['photo']
            pic_path = save_picture(photo)
            
            sql = """INSERT INTO device (device_num,device_name,device_model,technician_id,photo,count,description) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            val = (device_number,device_name,device_model,technician_id,pic_path,count,description)
            mycursor.execute(sql,val)
            mydb.commit()
            return redirect(url_for('index'))
    return render_template('adddevice.html')
        
# ------------------------------------------------------------------------Doctors-------------------------------------------------------------------        

@app.route('/doctors')
def doctors():
    return render_template('doctor.html')

# ------------------------------------------------------------------------Add Patient---------------------------------------------------------------
@app.route('/addpatient', methods = ['POST', 'GET'])
def addpatient():
    if request.method == 'POST': ##check if there is post data
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
        photo = request.files['photo']
        pic_path = save_picture(photo)

        sql = """INSERT INTO Patient (name, ssn, sex, email, username, password, address, birth_date, credit_card, insurance_num, marital_status, job, photo) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (name,ssn,sex,email,userName,password,address, birthDate, creditCard, insuranceNumber, maritalStatus, job, pic_path)
        mycursor.execute(sql, val)
        mydb.commit()

        sql1 = """INSERT INTO Patient (email, password, kind) VALUES (%s, %s, %s)"""
        val1 = (email,password,'patient')
        mycursor.execute(sql1, val1)
        mydb.commit()


        return redirect(url_for('index'))
    else:
        print('get')
        return render_template('addpatient.html')

# ------------------------------------------------------------------------View Patient---------------------------------------------------------------

@app.route('/viewpatient')
def viewpatient():
    mycursor.execute("SELECT * FROM Patient")
    myresult = mycursor.fetchall()
    return render_template('viewpatient.html', data = myresult)

# ------------------------------------------------------------------------Contact Us-----------------------------------------------------------------

@app.route('/contact_us')
def contact():
    return render_template('contact_us.html')


# ------------------------------------------------------------------------Home Page/ Profile---------------------------------------------------------

@app.route('/index/profile')
def profile():
    if 'loggedIn' in session:
        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT * FROM USERS WHERE email = %s', (session['user_patient'],))
        result = cursor.fetchall()
        
        return render_template('profile.html', data = result)
    return redirect(url_for('index'))

# ------------------------------------------------------------------------Admin Veiw Doctor---------------------------------------------------------

@app.route('/adminViewDoctor', methods = ['POST','GET'])
def adminViewDoctor():
    if request.method == 'POST'and "ssn" in request.form:

        name = request.form['name']
        ssn=request.form['ssn']
        sex = request.form['sex']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        birth_date = request.form['birth_date']
        degree = request.form['degree']
        Specialization= request.form['specialization']
        phone = request.form['phone']
        photo = request.form['photo']



        sql = """INSERT INTO doctor (name,ssn,sex,email,password,address,birth_date,degree,specialization,phone,photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        val = (name,ssn,sex,email,password,address,birth_date,degree,Specialization,phone,photo)
        mycursor.execute(sql,val)
        mydb.commit()
        
        sql = """INSERT INTO users (email,password,kind) VALUES (%s,%s,%s)"""
        val = (email,password,'doctor')
        mycursor.execute(sql,val)
        mydb.commit()



        cursor = mydb.cursor(buffered=True)
        cursor.execute("""DELETE FROM doctorPreRequest WHERE ssn = %s """,(ssn,))
        mydb.commit()  
        return redirect(url_for('adminViewDoctor'))

    if request.method == 'POST' and "ssnref" in request.form:

        nameref = request.form['nameref']
        ssnref=request.form['ssnref']
        
        # sql = """INSERT INTO test (name,ssn) values (%s,%s)"""
        # val = (nameref,ssnref)
        # cursor = mydb.cursor(buffered=True)
        # cursor.execute(sql,val)
        # mydb.commit()


        # sex = request.form['sex']
        # email = request.form['email']
        # password = request.form['password']
        # address = request.form['address']
        # birth_date = request.form['birth_date']
        # degree = request.form['degree']
        # Specialization= request.form['specialization']
        # salary = request.form['salary']

        cursor = mydb.cursor(buffered=True)
        cursor.execute(""" DELETE FROM doctorPreRequest WHERE ssn = %s """,(ssnref,))
        mydb.commit()
        return redirect(url_for('adminViewDoctor'))
    else:
        print('get')    
        
    sql = "SELECT * FROM doctorPreRequest"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return render_template('adminViewDoctor.html',result=result)        

# ------------------------------------------------------------------------add/view appointment----------------------------------------------------------------
@app.route('/addAppointment',methods=['GET','POST'])
def addAppointment():
    # print(session['user_doctor'])
    sql = "SELECT * FROM appointment"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    
    if request.method == 'POST':
        #requesting data form
        startT = request.form['startT']
        endT  = request.form['endT']
        date = request.form['date']
        
        sql = """INSERT INTO appointment (startT, endT, dt,doctorEmail,booked) VALUES (%s, %s, %s,%s,%s)"""
        val = (startT,endT,date,session['user_doctor'],0)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('addAppointment.html', added =True)
    else:
        return render_template('addAppointment.html',added = False)

@app.route('/viewAppointments')   
def viewAppointments():
    sql = "SELECT appNo,name,startT,endT,dt FROM appointment join doctor on doctorEmail = email"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return render_template('viewAppointments.html', data = result)

# ------------------------------------------------------------------------book now----------------------------------------------------------------

@app.route('/bookNow',methods = ['GET','POST'])
def bookNow():
    sql = "SELECT appNo,name,startT,endT,dt,booked FROM appointment join doctor on doctorEmail = email"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(result)
    
    list_of_tuples = pd.DataFrame(result)
    list_of_tuples[4] = pd.to_datetime(list_of_tuples[4],format="%d-%m-%Y")
    
    # print((datetime.now() - list_of_tuples[4][0]).days)
    print(list_of_tuples)
    
    if request.method == 'POST':
        appNo = request.form['appNo']
        sql = """UPDATE appointment
        SET patientEmail = %s,
        booked = %s
        WHERE appNo = %s"""
        
        value = (session['user_patient'],1,appNo)
        mycursor.execute(sql,value)
        mydb.commit()
        
        sql = "SELECT appNo,name,startT,endT,dt,booked FROM appointment join doctor on doctorEmail = email"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        list_of_tuples = pd.DataFrame(result)
        list_of_tuples[4] = pd.to_datetime(list_of_tuples[4],format="%d-%m-%Y")
        
        return render_template('bookNow.html',data = list_of_tuples,now = datetime.now().date(),booked = True)
    else:
        return render_template('bookNow.html',data = list_of_tuples,now = datetime.now().date(),booked = False)

# @app.route('/confirmBooking',methods = ['GET','POST'])
# def confirmBooking():


# ------------------------------------------------------------------------test----------------------------------------------------------------

@app.route('/messages', methods = ['GET','POST'])
def messages():
    if request.method == 'POST':
        emailTo = request.form['emailTo']
        emailFrom=request.form['emailFrom']
        title = request.form['title']
        message = request.form['message']

        sql = """INSERT INTO messages (emailTo,emailFrom,title,message) VALUES (%s,%s,%s,%s)"""
        val = (emailTo,emailFrom,title,message)
        mycursor.execute(sql,val)
        mydb.commit()

    return render_template('messages.html')

# ------------------------------------------------------------------------test----------------------------------------------------------------
@app.route('/inbox', methods = ['POST','GET'])
def inbox():
    if request.method == 'POST'and "deleteMessage" in request.form:
        deleteMessage = request.form['deleteMessage']

        cursor = mydb.cursor(buffered=True)
        cursor.execute(""" DELETE FROM messages WHERE id = %s """,(deleteMessage,))
        mydb.commit()
        return redirect(url_for('inbox'))

    sql = """Select * from messages where emailTo = %s"""
    val = (session['user_patient'],)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    return render_template('inbox.html',result=result)

# ------------------------------------------------------------------------test----------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug = True)
