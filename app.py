from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, g
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from random import randint
import functools
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
# from simplecrypt import encrypt, decrypt
from cryptography.fernet import Fernet


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12341234'
app.config['MYSQL_DB'] = 'bookstore'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'abcdabcd'

app.config.update(DEBUG=True, MAIL_SERVER='box5928.bluehost.com',
                  MAIL_PORT=465, MAIL_USE_SSL=True, MAIL_USERNAME = 't3@myw.urq.mybluehost.me',
                  MAIL_PASSWORD = '78rehkas')

mail = Mail(app)
mysql = MySQL(app)

key = b'fRmBje4ZejoeBPmxESfU2ElslhIcjiose6rHt4qaV4c='
fenc = Fernet(key=key)

def conv_int(a):
    try:
        int(a)
        return int(a)
    except ValueError:
        return 0


##### Menu Options ######

#HomePage
@app.route('/')
def index():
    return render_template('index.html')


# Login Page
@app.route('/login')
def login():
    if session['logged_in'] and session['uid']:
        flash('You are already logged in')
        return redirect(url_for('index'))
    else:
        session['logged_in'] = False
        user_logged_in_id = None
        user_logged_in_pdata = None
        user_logged_in_sadata = None
        return render_template('login.html')



# Register Page
@app.route('/register')
def register():
    if session['logged_in'] and session['uid']:
        flash('Logout first')
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

# Cart Page
@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/view_profile')
def view_profile():
    if session.get('logged_in'):
        return render_template('viewprofile.html')
    else:
        return redirect(url_for('index'))


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

    val_firstName = str(request.form['fname']).strip()
    val_lastName = str(request.form['lname']).strip()
    val_gender = str(request.form.get('gender')).strip()
    val_email = str(request.form['email']).strip().lower()
    val_password = generate_password_hash(str(request.form['password']).strip())
    val_phone = str(request.form.get('phonenumbercountry') + request.form['mainphonenumber']).strip()
    val_activationKey = randint(0,999999)

    val_streetaddress = str(request.form['streetaddress']).strip()
    val_aptno = str(request.form['aptno']).strip()
    val_inputCity = str(request.form['inputCity']).strip()
    val_inputState = str(request.form.get('inputState')).strip()
    val_inputZip = conv_int(request.form['inputZip'])

    val_nameoncard = str(request.form['nameoncard']).strip()
    val_cardno = str(request.form['cardno']).strip()
    val_CVV = conv_int(request.form['CVV'])
    val_cardtype = request.form.get('cardtype')
    val_expmonth = int(request.form.get('expmonth'))
    val_expyear = int(request.form.get('expyear'))

    val_billstreetaddress = str(request.form['billstreetaddress']).strip()
    val_billaptno = str(request.form['billaptno']).strip()
    val_billinputCity = str(request.form['billinputCity']).strip()
    val_billinputState = str(request.form.get('billinputState')).strip()
    val_billinputZip = conv_int(request.form['billinputZip'])


    #mandatory insert
    sqlstatementman = "INSERT INTO `bookstore`.`users`" \
                   "(`firstName`, `lastName`, `password`, " \
                   "`email`, `phone`, `userTypeID`, " \
                   "`Subscription`, `active`, `activationKey`, " \
                   "`suspended`, `gender`)" \
                   "VALUES (\'%s\', \'%s\', \'%s\', " \
                   "\'%s\', \'%s\', 2, " \
                   "1, 0, \'%d\', " \
                   "0, \'%s\' );" \
                   % ( val_firstName, val_lastName, val_password, \
                       val_email, val_phone, \
                       val_activationKey, \
                       val_gender)
    cur.execute(sqlstatementman)
    mysql.connection.commit()
    userid = cur.lastrowid

    #shipping address insert
    if len(val_streetaddress) != 0 or  len(val_aptno) != 0 or len(val_inputCity) != 0 or val_inputZip != 0:
        val_name = val_firstName + ' ' + val_lastName
        insert_address = "INSERT INTO `bookstore`.`address`" \
                "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'ship', \'%d\');" \
                 % (val_name, val_streetaddress, val_aptno, val_inputZip, val_inputCity, val_inputState, userid)

        cur.execute(insert_address)
        mysql.connection.commit()

    #card info insert
    if len(val_nameoncard) != 0 or len(val_cardno) != 0 or val_CVV != 0:
        insert_cardinfo = "INSERT INTO `bookstore`.`payment`" \
                    "(`cardNumber`, `expiryYear`, `expiryMonth`, `securityCode`, `paymentType`, `UserID`, `nameoncard`)" \
                    "VALUES( \'%s\' , \'%d\', \'%d\', \'%d\' , \'%s\', \'%d\', \'%s\' );" \
                    % (val_cardno, val_expyear, val_expmonth, val_CVV, val_cardtype, userid, val_nameoncard)

        # print(insert_cardinfo)
        cur.execute(insert_cardinfo)
        mysql.connection.commit()

    # billing address insert
    if len(val_billstreetaddress) != 0 or len(val_billaptno) != 0 or len(val_billinputCity) != 0 or val_billinputZip != 0:
        val_name = val_firstName + ' ' + val_lastName
        insert_billaddress = "INSERT INTO `bookstore`.`address`" \
                             "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                             "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'bill', \'%d\');" \
                             % (val_nameoncard, val_billstreetaddress, val_billaptno, val_billinputZip, val_billinputCity, val_billinputState,
                                userid)

        cur.execute(insert_billaddress)
        mysql.connection.commit()

    msgg = Message("Team3 Book Store", sender="t3@myw.urq.mybluehost.me", recipients=[val_email])
    msgg.body = '''Thank you for registering, ... 
                to activate your account ... 
                sign in with your password and ...
                you have to enter the following code when logging in : %s ''' % str(val_activationKey)

    mail.send(msgg)
    return redirect(url_for('index'))

