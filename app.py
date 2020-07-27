from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from random import randint
from datetime import datetime
import functools
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
from flask_uploads import UploadSet, configure_uploads, IMAGES
# from simplecrypt import encrypt, decrypt
from cryptography.fernet import Fernet
import re, os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12341234'
app.config['MYSQL_DB'] = 'bookstore'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'abcdabcd'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images/books'

app.config.update(DEBUG=True, MAIL_SERVER='box5928.bluehost.com',
                  MAIL_PORT=465, MAIL_USE_SSL=True, MAIL_USERNAME='t3@myw.urq.mybluehost.me',
                  MAIL_PASSWORD='78rehkas')

mail = Mail(app)
mysql = MySQL(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

key = b'fRmBje4ZejoeBPmxESfU2ElslhIcjiose6rHt4qaV4c='
fenc = Fernet(key=key)


##### Custom functions go here ####


def set_query(query):
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
        return True
    except:
        return False


def get_query(query):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute(query)
        return cur.fetchall()


def send_message(body, val_email):
    msgg = Message("Team3 Book Store", sender="t3@myw.urq.mybluehost.me", recipients=[val_email])
    msgg.body = body
    mail.send(msgg)


def conv_int(a):
    try:
        int(a)
        return int(a)
    except ValueError:
        return 0


def conv_float(a):
    try:
        float(a)
        return float(a)
    except ValueError:
        return None


def get_cart_total(cart_dict):
    total = 0
    for jj in cart_dict:
        item_total = conv_int(jj['quantity']) * conv_float(jj['sellingPrice'])
        total += item_total

    return total


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

    if fieldname == 'title' or fieldname == 'author' or fieldname == 'publisher':
        if len(value) < 50:
            return True
        else:
            return False

    if fieldname == 'ISBN':
        regex_ISBN = '^[0-9]{13}$'
        if re.search(regex_ISBN, value) is not None:
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

    if fieldname == 'title' or fieldname == 'author' or fieldname == 'publisher':
        if len(value) > 50:
            message.append('Too Long Input. Cannot exceed 50 characters.')

    if fieldname == 'ISBN':
        regex_ISBN = '^(\d{13})$'
        if re.search(regex_ISBN, value) is None:
            message.append('Invalid ISBN')

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

'''
@app.route('/let_me_see_base')
def base():
    return render_template('base.html')
'''


@app.route('/')
def index():
    all_book_query = "select  `books`.*, `bookinventory`.`bookID` , `bookinventory`.`sellingPrice` from `books`" \
                     "inner join `bookinventory`" \
                     "on `books`.`ISBN` = `bookinventory`.`bookID`;"
    result = get_query(all_book_query)
    return render_template('index.html', data=result)


# Login Page
@app.route('/login')
def login():
    if not session.get('uid'):
        return render_template('login.html')
    else:
        flash('You are already logged in')
        return redirect(url_for('view_profile'))


@app.route('/admin_panel')
def show_admin_panel():
    return render_template('admin.html')


@app.route('/manage_user')
def manage_user():
    return render_template('usermanagement.html')


@app.route('/manage_books')
def manage_books():
    all_book_query = "select `books`.*, `bookinventory`.*, `category`.`category` as `cats` from `books` " \
                     "inner join `bookinventory` " \
                     "on `books`.`ISBN` = `bookinventory`.`bookID`" \
                     "inner join `category`" \
                     "on `books`.`category` = `category`.`idCategory`;"
    all_book = get_query(all_book_query)
    return render_template('manage_books.html', data = all_book)


@app.route('/add_book')
def add_book():
    cat_query = "SELECT * FROM `bookstore`.`category`;"
    cats = get_query(cat_query)
    return render_template('addbook.html', cats=cats)


@app.route('/search_book')
def search_book():
    return render_template('searchbook.html')


@app.route('/manage_promotions')
def manage_promotions():
    return render_template('promomanagement.html')


# Register Page
@app.route('/register')
def register():
    if not session.get('uid'):
        return render_template('register.html')
    else:
        flash('You are already logged as %s. Logout First to signup as a new user.' % session.get('email'))
        return redirect(url_for('view_profile'))


# Cart Page
@app.route('/cart')
def cart():
    if session.get('logged_in') is True and session.get('userTypeID') == 2:
        uid = session.get('userID')
        cart_detail_query = "select  `cart`.* , " \
                            "`bookinventory`.`sellingPrice`, " \
                            "`books`.`title`, `books`.`author`, `books`.`category`, " \
                            "`category`.`category` as `cats`" \
                            "from `cart`" \
                            "inner join `bookinventory`" \
                            "on `cart`.`bookID` = `bookinventory`.`bookID`" \
                            "inner join `books`" \
                            "on `books`.`ISBN` = `cart`.`bookID`" \
                            "inner join `category`" \
                            "on `books`.`category` = `category`.`idCategory`" \
                            "where `cart`.`userID` = \'%d\';" % uid
        full_cart = get_query(cart_detail_query)
        temptot = get_cart_total(full_cart)
        get_pending_order = "select * from `bookstore`.`order` " \
                            "where (`userID` = \'%d\') and (`orderstatus` = 'pending');" % uid
        pending_order_det = get_query(get_pending_order)
        if len(pending_order_det) == 0:
            flash('Your cart is empty. Add some items to cart')
            return redirect(url_for('index'))
        elif pending_order_det[0]['PromoID'] == -1:
            update_in_order = "update `bookstore`.`order` " \
                              "set `total` = \'%.2f\'" \
                              "where (`userID` = \'%d\') and (`orderstatus` = \'%s\')" \
                              % (temptot, uid, 'pending')
            set_query(update_in_order)
            pending_order_det = get_query(get_pending_order)
            return render_template('cart.html', cdata=full_cart, odata=pending_order_det)
        else:
            disc_search = "select `discountAmount` from `bookstore`.`promotion` " \
                          "where `idPromotion` = \'%d\'" % int(pending_order_det[0]['PromoID'])
            disc_amount = int(get_query(disc_search)[0]['discountAmount'])
            fintot = temptot - temptot * disc_amount / 100
            update_in_order_promo = "update `bookstore`.`order` " \
                                    "set `total` = \'%.2f\'" \
                                    "where (`userID` = \'%d\') and (`orderstatus` = \'%s\')" \
                                    % (fintot, uid, 'pending')
            set_query(update_in_order_promo)
            pending_order_det = get_query(get_pending_order)
            return render_template('cart.html', cdata=full_cart, temptot=temptot, odata=pending_order_det)
    else:
        flash('You are not allowed to view this page')
        return redirect(url_for('index'))


@app.route('/modify_cart')
def modify_cart():
    if session.get('logged_in') is True and session.get('userTypeID') == 2:
        uid = session.get('userID')
        cart_detail_query = "select  `cart`.* , " \
                            "`bookinventory`.`sellingPrice`, " \
                            "`books`.`title`, `books`.`author`, `books`.`category`, " \
                            "`category`.`category` as `cats` " \
                            "from `cart`" \
                            "inner join `bookinventory`" \
                            "on `cart`.`bookID` = `bookinventory`.`bookID`" \
                            "inner join `books`" \
                            "on `books`.`ISBN` = `cart`.`bookID`" \
                            "inner join `category`" \
                            "on `books`.`category` = `category`.`idCategory`" \
                            "where `cart`.`userID` = \'%d\';" % uid
        full_cart = get_query(cart_detail_query)
        return render_template('modifycart.html', cdata=full_cart)
    else:
        flash('You are not allowed view this page')
        return redirect(url_for('index'))


@app.route('/remove_from_cart')
def remove_from_cart():
    if session.get('logged_in') is True and session.get('userTypeID') == 2:
        uid = int(session.get('userID'))
        cart_detail_query = "select  `cart`.* , " \
                            "`bookinventory`.`sellingPrice`, " \
                            "`books`.`title`, `books`.`author`, `books`.`category`, " \
                            "`category`.`category` as `cats` " \
                            "from `cart`" \
                            "inner join `bookinventory`" \
                            "on `cart`.`bookID` = `bookinventory`.`bookID`" \
                            "inner join `books`" \
                            "on `books`.`ISBN` = `cart`.`bookID`" \
                            "inner join `category`" \
                            "on `books`.`category` = `category`.`idCategory`" \
                            "where `cart`.`userID` = \'%d\';" % uid
        full_cart = get_query(cart_detail_query)
        return render_template('removefromcart.html', data=full_cart)
    else:
        flash('You are not allowed view this page')
        return redirect(url_for('index'))


@app.route('/checkout')
def checkout():
    if session.get('logged_in') is True and session.get('userTypeID') == 2:
        uid = int(session.get('userID'))
        pending_order_search = "select * from `bookstore`.`order` " \
                               "where (`userID` = \'%d\') and (`orderstatus` = 'pending');" % uid
        res = get_query(pending_order_search)
        if len(res) == 0:
            flash('Add something to cart first')
            redirect(url_for('index'))
        elif int(res[0]['total']) == 0:
            flash('Add something to cart first')
            redirect(url_for('index'))
        else:
            cart_detail_query = "select  `cart`.* , " \
                                "`bookinventory`.`sellingPrice`, " \
                                "`books`.`title`, `books`.`author`, `books`.`category`, " \
                                "`category`.`category` as `cats`" \
                                "from `cart`" \
                                "inner join `bookinventory`" \
                                "on `cart`.`bookID` = `bookinventory`.`bookID`" \
                                "inner join `books`" \
                                "on `books`.`ISBN` = `cart`.`bookID`" \
                                "inner join `category`" \
                                "on `books`.`category` = `category`.`idCategory`" \
                                "where `cart`.`userID` = \'%d\';" % uid
            full_cart = get_query(cart_detail_query)
            temptot = get_cart_total(full_cart)
            get_pending_order = "select * from `bookstore`.`order` " \
                                "where (`userID` = \'%d\') and (`orderstatus` = 'pending');" % uid
            pending_order_det = get_query(get_pending_order)

            # get payment info
            pay_query = "SELECT * FROM `bookstore`.`payment` WHERE `userID`=\'%d\'" % uid
            pay = get_query(pay_query)
            print(pay)
            # get billShipping info
            bill_query = "SELECT * FROM `bookstore`.`address` WHERE `userID`=\'%d\' AND `AddressType`=\'bill\'" % uid
            bill = get_query(bill_query)
            # get shippingAddy
            ship_query = "SELECT * FROM `bookstore`.`address` WHERE `userID`=\'%d\' AND `AddressType`=\'ship\'" % uid
            ship = get_query(ship_query)

            if pending_order_det[0]['PromoID'] == -1:
                update_in_order = "update `bookstore`.`order` " \
                                  "set `total` = \'%.2f\'" \
                                  "where (`userID` = \'%d\') and (`orderstatus` = \'%s\')" \
                                  % (temptot, uid, 'pending')
                set_query(update_in_order)
                pending_order_det = get_query(get_pending_order)
                return render_template('checkout.html', cartinfo=full_cart,
                                       orderinfo=pending_order_det, sadata=ship,
                                       badata=bill, paydata=pay)

            else:
                disc_search = "select `discountAmount` from `bookstore`.`promotion` " \
                              "where `idPromotion` = \'%d\'" % int(pending_order_det[0]['PromoID'])
                disc_amount = int(get_query(disc_search)[0]['discountAmount'])
                fintot = temptot - temptot * disc_amount / 100
                update_in_order_promo = "update `bookstore`.`order` " \
                                        "set `total` = \'%.2f\'" \
                                        "where (`userID` = \'%d\') and (`orderstatus` = \'%s\')" \
                                        % (fintot, uid, 'pending')
                set_query(update_in_order_promo)
                pending_order_det = get_query(get_pending_order)
                return render_template('checkout.html', cartinfo=full_cart, temptot=temptot,
                                       orderinfo=pending_order_det, sadata=ship,
                                       badata=bill, paydata=pay)


# View Profile Page
@app.route('/view_profile')
def view_profile():
    if session.get('userID') != None:
        uid = session.get('userID')
        pdata_query = "SELECT * FROM `bookstore`.`users` where `userID`= %d ;" % uid
        sadata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='ship' " % uid
        badata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='bill' " % uid
        paydata_query = "SELECT * FROM `bookstore`.`payment` where `UserID`= %d ;" % uid

        pdata = get_query(pdata_query)
        sadata = get_query(sadata_query)
        badata = get_query(badata_query)
        paydata = get_query(paydata_query)
        print(pdata, sadata, badata, paydata)
        return render_template('viewprofile.html', pdata=pdata, sadata=sadata, badata=badata, paydata=paydata)
    else:
        return redirect(url_for('index'))


# edit profile page
@app.route('/edit_profile')
def edit_profile():
    if session.get('userID') != None:
        uid = session.get('userID')
        pdata_query = "SELECT * FROM `bookstore`.`users` where `userID`= %d ;" % uid
        sadata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='ship' " % uid
        badata_query = "SELECT * FROM `bookstore`.`address` where `userID`=%d and `AddressType`='bill' " % uid
        paydata_query = "SELECT * FROM `bookstore`.`payment` where `UserID`= %d ;" % uid

        pdata = get_query(pdata_query)
        sadata = get_query(sadata_query)
        badata = get_query(badata_query)
        paydata = get_query(paydata_query)

        return render_template('editprofile.html', pdata=pdata, sadata=sadata, badata=badata, paydata=paydata)
    else:
        return redirect(url_for('index'))


@app.route('/apply_promo_page')
def apply_promo():
    if session.get('logged_in') is True and session.get('userTypeID') == 2:
        uid = session.get('userID')
        cart_detail_query = "select  `cart`.* , " \
                            "`bookinventory`.`sellingPrice`, " \
                            "`books`.`title`, `books`.`author`, `books`.`category`, " \
                            "`category`.`category` as `cats`" \
                            "from `cart`" \
                            "inner join `bookinventory`" \
                            "on `cart`.`bookID` = `bookinventory`.`bookID`" \
                            "inner join `books`" \
                            "on `books`.`ISBN` = `cart`.`bookID`" \
                            "inner join `category`" \
                            "on `books`.`category` = `category`.`idCategory`" \
                            "where `cart`.`userID` = \'%d\';" % uid
        full_cart = get_query(cart_detail_query)
        tot = get_cart_total(full_cart)
        get_pending_order = "select * from `bookstore`.`order` " \
                            "where (`userID` = \'%d\') and (`orderstatus` = 'pending');" % uid
        res = get_query(get_pending_order)
        if len(res) == 0:
            flash('Add items to cart first')
            return redirect(url_for('index'))
        elif int(res[0]['PromoID']) != -1:
            flash('Promo Code Already Applied')
            return redirect(url_for('cart'))
        else:
            return render_template('applypromo.html', data=full_cart, total=tot)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/order_history')
def order_history():
    if session.get('logged_in') is True and session.get('userTypeID') == 2:
        uid = int(session.get('userID'))
        non_pending_orders = "select * from `bookstore`.`order`" \
                             "where `userID` = \'%d\' and `orderstatus` != 'pending'" % uid
        all_orders = get_query(non_pending_orders)
        order_prods = []
        if len(all_orders) == 0:
            flash('You have no previous orders')
            return redirect(url_for('cart'))
        else:
            for jj in range(0, len(all_orders)):
                order_prods_query = "SELECT `orderitems`.*, `bookinventory`.`sellingPrice`, `books`.`title` " \
                                    "FROM `orderitems`" \
                                    "inner join `bookinventory`" \
                                    "on `orderitems`.`ProductID` = `bookinventory`.`bookID`" \
                                    "inner join `books`" \
                                    "on `orderitems`.`ProductID` = `books`.`ISBN`" \
                                    "where orderID = \'%d\';" \
                                    % int(all_orders[jj]['orderID'])
                one_order_prods = get_query(order_prods_query)
                order_prods.append(one_order_prods)

            return render_template('orderhistory.html', ord=all_orders, ordlen=len(all_orders),
                                   prod=order_prods)


    else:
        flash('you are not allowed to view this page')
        return redirect(url_for('index'))
    return render_template('orderhistory.html')


@app.route('/order_confirmation')
def order_confirmation():
    return render_template('orderconfirmation.html')


@app.route('/book/<string:book_num>')
def bookshow(book_num):
    specific_book_query = "select  `books`.*, `bookinventory`.`bookID`, `bookinventory`.`sellingPrice` from `books`" \
                          "inner join `bookinventory`" \
                          "on `books`.`ISBN` = `bookinventory`.`bookID` " \
                          "where `bookinventory`.`bookID` = %s;" % book_num
    infopass = get_query(specific_book_query)
    catID = int(infopass[0]['category'])
    find_cat = "select * from `bookstore`.`category` where `category`.`idCategory` = %d " % catID
    cat_res = get_query(find_cat)
    return render_template('book.html', infopass=infopass[0], cat=cat_res[0])


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
    if len(val_shipname) != 0 or len(val_streetaddress) != 0 or len(val_aptno) != 0 or len(
            val_inputCity) != 0 or val_inputZip != 0:

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
    if len(val_billname) != 0 or len(val_billstreetaddress) != 0 or len(val_billaptno) != 0 or len(
            val_billinputCity) != 0 or val_billinputZip != 0:
        # validate billing address info
        inputlist4 = [val_billname, val_billstreetaddress, val_billaptno, val_billinputCity, val_billinputZip]
        typelist4 = ['name', 'street', 'street2', 'city', 'zipCode']

        [validate4, flash_messages4] = validate_all_input(inputlist4, typelist4)

        if not validate4:
            flash(flash_messages4)
            return redirect(url_for('register'))

        if len(val_billname) != 0 and len(val_billstreetaddress) != 0 and len(val_billaptno) != 0 and len(
                val_billinputCity) != 0 and val_billinputZip != 0:
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
        set_query(sqlstatementman)
        userid = cur.lastrowid

        if ship_address_insert == 1:
            insert_address = "INSERT INTO `bookstore`.`address`" \
                             "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                             "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'ship', \'%d\');" \
                             % (val_shipname, val_streetaddress, val_aptno, val_inputZip, val_inputCity, val_inputState,
                                userid)
            set_query(insert_address)

        if card_info_insert == 1:
            insert_cardinfo = "INSERT INTO `bookstore`.`payment`" \
                              "(`cardNumber`, `expiryYear`, `expiryMonth`, `securityCode`, `paymentType`, `UserID`, `nameoncard`)" \
                              "VALUES( \'%s\' , \'%d\', \'%d\', \'%d\' , \'%s\', \'%d\', \'%s\' );" \
                              % (val_cardno, val_expyear, val_expmonth, val_CVV, val_cardtype, userid,
                                 val_nameoncard.upper())
            set_query(insert_cardinfo)

        if bill_address_insert == 1:
            insert_billaddress = "INSERT INTO `bookstore`.`address`" \
                                 "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                                 "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'bill', \'%d\');" \
                                 % (val_billname, val_billstreetaddress, val_billaptno, val_billinputZip,
                                    val_billinputCity, val_billinputState, userid)
            set_query(insert_billaddress)

    except:
        flash('Duplicate Email Address')
        return redirect(url_for('register'))

    body_text = '''Thank you for registering, ... 
                    to activate your account ... 
                    sign in with your password and ...
                    you have to enter the following code when logging in : %s ''' % str(val_activationKey)

    send_message(body_text, val_email)

    flash('You have successfully completed your registration. Please check your email for further procedures.')
    return redirect(url_for('index'))


