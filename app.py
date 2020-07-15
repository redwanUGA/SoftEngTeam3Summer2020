from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from random import randint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/bookstore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    userID = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(32))
    emailId = db.Column(db.String(255))
    firstName = db.Column(db.String(45))
    lastName = db.Column(db.String(45))
    phone = db.Column(db.Integer)
    userStatus = db.Column(db.String(32))
    SubscriptionID = db.Column(db.Integer)
    userType = db.Column(db.String(45))
    Addres_userID = db.Column(db.Integer)
    PromotionID = db.Column(db.Integer)
    Cart_userID = db.Column(db.Integer)

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
    val_userID = randint(0,9999999)
    val_password = request.form['password']
    val_emailid = request.form['emailid']
    val_firstName = request.form['firstname']
    val_lastName = request.form['lastname']
    val_phone = request.form['phonenumbercountry'] + request.form['mainphonenumber']
    val_userStatus = 'Inactive'
    val_SubscriptionID = '1'
    val_userType = 'Registered'
    val_Addres_userID = val_userID
    val_PromotionId = '0'
    val_Cart_userID = '0'
    passdat = users(userID = val_userID,
                    password = val_password,
                    emailId = val_emailid,
                    firstName = val_firstName,
                    lastName = val_lastName,
                    phone = val_phone ,
                    userStatus = val_userStatus,
                    SubscriptionID = val_SubscriptionID,
                    userType = val_userType,
                    Addres_userID = val_Addres_userID,
                    PromotionID = val_PromotionId,
                    Cart_userID = val_Cart_userID)

    db.session.add(passdat)
    db.session.commit()
    return render_template('dummyshowval.html', data = passdat)



if __name__ == '__main__':
    app.run(debug=True)

