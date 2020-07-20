from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from random import randint
import functools
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
# from simplecrypt import encrypt, decrypt
from cryptography.fernet import Fernet
import re

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12341234'
app.config['MYSQL_DB'] = 'bookstore'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'abcdabcd'

app.config.update(DEBUG=True, MAIL_SERVER='box5928.bluehost.com',
                  MAIL_PORT=465, MAIL_USE_SSL=True, MAIL_USERNAME='t3@myw.urq.mybluehost.me',
                  MAIL_PASSWORD='78rehkas')

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


def check_goodness(value, fieldname):
    if fieldname == 'firstName' or fieldname == 'lastName':
        if len(value) < 45:
            return True
        else:
            return False

    if fieldname == 'email':
        regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex_email, value) != None and len(value) < 45:
            return True
        else:
            return False

    if fieldname == 'password':
        if len(value) < 8 or len(value) > 100:
            return False
        else:
            return True

    if fieldname == 'phone':
        regex_phone = '^\([0-9]{3}\)-[0-9]{3}-[0-9]{4}$'
        if re.search(regex_phone, value):
            return True
        else:
            return False

    if fieldname == 'name' or fieldname == 'street' or fieldname == 'nameoncard':
        if len(value) < 90:
            return True
        else:
            return False

    if fieldname == 'street2':
        if len(value) < 30:
            return True
        else:
            return False

    if fieldname == 'zipCode' or fieldname == 'securityCode':
        if value == 0:
            return False
        else:
            return True

    if fieldname == 'city':
        if len(value) < 15:
            return True
        else:
            return False

    if fieldname == 'cardNumber':
        regex_card = '(?:[0-9]{4}-){3}[0-9]{4}'
        if re.search(regex_card, value):
            return True
        else:
            return False


def error_message(value, fieldname):
    message = []

    if fieldname == 'firstName' or fieldname == 'lastName':
        if len(value) > 45:
            message.append('Too Long First Name or Last Name.')

    if fieldname == 'email':
        regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex_email, value) == None:
            message.append('Invalid Email.')

        if len(value) > 45:
            message.append('Too Long Email.')

    if fieldname == 'password':
        if len(value) < 8:
            message.append('Password should be minimum 8 characters.')
        elif len(value) > 100:
            message.append('Too Long Password.')

    if fieldname == 'phone':
        regex_phone = '^\([0-9]{3}\)[0-9]{3}-[0-9]{4}$'
        if re.search(regex_phone, value) == None:
            message.append('Invalid Phone Number. Maintain the format (XXX)-XXX-XXXX.')

    if fieldname == 'name':
        if len(value) > 90:
            message.append('Too Long Address Name.')

    if fieldname == 'street':
        if len(value) > 90:
            message.append('Too Long Street Address.')

    if fieldname == 'nameoncard':
        if len(value) > 90:
            message.append('Too Long Name on Card.')

    if fieldname == 'street2':
        if len(value) > 30:
            message.append('Too Long Apt No.')

    if fieldname == 'city':
        if len(value) > 30:
            message.append('Too Long City Name')

    if fieldname == 'zipCode':
        if value == 0:
            message.append('Invalid ZIP Code.')

    if fieldname == 'securityCode':
        if value == 0:
            message.append('Invalid Security Code.')

    if fieldname == 'city':
        if len(value) > 15:
            message.append('Too Long Input')

    if fieldname == 'cardNumber':
        regex_card = '(?:[0-9]{4}-){3}[0-9]{4}'
        if re.search(regex_card, value) == None:
            message.append('Invalid Card Number. Maintain the format XXXX-XXXX-XXXX-XXXX')

    return message


def validate_all_input(inputlist, valuelist):
    valid = True
    message = []

    for jj in range(0, len(inputlist)):
        boolval = check_goodness(inputlist[jj], valuelist[jj])
        valid = valid and boolval
        if boolval == False:
            message.append(error_message(inputlist[jj], valuelist[jj]))

    return [valid, message]