@app.route('/login_action', methods=['GET', 'POST'])
def login_action():
    # get email and password from form
    val_email = request.form['email']
    val_password = request.form['psw']

    # see if remember me is checcked
    val_rem = request.form.getlist('remember')

    # search for email and password in database
    querystatement = "SELECT * FROM `bookstore`.`users`" \
                     "where email=\'%s\' " % val_email

    results = get_query(querystatement)

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
        if results[0]['userTypeID'] == 1:
            session['userTypeID'] = 1
            uid = results[0]['userID']
            email = results[0]['email']
            session['userID'] = uid
            session['email'] = val_email
            flash('You are Logged in as %s' % session.get('email'))
            return redirect(url_for('show_admin_panel'))
        else:
            session['userTypeID'] = 2
            uid = results[0]['userID']
            email = results[0]['email']
            session['userID'] = uid
            session['email'] = val_email
            flash('You are Logged in as %s' % val_email)
            return redirect(url_for('view_profile'))


@app.route('/logout')
def logout():
    if session['logged_in'] == True:
        session['logged_in'] = False
        session['userID'] = None
        session['email'] = None
        session['userTypeID'] = None
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
    # get email and password from form
    val_email = request.form['email']
    search_email_query = "SELECT * FROM `bookstore`.`users`" \
                         "where email=\'%s\' " % (val_email)
    results = get_query(search_email_query)
    print(results)
    if results:
        update_id = results[0]['userID']
        new_activation_key = randint(0, 99999)
        update_activation_key = "UPDATE `bookstore`.`users` " \
                                "SET `activationKey` = %d " \
                                "WHERE (`userID` = %d)" \
                                % (new_activation_key, update_id)
        set_query(update_activation_key)

        body_text = ''' We have sent you a one time password to recover your password %s ''' % str(new_activation_key)
        send_message(body_text, val_email)

        return render_template('password_recover_2.html')
    else:
        flash('Email not found in system')
        return redirect(url_for('password_recover_start'))


