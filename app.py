from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from random import randint

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12341234'
app.config['MYSQL_DB'] = 'bookstore'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'thisissecret'
mysql = MySQL(app)


##### Menu Options ######

#HomePage
@app.route('/')
def index():
    return render_template('index.html')


# Login Page
@app.route('/login')
def login():
    return render_template('login.html')


# Register Page
@app.route('/register')
def register():
    return render_template('register.html')

# Cart Page
@app.route('/cart')
def cart():
    return render_template('cart.html')


# Show Books
# @@ Get from Database
@app.route('/book/<int:book_num>')
def bookshow(book_num):
    book_title = ["Software Engineering", "Computer Networks", "C How to program", "Data Mining", "Operating System", "Rome History"]
    book_author = ["SommerVille", "Andrew S Tanenbaum", "Dietel", "Vipin Kumar", "Greg Gagne", "John Smith"]
    book_price = ["$15", "$25", "$40", "$50", "$18", "$15"]
    book_dir = ["../static/images/books/05.jpg",
                "../static/images/books/06.jpg",
                "../static/images/books/03.jpg",
                "../static/images/books/02.jpg",
                "../static/images/books/04.jpg",
                "../static/images/books/01.jpg"]

    infopass = {'book_title': book_title[book_num-1],
                'book_author': book_author[book_num-1],
                'book_price': book_price[book_num-1],
                'book_dir': book_dir[book_num-1]}
    # print(infopass)
    return render_template('book.html', infopass=infopass)

##### Actions #####

@app.route('/register_data', methods = ['GET', 'POST'])
def register_data():
    cur = mysql.connection.cursor()
    val_userID = randint(0,999999)
    val_firstName = request.form['firstname']
    val_lastName = request.form['firstname']
    val_password = request.form['password']
    val_email = request.form['emailid']
    val_phone = 470394
    sqlstatement = "INSERT INTO `bookstore`.`users` " \
                   "(`userID`, `firstName`, `lastName`, `password`, `email`, `phone`, `userTypeID`, `Subscription`)" \
                   'VALUES ( %d, \'%s\', \'%s\', \'%s\', \'%s\', %d, 1, 1 ) ;' \
                   % (val_userID, val_firstName, val_lastName, val_password, val_email, val_phone)
    cur.execute(sqlstatement)
    mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/login_action', methods = ['GET', 'POST'])
def login_action():
    cur = mysql.connection.cursor()
    val_email = request.form['email']
    val_password = request.form['psw']
    querystatement = "SELECT email, password FROM `bookstore`.`users`" \
                     "where email=\'%s\' AND password=\'%s\'" \
                     % (val_email, val_password)
    cur.execute(querystatement)
    results = cur.fetchall()

    if len(results) == 0:
        flash('Invalid Email or Password')
        return redirect(url_for('login'))
    else:
        flash('You are Logged in as %s' % val_email)
        return redirect(url_for('index'))
        pass




if __name__ == '__main__':
    app.run(debug=True)