@app.route('/login_action', methods = ['GET', 'POST'])
def login_action():
    cur = mysql.connection.cursor()
    # get email and password from form
    val_email = request.form['email']
    val_password = request.form['psw']

    # see if remember me is checcked
    val_rem = request.form.getlist('remember')

    # search for email and password in database
    querystatement = "SELECT * FROM `bookstore`.`users`" \
                     "where email=\'%s\' " % (val_email)
    cur.execute(querystatement)
    results = cur.fetchall()

    #storing email in session
    if len(val_rem) == 1 and len(results) != 0:
        session['email'] = val_email
    else:
        session.pop('email', None)

    #email match action
    if len(results) == 0:
        flash('Invalid Email or Password')
        return redirect(url_for('login'))
    elif not check_password_hash(results[0]['password'], val_password):
        flash('Invalid Email or Password')
        return redirect(url_for('login'))
    elif results[0]['active'] == 0:
        return redirect(url_for('activate_user_start'))
    else:

        session['logged_in'] = True
        flash('You are Logged in as %s' % val_email)

        if results[0]['userTypeID'] == 1:
            session['usertype'] = 1
            uid = results[0]['userID']
            session['uid'] = uid
            return render_template('admin.html')
        else:
            session['usertype'] = 2
            uid = results[0]['userID']
            session['uid'] = uid
            personalinfoquery = "SELECT * FROM `bookstore`.`users` WHERE `userID` = %d" % uid
            shippingaddressinfoquery = "SELECT * FROM `bookstore`.`address` WHERE `userID` = %d and `AddressType`='ship' "  % uid
            billingaddressinfoquery = "SELECT * FROM `bookstore`.`address` WHERE `userID` = %d and `AddressType`='bill' " % uid
            paymentinfoquery = "SELECT * FROM `bookstore`.`payment` WHERE `UserID` = %d" % uid

            cur.execute(personalinfoquery)
            personaldata = cur.fetchall()
            cur.execute(shippingaddressinfoquery)
            shippingaddressdata = cur.fetchall()
            cur.execute(billingaddressinfoquery)
            billingaddressdata = cur.fetchall()
            cur.execute(paymentinfoquery)
            paymentinfo = cur.fetchall()


            return render_template('viewprofile.html', pdata = personaldata,
                               sadata = shippingaddressdata,
                               badata = billingaddressdata,
                               paydata = paymentinfo)