@app.route('/password_recovery_finished', methods=['GET', 'POST'])
def password_recovery_finished():
    val_email = request.form['email']
    val_otp = int(request.form['OTP'])
    val_newpass = request.form['newpass']
    val_rnewpass = request.form['rnewpass']
    stage_1_conf = "SELECT email, activationKey FROM `bookstore`.`users`" \
                   "where email=\'%s\' AND activationKey=\'%d\'" \
                   % (val_email, val_otp)
    res1 = get_query(stage_1_conf)
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
                set_query(password_change)
                flash('Password Successfully Changed')

            # see if activated

            active_check = "SELECT active FROM `bookstore`.`users` WHERE ( `email` = \'%s\' )" % val_email
            res = get_query(active_check)
            active_stat = int(res[0]['active'])

            # update OTP and notify user
            if active_stat == 0:
                new_otp = randint(0, 999999)
                otp_update = "UPDATE `bookstore`.`users` " \
                             "SET `activationKey` = \'%d\' " \
                             "WHERE (`email` = \'%s\')" \
                             % (new_otp, val_email)
                set_query(otp_update)
                body_text = ''' You have successfully changed your password. Please use the new activation key %d to activate yourself''' % new_otp
            else:
                body_text = ''' You have successfully changed your password '''

            send_message(body_text, val_email)
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
    val_email = request.form['email']
    val_otp = request.form['otp']

    find_user = "SELECT * FROM `bookstore`.`users`" \
                "where email=\'%s\' " % (val_email)

    res = get_query(find_user)

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

        set_query(activation_change)
        body_text = "You have been activated. Use your password to login"
        send_message(body_text, val_email)

        flash('User Successfully activated')
        return redirect(url_for('login'))