def validate_all_nonempty_input(inputlist, valuelist):
    valid = True
    message = []

    for jj in range(0, len(inputlist)):
        print(inputlist[jj])
        if inputlist[jj] == [] or inputlist[jj] is None or inputlist[jj] == '' or inputlist[jj] == 0:
            pass
        else:
            boolval = check_goodness(inputlist[jj], valuelist[jj])
            valid = valid and boolval
            if boolval == False:
                message.append(error_message(inputlist[jj], valuelist[jj]))

    return [valid, message]


##### Menu Options ######

##### Page Routes  ######

# HomePage
@app.route('/')
def index():
    return render_template('index.html')


# Login Page
@app.route('/login')
def login():
    if not session.get('uid'):
        return render_template('login.html')
    else:
        flash('You are already logged in')
        return redirect(url_for('view_profile'))



# Register Page
@app.route('/register')
def register():
    if not session.get('uid'):
        return render_template('register.html')
    else:
        flash('You are already logged as %s. Logout First to signup as a new user.' % session.get('email') )
        return redirect(url_for('view_profile'))


# Cart Page
@app.route('/cart')
def cart():
    return render_template('cart.html')

# View Profile Page
@app.route('/view_profile')
def view_profile():
        if session.get('uid') != None:
            uid = session.get('uid')
            pdata_query = "SELECT * FROM `bookstore`.`users` where `userID`= %d ;" % uid
            sadata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='ship' " % uid
            badata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='bill' " % uid
            paydata_query = "SELECT * FROM `bookstore`.`payment` where `UserID`= %d ;" % uid
            cur = mysql.connection.cursor()

            cur.execute(pdata_query)
            pdata = cur.fetchall()
            cur.execute(sadata_query)
            sadata = cur.fetchall()
            cur.execute(badata_query)
            badata = cur.fetchall()
            cur.execute(paydata_query)
            paydata = cur.fetchall()
            print(pdata, sadata, badata, paydata)
            return render_template('viewprofile.html', pdata=pdata, sadata= sadata, badata = badata, paydata = paydata)
        else:
            return redirect(url_for('index'))


@app.route('/edit_profile')
def edit_profile():
    if session.get('uid') != None:
        uid = session.get('uid')
        pdata_query = "SELECT * FROM `bookstore`.`users` where `userID`= %d ;" % uid
        sadata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='ship' " % uid
        badata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='bill' " % uid
        paydata_query = "SELECT * FROM `bookstore`.`payment` where `UserID`= %d ;" % uid
        cur = mysql.connection.cursor()

        cur.execute(pdata_query)
        pdata = cur.fetchall()
        cur.execute(sadata_query)
        sadata = cur.fetchall()
        cur.execute(badata_query)
        badata = cur.fetchall()
        cur.execute(paydata_query)
        paydata = cur.fetchall()
        return render_template('editprofile.html', pdata=pdata, sadata=sadata, badata=badata, paydata=paydata)
    else:
        return redirect(url_for('index'))

# Show Books
# @@ Get from Database
@app.route('/book/<int:book_num>')
def bookshow(book_num):
    book_title = ["Software Engineering", "Computer Networks", "C How to program", "Data Mining", "Operating System",
                  "Rome History"]
    book_author = ["SommerVille", "Andrew S Tanenbaum", "Dietel", "Vipin Kumar", "Greg Gagne", "John Smith"]
    book_price = ["$15", "$25", "$40", "$50", "$18", "$15"]
    book_dir = ["../static/images/books/05.jpg",
                "../static/images/books/06.jpg",
                "../static/images/books/03.jpg",
                "../static/images/books/02.jpg",
                "../static/images/books/04.jpg",
                "../static/images/books/01.jpg"]

    infopass = {'book_title': book_title[book_num - 1],
                'book_author': book_author[book_num - 1],
                'book_price': book_price[book_num - 1],
                'book_dir': book_dir[book_num - 1]}
    # print(infopass)
    return render_template('book.html', infopass=infopass)


##### Actions #####