@app.route('/logout')
def logout():
    if session['logged_in'] == True:
        session['logged_in'] = False
        session['uid'] = None
        flash('You are successfully logged out')
        return redirect(url_for('index'))
    else:
        flash('You are already logged out')
        return redirect(url_for('index'))

@app.route('/password_recover_start')
def password_recover_start():
    return render_template('password_recover_1.html')

@app.route('/send_otp', methods = ['GET', 'POST'])
def send_otp():
    cur = mysql.connection.cursor()
    # get email and password from form
    val_email = request.form['email']
    search_email_query = "SELECT * FROM `bookstore`.`users`" \
                         "where email=\'%s\' " % (val_email)
    cur.execute(search_email_query)
    results = cur.fetchall()
    print(results)
    if results:
        update_id = results[0]['userID']
        new_activation_key = randint(0,99999)
        update_activation_key = "UPDATE `bookstore`.`users` " \
                                "SET `activationKey` = %d " \
                                "WHERE (`userID` = %d)" \
                                % (new_activation_key, update_id)
        cur.execute(update_activation_key)
        mysql.connection.commit()

        msgg = Message("Team3 Book Store", sender="t3@myw.urq.mybluehost.me", recipients=[val_email])
        msgg.body = ''' We have sent you a one time password to recover your password %s ''' % str(new_activation_key)

        mail.send(msgg)

        return render_template('password_recover_2.html')
    else:
        flash('Email not found in system')
        return redirect(url_for('password_recover_start'))

@app.route('/password_recovery_finished', methods = ['GET', 'POST'])
def password_recovery_finished():
    cur = mysql.connection.cursor()
    val_email = request.form['email']
    val_otp = int(request.form['OTP'])
    val_newpass = request.form['newpass']
    val_rnewpass = request.form['rnewpass']
    stage_1_conf = "SELECT email, activationKey FROM `bookstore`.`users`" \
                    "where email=\'%s\' AND activationKey=\'%d\'" \
                    % (val_email, val_otp)
    if stage_1_conf:
        if val_newpass == val_rnewpass:
            password_change = "UPDATE `bookstore`.`users` " \
                               "SET `password` = \'%s\' " \
                               "WHERE (`email` = \'%s\')" \
                                % (generate_password_hash(val_newpass), val_email)
            cur.execute(password_change)
            mysql.connection.commit()
            flash('Password Successfully Changed')

            msgg = Message("Team3 Book Store", sender="t3@myw.urq.mybluehost.me", recipients=[val_email])
            msgg.body = ''' You have successfully changed your password '''
            mail.send(msgg)

            return redirect(url_for('login'))
        else:
            flash('Retyeped Password Did Not Match')
            return render_template('password_recover_2.html')
    else:
        flash('OTP did not match')
        return redirect(url_for('login'))


@app.route('/activate_user_start')
def activate_user_start():
    return render_template('activate.html')

@app.route('/activate_user_action', methods = ['GET', 'POST'])
def activate_user_action():
    cur = mysql.connection.cursor()


    val_email = request.form['email']
    val_otp = request.form['otp']

    find_user = "SELECT * FROM `bookstore`.`users`" \
                "where email=\'%s\' " % (val_email)

    cur.execute(find_user)
    res = cur.fetchall()

    if len(res) == 0:
        flash('Wrong Email')
        return redirect(url_for('login'))
    elif conv_int(val_otp) != res[0]['activationKey']:
        flash('Wrong Activation Key')
        return redirect(url_for('login'))
    else:
        activation_change = "UPDATE `bookstore`.`users` " \
                          "SET `active` = '1' " \
                          "WHERE (`email` = \'%s\')" \
                          % val_email

        cur.execute(activation_change)
        mysql.connection.commit()

        msgg = Message("Team3 Book Store", sender="t3@myw.urq.mybluehost.me", recipients=[val_email])
        msgg.body = "You have been activated. Use your password to login"

        mail.send(msgg)

        flash('User Successfully activated')
        return redirect(url_for('login'))