@app.route('/editProfileData', methods=['GET', 'POST'])
def editProfileData():
    userid = int(session.get('userID'))

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

    typelist = ['firstName', 'lastName', 'phone',
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

        sadataex = get_query(sadata_query)
        badataex = get_query(badata_query)
        paydataex = get_query(paydata_query)

        pdataupdate = "UPDATE `bookstore`.`users`" \
                      "SET `firstName` = \'%s\', `lastName` = \'%s\', `phone` = \'%s\' " \
                      "WHERE `userID` = %d; " \
                      % (val_firstName, val_lastName, val_phone, userid)
        sadataupdate = "UPDATE `bookstore`.`address`" \
                       "SET `name` = \'%s\', `street` = \'%s\', `street2` = \'%s\', `city` = \'%s\', `state` = \'%s\', `zipCode` = %d   " \
                       "WHERE `userID` = %d and `AddressType` = 'ship' ;" \
                       % (
                           val_shipname, val_streetaddress, val_aptno, val_inputCity, val_inputState, val_inputZip,
                           userid)
        badataupdate = "UPDATE `bookstore`.`address`" \
                       "SET `name` = \'%s\', `street` = \'%s\', `street2` = \'%s\', `city` = \'%s\', `state` = \'%s\', `zipCode` = %d   " \
                       "WHERE `userID` = %d and `AddressType` = 'bill' ;" \
                       % (val_billname, val_billstreetaddress, val_billaptno, val_billinputCity, val_billinputState,
                          val_billinputZip, userid)

        paydataupdate = "UPDATE `bookstore`.`payment`" \
                        "SET `cardNumber` = \'%s\', `expiryYear` = %d, `expiryMonth` = %d, `securityCode` = %d, `nameoncard` = \'%s\', `paymentType` = \'%s\' " \
                        "WHERE `UserID` = %d ;" \
                        % (val_cardno, val_expyear, val_expmonth, val_CVV, val_nameoncard.upper(), val_cardtype, userid)

        sadatainsert = "INSERT INTO `bookstore`.`address`" \
                       "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                       "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'ship', \'%d\');" \
                       % (
                           val_shipname, val_streetaddress, val_aptno, val_inputZip, val_inputCity, val_inputState,
                           userid)

        badatainsert = "INSERT INTO `bookstore`.`address`" \
                       "(`name`, `street`, `street2`, `zipCode`, `city`, `state`, `AddressType`, `userID`)" \
                       "VALUES( \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', 'bill', \'%d\');" \
                       % (val_billname, val_billstreetaddress, val_billaptno, val_billinputZip, val_billinputCity,
                          val_billinputState, userid)

        paydatainsert = "INSERT INTO `bookstore`.`payment`" \
                        "(`cardNumber`, `expiryYear`, `expiryMonth`, `securityCode`, `paymentType`, `UserID`, `nameoncard`)" \
                        "VALUES( \'%s\' , \'%d\', \'%d\', \'%d\' , \'%s\', \'%d\', \'%s\' );" \
                        % (val_cardno, val_expyear, val_expmonth, val_CVV, val_cardtype, userid, val_nameoncard.upper())

        set_query(pdataupdate)

        if sadataex != ():
            set_query(sadataupdate)
        else:
            set_query(sadatainsert)

        if badataex != ():
            set_query(badataupdate)
        else:
            set_query(badatainsert)

        if paydataex != ():
            set_query(paydataupdate)
        else:
            set_query(paydatainsert)

        ses_email = session.get('email')
        body_text = ''' You have successfully updated your profile information.'''
        send_message(body_text, ses_email)
        flash('You have sucessfully updated your profile information.')
        return redirect(url_for('view_profile'))