@app.route('/register_data', methods=['GET', 'POST'])
def register_data():
    cur = mysql.connection.cursor()
    ship_address_insert = 0
    card_info_insert = 0
    bill_address_insert = 0

    val_firstName = str(request.form['fname']).strip()
    val_lastName = str(request.form['lname']).strip()
    val_gender = str(request.form.get('gender')).strip()
    val_email = str(request.form['email']).strip().lower()
    val_password = str(request.form['password']).strip()
    val_phone_1 = str(request.form.get('phonenumbercountry'))
    val_phone_2 = str(request.form['mainphonenumber']).strip()
    val_phone = val_phone_1 + val_phone_2
    val_activationKey = randint(0, 999999)

    val_shipname = str(request.form['shipname']).strip()
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

    val_billname = str(request.form['billname']).strip()
    val_billstreetaddress = str(request.form['billstreetaddress']).strip()
    val_billaptno = str(request.form['billaptno']).strip()
    val_billinputCity = str(request.form['billinputCity']).strip()
    val_billinputState = str(request.form.get('billinputState')).strip()
    val_billinputZip = conv_int(request.form['billinputZip'])

    # validate mandatory inputs
    inputlist = [val_firstName, val_lastName, val_email, val_password, val_phone_2]
    typelist = ['firstName', 'lastName', 'email', 'password', 'phone']

    [validate, flash_messages] = validate_all_input(inputlist, typelist)

    if not validate:
        flash(flash_messages)
        return redirect(url_for('register'))

    # check if any entry for shipping address is there
    if len(val_shipname) != 0 or len(val_streetaddress) != 0 or len(val_aptno) != 0 or len(val_inputCity) != 0 or val_inputZip != 0:

        # validate shipping address inputs
        inputlist2 = [val_shipname, val_streetaddress, val_aptno, val_inputCity, val_inputZip]
        typelist2 = ['name', 'street', 'street2', 'city', 'zipCode']

        [validate2, flash_messages2] = validate_all_input(inputlist2, typelist2)

        if not validate2:
            flash(flash_messages2)
            return redirect(url_for('register'))

        if len(val_streetaddress) != 0 and len(val_aptno) != 0 and len(val_inputCity) != 0 and val_inputZip != 0:
            # confirm if shipping address is needed to be inserted
            ship_address_insert = 1
        else:
            flash('Enter All Fields in the Shipping Address')
            return redirect(url_for('register'))

    # check if card inputs are there
    if len(val_nameoncard) != 0 or len(val_cardno) != 0 or val_CVV != 0:
        # validate card inputs
        inputlist3 = [val_nameoncard, val_cardno, val_CVV]
        typelist3 = ['nameoncard', 'cardNumber', 'securityCode']

        [validate3, flash_messages3] = validate_all_input(inputlist3, typelist3)

        if not validate3:
            flash(flash_messages3)
            return redirect(url_for('register'))

        if len(val_nameoncard) != 0 and len(val_cardno) != 0 and val_CVV != 0:
            card_info_insert = 1
        else:
            flash('Enter All fields in the Card Information')
            return redirect(url_for('register'))

    # check if billing address is there
    if len(val_billname) != 0 or len(val_billstreetaddress) != 0 or len(val_billaptno) != 0 or len(val_billinputCity) != 0 or val_billinputZip != 0:
        # validate billing address info
        inputlist4 = [val_billname, val_billstreetaddress, val_billaptno, val_billinputCity, val_billinputZip]
        typelist4 = ['name', 'street', 'street2', 'city', 'zipCode']

        [validate4, flash_messages4] = validate_all_input(inputlist4, typelist4)

        if not validate4:
            flash(flash_messages4)
            return redirect(url_for('register'))

        if len(val_billname) != 0 and len(val_billstreetaddress) != 0 and len(val_billaptno) != 0 and len(val_billinputCity) != 0 and val_billinputZip != 0:
            bill_address_insert = 1
        else:
            flash('Enter All fields in the Billing Address')
            return redirect(url_for('register'))

    try:
        sqlstatementman = "INSERT INTO `bookstore`.`users`" \
                          "(`firstName`, `lastName`, `password`, " \
                          "`email`, `phone`, `userTypeID`, " \
                          "`Subscription`, `active`, `activationKey`, " \
                          "`suspended`, `gender`)" \
                          "VALUES (\'%s\', \'%s\', \'%s\', " \
                          "\'%s\', \'%s\', 2, " \
                          "1, 0, \'%d\', " \
                          "0, \'%s\' );" \
                          % (val_firstName, val_lastName, generate_password_hash(val_password), \
                             val_email, val_phone, \
                             val_activationKey, \
                             val_gender)
        cur.execute(sqlstatementman)
        mysql.connection.commit()
        userid = cur.lastrowid

        if ship_address_insert == 1:
            insert_address = "INSERT INTO `bookstore`.`address`" \
                             "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                             "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'ship', \'%d\');" \
                             % (val_shipname, val_streetaddress, val_aptno, val_inputZip, val_inputCity, val_inputState, userid)
            cur.execute(insert_address)
            mysql.connection.commit()

        if card_info_insert == 1:
            insert_cardinfo = "INSERT INTO `bookstore`.`payment`" \
                              "(`cardNumber`, `expiryYear`, `expiryMonth`, `securityCode`, `paymentType`, `UserID`, `nameoncard`)" \
                              "VALUES( \'%s\' , \'%d\', \'%d\', \'%d\' , \'%s\', \'%d\', \'%s\' );" \
                              % (val_cardno, val_expyear, val_expmonth, val_CVV, val_cardtype, userid, val_nameoncard.upper())
            cur.execute(insert_cardinfo)
            mysql.connection.commit()

        if bill_address_insert == 1:
            insert_billaddress = "INSERT INTO `bookstore`.`address`" \
                                 "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                                 "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'bill', \'%d\');" \
                                 % (val_billname, val_billstreetaddress, val_billaptno, val_billinputZip, val_billinputCity, val_billinputState, userid)
            cur.execute(insert_billaddress)
            mysql.connection.commit()

    except:
        flash('Duplicate Email Address')
        return redirect(url_for('register'))


    msgg = Message("Team3 Book Store", sender="t3@myw.urq.mybluehost.me", recipients=[val_email])
    msgg.body = '''Thank you for registering, ... 
                    to activate your account ... 
                    sign in with your password and ...
                    you have to enter the following code when logging in : %s ''' % str(val_activationKey)

    mail.send(msgg)

    flash('You have successfully completed your registration. Please check your email for further procedures.')
    return redirect(url_for('index'))


