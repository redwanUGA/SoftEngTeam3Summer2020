from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from random import randint

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12341234'
app.config['MYSQL_DB'] = 'Bookstore'
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
    sqlstatement = "INSERT INTO `Bookstore`.`Users` " \
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
    querystatement = "SELECT email, password FROM `Bookstore`.`Users`" \
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


#---------------------------------------|
#     Start of Edit and View Profile    |
#---------------------------------------|
# -additonally the pages, viewprofile   |
#  and editprofile html were modified   |
#---------------------------------------|
@app.route('/view_profile', methods = ['GET', 'POST'])
def view_profile():
    cur = mysql.connection.cursor()
    #if not logged in show an empy profile page

    #assuming we are logged in as email@email.com
    val_email = "email@email.com"

    query = "SELECT userID, firstName, lastName, email, phone, Subscription FROM `Bookstore`.`Users`" \
                     "where email=\'%s\'" \
                     % (val_email)
    cur.execute(query)
    results = cur.fetchall()
    
    userID = results[0]['userID']

    addyQuery = "SELECT * FROM Bookstore.Address WHERE userID=%s" % (userID)
    cur.execute(addyQuery)
    addy = cur.fetchall()

    payQuery = "SELECT * FROM Bookstore.Payment WHERE userID=\'%s\'" % (userID)
    cur.execute(payQuery)
    pay = cur.fetchall()

    print(pay)
    
    if(len(addy) != 0 and len(pay) != 0):
        return render_template("viewprofile.html", user=results[0], addy=addy[0], pay=pay[0])
    elif(len(pay) != 0):
        return render_template("viewprofile.html", user=results[0], addy=addy, pay=pay[0])
    elif(len(addy) != 0):
        return render_template("viewprofile.html", user=results[0], addy=addy[0], pay=pay)
    else:
        return render_template("viewprofile.html", user=results[0], addy=addy, pay=pay)

@app.route('/edit_profile')
def editProfile():
    return render_template('editprofile.html')

@app.route('/editProfileData', methods=['GET','POST'])
def editProfileData():
    cur = mysql.connection.cursor()

    #----------important-------#
    #id of the logged in user
    userID = 212586
    #-----must be linked to the login form--------#
    
    #updated personal information
    query =""
    firstName = request.form['firstname']
    if(firstName!=""):
        query += "UPDATE Bookstore.Users SET firstName=\'%s\'" % (firstName)    
    lastName = request.form['lastname']
    if(lastName!=""):
        query += ", lastName=\'%s\'" % (lastName)
    phone = request.form['phone']
    if(phone!=""):
        query += ", phone=%d" % (int(phone))

    #user info update
    if(query != ""):
        query += " WHERE userID=%d" % (userID)
        cur.execute(query)
        mysql.connection.commit()

    
    #updated Address information
    address = []
    address.append(str(request.form['addyname']))
    address.append(str(request.form['street1']))
    address.append(str(request.form['street2']))
    address.append(str(request.form['city']))
    address.append(str(request.form['state']))
    address.append(str(request.form['zip']))
    address.append(str(request.form['country']))
    valid = True
    print(address)
    for x in range(len(address)):
        if(address[x] == "" and x != 2):
            valid=False
        
    if(valid):
        check = "SELECT * FROM Bookstore.Address WHERE userID=%s" % (userID)
        cur.execute(check)
        res = cur.fetchall()
        if(len(res) == 0):
            query = "INSERT INTO Bookstore.Address (idAddress, name, street, street2, zipCode, city,"\
                " state, country, userID) VALUES (%s, \'%s\', \'%s\', \'%s\', %s, \'%s\', \'%s\', \'%s\', %s)"\
                % (randint(0,999999),address[0], address[1], address[2], address[5], address[3], address[4], address[6], userID)

            cur.execute(query)
            mysql.connection.commit()
        else:
            query = "UPDATE Bookstore.address SET name=\'%s\', street=\'%s\', street2=\'%s\'," \
                " zipCode=%s, city=\'%s\', state=\'%s\', country=\'%s\' WHERE userID=\'%s\'" \
                % (address[0], address[1], address[2], address[5], address[3], address[4], address[6], userID)
            cur.execute(query)
            mysql.connection.commit()
    
    
    #updated payment info
    payment=[]
    payment.append(request.form['cardNum'])
    payment.append(request.form['expYear'])
    payment.append(request.form['expMonth'])
    valid = True
    for x in range(len(payment)):
        if(payment[x] == ''):
            valid = False
    if(valid):
        check = "SELECT * FROM Bookstore.Payment WHERE userID=%s" % (userID)
        cur.execute(check)
        res = cur.fetchall()
        if(len(res) == 0):
            query = "INSERT INTO Bookstore.Payment (cardNumber, expiryYear,"\
                " expiryMonth,securityCode, UserID, paymentType) VALUES (%s, %s, %s, %s, %s, \'%s\')" \
                % (payment[0], payment[1], payment[2], 000, userID, "type")
            cur.execute(query)
            mysql.connection.commit()
        else:
            query = "UPDATE Bookstore.Payment SET cardNumber=%s, expiryYear=%s,"\
                " expiryMonth=%s, paymentType=\'%s\' WHERE UserID=%s"\
                % (payment[0], payment[1], payment[2], "type", userID)
            cur.execute(query)
            mysql.connection.commit()
    return redirect(url_for('view_profile'))

#---------------------------------------|
#     END of Edit and View Profile      |
#---------------------------------------|

if __name__ == '__main__':
    app.run(debug=True)