@app.route('/change_password')
def change_password_start():
    return render_template('change_password.html')


@app.route('/password_changed', methods=['GET', 'POST'])
def password_change_finished():
    cur = mysql.connection.cursor()
    val_email = session.get('email')
    oldp = request.form['oldp']
    val_newpass = request.form['newpass']
    val_rnewpass = request.form['rnewpass']
    stage_1_conf = "SELECT email, password FROM `bookstore`.`users`" \
                   "where email=\'%s\'" \
                   % val_email
    res1 = get_query(stage_1_conf)

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
        set_query(password_change)

        body_text = ''' You have successfully changed your password.'''
        send_message(body_text, val_email)

        flash('Password Successfully Changed')
        return redirect(url_for('edit_profile'))


@app.route('/add2cart', methods=['GET', 'POST'])
def add2cart():
    if session.get('logged_in') == True and session.get('userTypeID') == 2:
        uid = int(session.get('userID'))
        val_ISBN = request.form['book_ISBN_h']
        val_price = request.form['book_price_h']

        isbn_search = "SELECT * FROM `bookstore`.`cart` WHERE `userID` = \'%d\' AND `bookID` = \'%s\';" % (
            uid, val_ISBN)
        isbn_search_res = get_query(isbn_search)
        # if isbn is not in the cart
        # insert
        if len(isbn_search_res) == 0:
            insert_in_cart = "insert ignore into `bookstore`.`cart` (`userID`, `bookID`, `quantity`) " \
                             "values (\'%d\', \'%s\', \'%d\');" % (uid, val_ISBN, 1)
            set_query(insert_in_cart)
        else:
            # else update
            get_quantity = int(isbn_search_res[0]['quantity'])
            update_quantity = "update `bookstore`.`cart` " \
                              "set `quantity` = \'%d\' " \
                              "where (`userID` = \'%d\') and (`bookID` = \'%s\');" \
                              % (get_quantity + 1, uid, val_ISBN)
            set_query(update_quantity)

        # get cart total
        get_cart_items = "select  `cart`.* , `bookinventory`.`sellingPrice` from `cart` " \
                         "inner join `bookinventory`" \
                         "on `cart`.`bookID` = `bookinventory`.`bookID`" \
                         "where `cart`.`userID` = \'%d\';" % uid
        get_cart_items = get_query(get_cart_items)
        tot = get_cart_total(get_cart_items)

        pending_order_search = "select * from `bookstore`.`order` " \
                               "where (`userID` = \'%d\') and (`orderstatus` = 'pending');" % uid
        pending_order_res = get_query(pending_order_search)
        if len(pending_order_res) == 0:
            # insert into order
            insert_in_order = "insert into `bookstore`.`order` (`userID`, `total`, `orderDateTime`, `orderstatus`) " \
                              "values (\'%d\', \'%.2f\', \'%s\', \'%s\');" \
                              % (uid, tot, datetime.today().strftime('%Y-%m-%d'), 'pending')
            set_query(insert_in_order)
        elif pending_order_res[0]['PromoID'] == -1:
            update_in_order_wo_promo = "update `bookstore`.`order` " \
                                       "set `total` = \'%.2f\'" \
                                       "where (`userID` = \'%d\') and (`orderstatus` = \'%s\')" \
                                       % (tot, uid, 'pending')
            set_query(update_in_order_wo_promo)
        else:
            disc_search = "select `discountAmount` from `bookstore`.`promotion` " \
                          "where `idPromotion` = \'%d\'" % int(pending_order_res[0]['PromoID'])
            disc_amount = int(get_query(disc_search)[0]['discountAmount'])
            fintot = tot - tot * disc_amount / 100
            update_in_order_promo = "update `bookstore`.`order` " \
                                    "set `total` = \'%.2f\'" \
                                    "where (`userID` = \'%d\') and (`orderstatus` = \'%s\')" \
                                    % (fintot, uid, 'pending')
            set_query(update_in_order_promo)
        flash('Item successfully added to cart.')
        return redirect(url_for('bookshow', book_num=val_ISBN))
    else:
        flash('You are not allowed to add to the cart')
        return redirect(url_for('index'))