@app.route('/login_action', methods=['GET', 'POST'])
def login_action():
    cur = mysql.connection.cursor()
    # get email and password from form
    val_email = request.form['email']
    val_password = request.form['psw']

    # see if remember me is checcked
    val_rem = request.form.getlist('remember')

    # search for email and password in database
    querystatement = "SELECT * FROM `bookstore`.`users`" \
                     "where email=\'%s\' " % val_email
    cur.execute(querystatement)
    results = cur.fetchall()

    # storing email in session
    if len(val_rem) == 1:
        session.permanent = True

    # email match action
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
            email = results[0]['email']
            session['uid'] = uid
            session['email'] = email
            return render_template('admin.html')
        else:
            session['usertype'] = 2
            uid = results[0]['userID']
            email = results[0]['email']
            session['uid'] = uid
            session['email'] = email
            return redirect(url_for('view_profile'))


@app.route('/logout')
def logout():
    if session['logged_in'] == True:
        session['logged_in'] = False
        session['uid'] = None
        session['email'] = None
        flash('You are successfully logged out')
        return redirect(url_for('index'))
    else:
        flash('You are already logged out')
        return redirect(url_for('index'))


@app.route('/password_recover_start')
def password_recover_start():
    return render_template('password_recover_1.html')


@app.route('/send_otp', methods=['GET', 'POST'])
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
        new_activation_key = randint(0, 99999)
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