@app.route('/edit_profile')
def edit_profile():
    return render_template('editprofile.html')

@app.route('/editProfileData', methods=['GET','POST'])
def editProfileData():
    cur = mysql.connection.cursor()

    # ----------important-------#
    # id of the logged in user
    userID = session['uid']
    # -----must be linked to the login form--------#

    # updated personal information
    query = ""
    firstName = request.form['firstname']
    if (firstName != ""):
        query += "UPDATE Bookstore.Users SET firstName=\'%s\'" % (firstName)
    lastName = request.form['lastname']
    if (lastName != ""):
        query += ", lastName=\'%s\'" % (lastName)
    phone = request.form['phone']
    if (phone != ""):
        query += ", phone=%d" % (int(phone))

    # user info update
    if (query != ""):
        query += " WHERE userID=%d" % (userID)
        cur.execute(query)
        mysql.connection.commit()

    # updated Address information
    address = []
    address.append(str(request.form['addyname']))
    address.append(str(request.form['street1']))
    address.append(str(request.form['street2']))
    address.append(str(request.form['city']))
    address.append(str(request.form['state']))
    address.append(str(request.form['zip']))
    valid = True
    print(address)
    for x in range(len(address)):
        if (address[x] == "" and x != 2):
            valid = False

    if (valid):
        check = "SELECT * FROM Bookstore.Address WHERE userID=%s" % (userID)
        cur.execute(check)
        res = cur.fetchall()
        if (len(res) == 0):
            query = "INSERT INTO Bookstore.Address (idAddress, name, street, street2, zipCode, city," \
                    " state, userID) VALUES (%s, \'%s\', \'%s\', \'%s\', %s, \'%s\', \'%s\', \'%s\', %s)" \
                    % (randint(0, 999999), address[0], address[1], address[2], address[5], address[3], address[4], userID)

            cur.execute(query)
            mysql.connection.commit()
        else:
            query = "UPDATE Bookstore.address SET name=\'%s\', street=\'%s\', street2=\'%s\'," \
                    " zipCode=%s, city=\'%s\', state=\'%s\', WHERE userID=\'%s\'" \
                    % (address[0], address[1], address[2], address[5], address[3], address[4], userID)
            cur.execute(query)
            mysql.connection.commit()

    # updated payment info
    payment = []
    payment.append(request.form['cardNum'])
    payment.append(request.form['expYear'])
    payment.append(request.form['expMonth'])
    valid = True
    for x in range(len(payment)):
        if (payment[x] == ''):
            valid = False
    if (valid):
        check = "SELECT * FROM Bookstore.Payment WHERE userID=%s" % (userID)
        cur.execute(check)
        res = cur.fetchall()
        if (len(res) == 0):
            query = "INSERT INTO Bookstore.Payment (cardNumber, expiryYear," \
                    " expiryMonth,securityCode, UserID, paymentType) VALUES (%s, %s, %s, %s, %s, \'%s\')" \
                    % (payment[0], payment[1], payment[2], 000, userID, "type")
            cur.execute(query)
            mysql.connection.commit()
        else:
            query = "UPDATE Bookstore.Payment SET cardNumber=%s, expiryYear=%s," \
                    " expiryMonth=%s, paymentType=\'%s\' WHERE UserID=%s" \
                    % (payment[0], payment[1], payment[2], "type", userID)
            cur.execute(query)
            mysql.connection.commit()
    return redirect(url_for('view_profile'))


if __name__ == '__main__':
    app.run(debug=True)