@app.route('/add_book_action', methods=['GET', 'POST'])
def add_book_action():
    val_title = request.form['title']
    val_author = request.form['author']
    val_ISBN = request.form['ISBN']
    val_edition = conv_int(request.form['edition'])
    val_publisher = request.form['publisher']
    val_pubYear = conv_int(request.form.get('pubYear'))
    val_category = conv_int(request.form.get('category'))
    val_cover = request.files['cover']
    val_buyingPrice = conv_float(request.form['buyingPrice'])
    val_sellingPrice = conv_float(request.form['sellingPrice'])
    val_quantity = conv_int(request.form['quantity'])
    print(val_title, val_author, val_ISBN, val_edition, val_pubYear, val_publisher, val_category, val_sellingPrice,
          val_sellingPrice)
    inputlist = [val_title, val_author, val_ISBN, val_publisher]
    typelist = ['title', 'author', 'ISBN', 'publisher']

    [validate, flash_messages] = validate_all_input(inputlist, typelist)

    if (validate is True) and (val_edition != 0) and (val_pubYear != 0) and \
            (val_category != 0) and val_buyingPrice is not None \
            and val_sellingPrice is not None and val_cover is not '':

        filename = photos.save(request.files['cover'], name=val_ISBN + '_cover.jpg')
        filepath = 'images/books/' + filename

        book_insert = "INSERT INTO `bookstore`.`books`" \
                      "(`ISBN`, `author`, `title`, `cover`, `edition`, `publisher`, `pubYear`, `category`)" \
                      " VALUES( \'%s\', \'%s\', \'%s\', \'%s\', \'%d\', \'%s\', \'%d\', \'%d\' ); " \
                      % (
                          val_ISBN, val_author, val_title, filepath, val_edition, val_publisher, val_pubYear,
                          val_category)

        inventory_insert = "INSERT INTO `bookstore`.`bookinventory`" \
                           "(`bookID`, `bookStatus`, `buyingPrice`, `sellingPrice`, `quantity`)" \
                           "VALUES (\'%s\', 'Available', \'%.2f\', \'%.2f\', \'%d\'); " \
                           % (val_ISBN, val_buyingPrice, val_sellingPrice, val_quantity)

        if set_query(book_insert) and set_query(inventory_insert):
            flash('Book Successfully Added')
            return redirect(url_for('index'))
        else:
            flash('Duplicate Book')
            return redirect(url_for('add_book'))

    elif validate is False:
        flash(flash_messages)
        return redirect(url_for('add_book'))
    elif val_edition == 0:
        flash('Enter a valid Edition Number')
        return redirect(url_for('add_book'))
    elif val_pubYear == 0:
        flash('Choose Publication Year')
        return redirect(url_for('add_book'))
    elif val_category == '0':
        flash('Choose category')
        return redirect(url_for('add_book'))
    elif val_buyingPrice is None:
        flash('Invalid Buying Price')
        return redirect(url_for('add_book'))
    elif val_sellingPrice is None:
        flash('Invalid Selling Price')
        return redirect(url_for('add_book'))
    elif val_cover is '':
        flash('Choose a cover for the book')
        return redirect(url_for('add_book'))