@app.route('/password_recovery_finished', methods=['GET', 'POST'])
def password_recovery_finished():
    cur = mysql.connection.cursor()
    val_email = request.form['email']
    val_otp = int(request.form['OTP'])
    val_newpass = request.form['newpass']
    val_rnewpass = request.form['rnewpass']
    stage_1_conf = "SELECT email, activationKey FROM `bookstore`.`users`" \
                   "where email=\'%s\' AND activationKey=\'%d\'" \
                   % (val_email, val_otp)
    cur.execute(stage_1_conf)
    res1 = cur.fetchall()
    if len(res1) != 0:
        if val_newpass == val_rnewpass:
            if not check_goodness(val_newpass, 'password'):
                flash(error_message(val_newpass, 'password'))
                return render_template('password_recover_2.html.')
            else:
                password_change = "UPDATE `bookstore`.`users` " \
                                  "SET `password` = \'%s\' " \
                                  "WHERE (`email` = \'%s\')" \
                                  % (generate_password_hash(val_newpass), val_email)
                cur.execute(password_change)
                mysql.connection.commit()
                flash('Password Successfully Changed')

            #see if activated

            active_check = "SELECT active FROM `bookstore`.`users` WHERE ( `email` = \'%s\' )" % val_email
            cur.execute(active_check)
            res = cur.fetchall()
            active_stat = int(res[0]['active'])

            # update OTP and notify user
            if active_stat == 0:
                new_otp = randint(0,999999)
                otp_update = "UPDATE `bookstore`.`users` " \
                              "SET `activationKey` = \'%d\' " \
                              "WHERE (`email` = \'%s\')" \
                              % (new_otp, val_email)
                cur.execute(otp_update)
                mysql.connection.commit()

                msgg = Message("Team3 Book Store", sender="t3@myw.urq.mybluehost.me", recipients=[val_email])
                msgg.body = ''' You have successfully changed your password. Please use the new activation key %d to activate yourself''' % new_otp
                mail.send(msgg)
            else:
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


@app.route('/activate_user_action', methods=['GET', 'POST'])
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



@app.route('/editProfileData', methods=['GET', 'POST'])
def editProfileData():
    cur = mysql.connection.cursor()
    userid = session.get('uid')

    val_firstName = str(request.form['fname']).strip()
    val_lastName = str(request.form['lname']).strip()
    val_gender = str(request.form.get('gender')).strip()
    val_email = str(request.form.get('email')).strip()
    val_phone_1 = str(request.form.get('phonenumbercountry'))
    val_phone_2 = str(request.form['mainphonenumber']).strip()
    val_phone = val_phone_1 + val_phone_2

    val_shipname = str(request.form['shipname']).strip()
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

    val_billname = str(request.form['billname']).strip()
    val_billstreetaddress = str(request.form['billstreetaddress']).strip()
    val_billaptno = str(request.form['billaptno']).strip()
    val_billinputCity = str(request.form['billinputCity']).strip()
    val_billinputState = str(request.form.get('billinputState')).strip()
    val_billinputZip = conv_int(request.form['billinputZip'])

    # validate individual

    inputlist = [val_firstName, val_lastName, val_phone_2,
                 val_shipname, val_streetaddress, val_aptno, val_inputCity, val_inputZip,
                 val_nameoncard, val_cardno, val_CVV,
                 val_billname, val_billstreetaddress, val_billaptno, val_billinputCity, val_billinputZip]

    typelist = [ 'firstName', 'lastName', 'phone',
                 'name', 'street', 'street2', 'city', 'zipCode',
                 'nameoncard', 'cardNumber', 'securityCode',
                 'name', 'street', 'street2', 'city', 'zipCode']
    val_ind = True
    error_show = []
    [val_ind, error_show] = validate_all_nonempty_input(inputlist, typelist)

    if not val_ind:
        flash(error_show)
        return redirect(url_for('edit_profile'))
    else:

        sadata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='ship' " % userid
        badata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='bill' " % userid
        paydata_query = "SELECT * FROM `bookstore`.`payment` where `UserID`= %d ;" % userid

        cur.execute(sadata_query)
        sadataex = cur.fetchall()
        cur.execute(badata_query)
        badataex = cur.fetchall()
        cur.execute(paydata_query)
        paydataex = cur.fetchall()



        pdataupdate = "UPDATE `bookstore`.`users`" \
                      "SET `firstName` = \'%s\', `lastName` = \'%s\', `phone` = \'%s\' " \
                      "WHERE `userID` = %d; " \
                       % (val_firstName, val_lastName, val_phone, userid)
        sadataupdate = "UPDATE `bookstore`.`address`" \
                      "SET `name` = \'%s\', `street` = \'%s\', `street2` = \'%s\', `city` = \'%s\', `state` = \'%s\', `zipCode` = %d   "  \
                      "WHERE `userID` = %d and `AddressType` = 'ship' ;" \
                       % (val_shipname, val_streetaddress, val_aptno, val_inputCity, val_inputState, val_inputZip, userid)
        badataupdate = "UPDATE `bookstore`.`address`" \
                       "SET `name` = \'%s\', `street` = \'%s\', `street2` = \'%s\', `city` = \'%s\', `state` = \'%s\', `zipCode` = %d   " \
                       "WHERE `userID` = %d and `AddressType` = 'bill' ;" \
                       % (val_billname, val_billstreetaddress, val_billaptno, val_billinputCity, val_billinputState, val_billinputZip, userid)

        paydataupdate = "UPDATE `bookstore`.`payment`" \
                        "SET `cardNumber` = \'%s\', `expiryYear` = %d, `expiryMonth` = %d, `securityCode` = %d, `nameoncard` = \'%s\', `paymentType` = \'%s\' " \
                        "WHERE `UserID` = %d ;" \
                        % (val_cardno, val_expyear, val_expmonth, val_CVV, val_nameoncard.upper(), val_cardtype, userid)

        sadatainsert = "INSERT INTO `bookstore`.`address`" \
                         "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                         "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'ship', \'%d\');" \
                         % (val_shipname, val_streetaddress, val_aptno, val_inputZip, val_inputCity, val_inputState, userid)

        badatainsert = "INSERT INTO `bookstore`.`address`" \
                        "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                        "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'bill', \'%d\');" \
                        % (val_billname, val_billstreetaddress, val_billaptno, val_billinputZip, val_billinputCity, val_billinputState, userid)

        paydatainsert = "INSERT INTO `bookstore`.`payment`" \
                          "(`cardNumber`, `expiryYear`, `expiryMonth`, `securityCode`, `paymentType`, `UserID`, `nameoncard`)" \
                          "VALUES( \'%s\' , \'%d\', \'%d\', \'%d\' , \'%s\', \'%d\', \'%s\' );" \
                          % (val_cardno, val_expyear, val_expmonth, val_CVV, val_cardtype, userid, val_nameoncard.upper())

        cur.execute(pdataupdate)
        mysql.connection.commit()

        if sadataex != ():
            cur.execute(sadataupdate)
            mysql.connection.commit()
        else:
            cur.execute(sadatainsert)
            mysql.connection.commit()

        if badataex != ():
            cur.execute(badataupdate)
            mysql.connection.commit()
        else:
            cur.execute(badatainsert)
            mysql.connection.commit()

        if paydataex != ():
            cur.execute(paydataupdate)
            mysql.connection.commit()
        else:
            cur.execute(paydatainsert)
            mysql.connection.commit()

        msgg = Message("Team3 Book Store", sender="t3@myw.urq.mybluehost.me", recipients=[val_email])
        msgg.body = ''' You have successfully updated your profile information.'''
        mail.send(msgg)
        flash('You have sucessfully updated your profile information.')
        return redirect(url_for('view_profile'))


