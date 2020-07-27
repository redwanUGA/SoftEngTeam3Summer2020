from flask import Flask, render_template, url_for, flash, session, request, redirect, make_response
from flaskext.mysql import MySQL
import pymysql
from datetime import timedelta
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "caircocoders-ednalan-2020"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
 
global COOKIE_TIME_OUT
#COOKIE_TIME_OUT = 60*60*24*7 #7 days
COOKIE_TIME_OUT = 60*5 #5 minutes
 
#Database Configuration
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12341234'
app.config['MYSQL_DB'] = 'Bookstore'


@app.route('/login', methods=('GET', 'POST'))
def login():

    conn = None
    cursor = None
  
    _email = request.form['uname']
    _password = request.form['psw']

    if 'email' in request.cookies:
    username = request.cookies.get('email')
    password = request.cookies.get('password')
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM Users WHERE email=%s"
    sql_where = (username,)
    cursor.execute(sql, sql_where)
    row = cursor.fetchone()

    if row and check_password_hash(row[4], password):
        print(username + ' ' + password)
        session['email'] = row[3]
        cursor.close()
        conn.close()
        return redirect('/')
        else:
        return redirect('/login')

    # validate the received values
    elif _email and _password:
        #check user exists   
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM Users WHERE email=%s"
        sql_where = (_email,)
        cursor.execute(sql, sql_where)
        row = cursor.fetchone()
        if row:
            if check_password_hash(row[4], _password):
                session['email'] = row[3]
                cursor.close() 
                conn.close()
                return redirect('/')
                if _remember:
                resp = make_response(redirect('/'))
                resp.set_cookie('email', row[3], max_age=COOKIE_TIME_OUT)
                resp.set_cookie('password', _password, max_age=COOKIE_TIME_OUT)
                return resp
            return redirect('/')
    else:
    flash('Invalid Password!')
    return redirect('/login')
    else:
    flash('Invalid Email Or Password!')
    return redirect('/login')
    else:
    flash('Invalid Email Or Password!')
    return redirect('/login')
   
@app.route('/logout')
def logout():
 if 'email' in session:
  session.pop('email', None)
 return redirect('/')
  
if __name__ == '__main__':
 app.run(debug=True)









    return 'login'