@app.route('/search_book_action', methods=['GET', 'POST'])
def search_book_action():
    return 'Needs to be implemented by Sakher/Divya/Andres/Redwan'


@app.route('/get_EOD')
def get_EOD():
    return 'Needs to be implemented by Sakher/Divya/Andres/Redwan'


@app.route('/get_Inventory')
def get_Inventory():
    return 'Needs to be implemented by Sakher/Divya/Andres/Redwan'


@app.route('/modify_cart_action', methods=['GET', 'POST'])
def modify_cart_action():
    uid = int(session.get('userID'))
    keylist = []
    vallist = []
    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            keylist.append(key)
            vallist.append(conv_int(value))

    for k in range(0, len(keylist)):
        updatequery = "UPDATE `bookstore`.`cart` " \
                      "SET `quantity` = \'%d\' " \
                      "WHERE (`userID` = \'%d\') and (`bookID` = \'%s\');" \
                      % (vallist[k], uid, keylist[k])
        set_query(updatequery)

    return redirect(url_for('cart'))


@app.route('/remove_from_cart_action', methods=['GET', 'POST'])
def remove_from_cart_action():
    uid = int(session.get('userID'))
    keylist = []
    f = request.form
    for key in f.keys():
        del_query = "delete from `bookstore`.`cart` " \
                    "where `bookID` = \'%s\' and userID = \'%d\' " \
                    % (key, uid)
        set_query(del_query)
    return redirect(url_for('cart'))