@app.route('/change_password')
def change_password_start():
    return render_template('change_password.html')

@app.route('/password_changed' , methods = ['GET', 'POST'] )
def password_change_finished():
    cur = mysql.connection.cursor()
    val_email = session.get('email')
    oldp = request.form['oldp']
    val_newpass = request.form['newpass']
    val_rnewpass = request.form['rnewpass']
    stage_1_conf = "SELECT email, password FROM `bookstore`.`users`" \
                   "where email=\'%s\'" \
                   % val_email
    cur.execute(stage_1_conf)
    res1 = cur.fetchall()

    if not check_password_hash(res1[0]['password'], oldp):
        flash('Old password did not match')
        return render_template('change_password.html')
    elif val_newpass != val_rnewpass:
        flash('ReTyped password did not match')
        return render_template('change_password.html')
    elif not check_goodness(val_newpass, 'password'):
        flash(error_message(val_newpass, 'password'))
        return render_template('change_password.html')
    else:
        password_change = "UPDATE `bookstore`.`users` " \
                          "SET `password` = \'%s\' " \
                          "WHERE (`email` = \'%s\')" \
                           % (generate_password_hash(val_newpass), val_email)
        cur.execute(password_change)
        mysql.connection.commit()

        msgg = Message("Team3 Book Store", sender="t3@myw.urq.mybluehost.me", recipients=[val_email])
        msgg.body = ''' You have successfully changed your password.'''
        mail.send(msgg)

        flash('Password Successfully Changed')
        return redirect(url_for('edit_profile'))




if __name__ == '__main__':
    app.run(debug=True)