@app.route('/apply_promo_action', methods=['GET', 'POST'])
def apply_promo_action():
    uid = int(session.get('userID'))
    inputpromo = str(request.form['promocode']).strip()
    dt = datetime.today().date()
    dtstr = dt.strftime('%Y-%m-%d')
    search_validity = "select * from `bookstore`.`promotion`" \
                      "where `startDate` < \'%s\' and `promoCode` = \'%s\'" \
                      % (dtstr, inputpromo)
    init_search = get_query(search_validity)
    if len(init_search) == 0:
        flash('Invalid Promo')
        return redirect(url_for('apply_promo'))
    elif datetime.strptime(str(init_search[0]['expirationDate']), '%Y-%m-%d').date() < dt:
        flash('Expired Promo')
        return redirect(url_for('apply_promo'))
    else:
        update_promo = "update `bookstore`.`order` " \
                       "set `PromoID` = \'%d\'" \
                       "where `userID` = \'%d\' and `orderstatus` = 'pending'" \
                       % (init_search[0]['idPromotion'], uid)
        set_query(update_promo)
        return redirect(url_for('cart'))


@app.route('/checkout_action', methods=['GET', 'POST'])
def checkout_action():
    uid = int(session.get('userID'))
    # transfer cart items to order items

    # get cart items
    cart_query = "SELECT * FROM `bookstore`.`cart` WHERE `userID`=\'%d\'" % uid
    cartItems = get_query(cart_query)

    # inventory relation
    inventory_after = "SELECT `cart`.* , `bookinventory`.`quantity` as `totcount`," \
                      "`bookinventory`.`quantity`-`cart`.`quantity` as `rem` FROM `bookstore`.`cart`" \
                      "inner join `bookinventory`" \
                      "on `cart`.`bookID` = `bookinventory`.`bookID`" \
                      "where `bookinventory`.`quantity`-`cart`.`quantity` > 0 and `userID` = \'%d\';" % uid

    inventory_problem = "SELECT `cart`.*, `bookinventory`.`quantity` as `totcount`," \
                        "`bookinventory`.`quantity`-`cart`.`quantity` as `rem` FROM `bookstore`.`cart`" \
                        "inner join `bookinventory`" \
                        "on `cart`.`bookID` = `bookinventory`.`bookID`" \
                        "where `bookinventory`.`quantity`-`cart`.`quantity` < 0 and `userID` = \'%d\';" % uid

    # get payment info
    pay_query = "SELECT * FROM `bookstore`.`payment` WHERE `userID`=\'%d\'" % uid
    pay = get_query(pay_query)
    # get billShipping info
    bill_query = "SELECT * FROM `bookstore`.`address` WHERE `userID`=\'%d\' AND `AddressType`=\'bill\'" % uid
    bill = get_query(bill_query)
    # get shippingAddy
    ship_query = "SELECT * FROM `bookstore`.`address` WHERE `userID`=\'%d\' AND `AddressType`=\'ship\'" % uid
    ship = get_query(ship_query)

    # if cart is empty
    if len(cartItems) == 0:
        flash('Your cart is empty.')
        return redirect(url_for('index'))
    # if shipping/billing info is missing
    elif len(pay) == 0 or len(bill) == 0 or len(ship) == 0:
        flash('Please enter Shipping/Billing Address and/or payment.')
        return redirect(url_for('edit_profile'))
    # if items greater than inventory
    elif len(get_query(inventory_problem)) != 0:
        flash('Desired Quantities not available. Go to cart to modify items')
        return redirect(url_for('checkout'))
    else:
        print(request.form['orderid'])
        print(len(cartItems))
        orderid = int(request.form['orderid'])
        inventory_update = get_query(inventory_after)
        print(inventory_update)
        for jj in range(0, len(cartItems)):
            insert_order_item = "insert into `bookstore`.`orderitems`" \
                                "(`orderID`, `ProductID`, `quantity`)" \
                                "values (\'%d\', \'%s\', \'%d\') " \
                                % (orderid, cartItems[jj]['bookID'], cartItems[jj]['quantity'])
            set_query(insert_order_item)

        for jj in range(0,len(inventory_update)):
            update_inventory = "update `bookstore`.`bookinventory`" \
                               "set `quantity` = \'%d\'" \
                               "where `bookID` = \'%s\'" \
                                % (int(inventory_update[jj]['rem']),inventory_update[jj]['bookID'] )
            set_query(update_inventory)

        # clear cart
        del_query = "delete from `bookstore`.`cart` " \
                    "where userID = \'%d\' " \
                    % uid
        set_query(del_query)

        #make orderstatus active
        update_order = "update `bookstore`.`order`" \
                       "set `orderstatus` = 'active'" \
                       "where `orderID` = \'%d\' " % orderid
        set_query(update_order)
        return redirect(url_for('order_confirmation'))


@app.route('/cancel_order/<int:id>', methods=['GET', 'POST'])
def cancel_order(id):
    set_cancel = "update `order` " \
                 "set `orderstatus` = 'cancelled'" \
                 "where orderID = \'%d\'" % id
    set_query(set_cancel)
    return redirect(url_for('order_history'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
