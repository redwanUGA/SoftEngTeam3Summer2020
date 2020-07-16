from flask import Flask
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_mysqldb import MySQL

from flask_mail import Mail, Message

import re

app = Flask(__name__, static_url_path='/static')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'bookstore'

mysql = MySQL(app)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='box5928.bluehost.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 't3@myw.urq.mybluehost.me',
	MAIL_PASSWORD = '78rehkas'
	)
mail = Mail(app)

template_head = '''
	<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    <link rel="stylesheet" href="/static/style.css" type="text/css" />
    <script type="text/javascript">
        window.onload = initiate;
        function initiate() {
        //var search_query=document.getElementById(\'search_query\');
        var menu_closed=true;
        var menu_content=document.getElementById(\'menu_content\');
        var mobile_button=document.getElementById(\'mobile_button\');
        mobile_button.onclick=function(){
        if(menu_closed) {
        menu_closed=false;
        menu_content.style.display=\'block\';
        menu_content.style.height=\'70%\';
        } else {
        menu_content.style.display=\'none\';
        menu_content.style.height=\'0%\';
        menu_closed=true;
        }
        };
        };
    </script>
    <title>'''#template_head
template_body = '''</title>
</head>
<body>
    <div id="div1">
        <header class="container-fluid">

            <div>
                <a href="#" id="logo"><img src="/static/images/icons/books-icon.png" alt="team3" /> Team#3 BookStore</a>
            </div>
            <div>
                <form><input type="search" name="search_query" id="search_query" value="Search ..." onclick="this.value=\'\';" /></form>
            </div>

        </header><!-- container -->
        <div id="menu">
            <ul id="menu_content">
                <li><a href="index.html">Home</a></li>
                <li>
                    <a href="#">Categories</a><ul>
                        <li><a href="#">Classic</a></li>
                        <li><a href="#">Romance</a></li>
                        <li><a href="#">Technology</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">Browse</a>
                </li>
                <li>
                    <a href="#">Help</a><ul>
                        <li><a href="#">Support Request</a></li>
                        <li><a href="#">FAQs</a></li>
                        <li><a href="search.html">Advanced Search</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">About</a>
                </li>
            </ul>

            <div id="mobile_button">
                <img src="/static/images/menu.png" />
            </div>
            <div id="user_controls">
                <ul>
                    <li><a href="cart.html"><img src="/static/images/cart.png" />MY CART</a></li>
                    <li><a href="login.html"><img src="/static/images/signin.png" />SING IN</a></li>
                    <li><a href="register.html"><img src="/static/images/signup.png" />SIGN UP</a></li>
                </ul>
            </div>
        </div>
        <div id="main_content">
        '''#template_body
template_footer = '''  </div><!-- main_content -->
        <footer>
            team 3 book store
        </footer>
    </div><!-- div1 -->

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
</body>
</html>

	'''#template_footer
#@app.route('/<name>')
#def index(name):
#	
#	return template
@app.route('/register', methods=('GET', 'POST'))
def register():

    email = 'sakher.x@gmail'
    password =  ''
    fname =  'sakher'
    lname =  'qaaidi'
    phone =  ''
    subscribe =  1
    msg=''
    userid=0
    activationKey=1234

    address='101 hardsman'
    city='Athens'
    state='GA'
    zip_code='30605'
    country='USA'

    cc='1234789565471230'
    mnth='08'
    yr='2030'
    visa=''
    mastercard=''
    csv=''
    cctype=''




    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password1']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        country = request.form['country']
        cc = request.form['cc']
        mnth = request.form['mnth']
        yr = request.form['yr']
        csv = request.form['csv']
        if len(csv)<1 :
            csv=None
        visa=''
        mastercard=request.form['cctype']
        if request.form['cctype'] == 'visa':
            visa='Selected'
            cctype='visa'
        else:
            mastercard='Selected'
            cctype='mastercard'

        if not request.form['subscribe']:
            subscribe = 0
        else:
            subscribe = 1
        if len(password)<8: ######################### change it to 8
            msg+='Password should be 8 digits at least'
        if len(fname)<1:
            msg+='You should provide a first name'
        if len(lname)<1:
            msg+='You should provide a last name'
        if bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email)) == False:
            msg+='You should provide a valid email'

        email = email.lower()
        ####################### activationKey

        if len(msg)<1:
            try:
                cur = mysql.connection.cursor()
                #cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
                cur.execute('''INSERT INTO `users`
                (`firstName`,
    `lastName`,
    `password`,
    `email`,
    `phone`,
    `userTypeID`,
    `Subscription`,
    `active`,
    `activationKey`,
    `suspended`
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(
    fname,
    lname,
    generate_password_hash(password),
    email,
    phone,
    2,
    subscribe,
    0,
    activationKey,0));

                mysql.connection.commit()
                userid=cur.lastrowid
                cur.close()
            except Exception as e:
                msg+='Error, please try again later<br />'+str(e)
            finally:
                cur.close()

            if len(address) > 0:
                try:
                    cur = mysql.connection.cursor()
                    cur.execute('''INSERT INTO `Address`
                
    (
    `name`,
    `street`,
    `street2`,
    `zipCode`,
    `city`,
    `state`,
    `country`,
    `AddressType`,
    `userID`)

     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(
        address,
        address,
        address,
        zip_code,
        city,
        state,
        country,
        'Ship',
        userid));

                    mysql.connection.commit()
                    cur.close()
                except Exception as e:
                    msg+='Error in address, please try again later<br />'+str(e)
                finally:
                    cur.close()

            if len(cc)>0:
                try:
                    cur = mysql.connection.cursor()
                    #cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
                    cur.execute('''INSERT INTO `payment`
            
        (`cardNumber`,
        `expiryYear`,
        `expiryMonth`,
        `securityCode`,
        `paymentType`,
        `UserID`

        ) VALUES (%s,%s,%s,%s,%s,%s)''',(
        generate_password_hash(cc),
        mnth,
        yr,
        csv,
        cctype,
        userid));

                    mysql.connection.commit()
                    cur.close()
                except Exception as e:
                    msg+='Error payment, please try again later<br />'+str(e)
                finally:
                    cur.close()
        

        if len(msg)>0:
            msg='<div class="msg">'+msg+'</div>'
        else:
            try:
                msgg = Message("Team3 Book Store",sender="t3@myw.urq.mybluehost.me",recipients=[email])
                msgg.body ="Thank you for registering, to activate your account you have to enter the following code when logging in : "+activationKey
                mail.send(msgg)
            except Exception as e:
                msg = str(e) ################### change to nothing
            return redirect('/confirmation')
    elif request.method == 'GET':
        nothing = False

    page_content = '''
    <h2>Registration Form</h2>
    <form method="post" action="/register">

    '''+msg+'''

    <div class="field_label">Email address *</div>
    <div class="field"><input type="text" name="email" value="'''+email+'''" /></div>

    <div class="field_label">Password *</div>
    <div class="field"><input type="password" id="password1" name="password1" />
    <span>Must be 8 digits at least</span>
    </div>

    <div class="field_label">Confirm Password *</div>
    <div class="field"><input type="password" id="password2" name="password2" /></div>
    
    <div class="field_label">First Name *</div>
    <div class="field"><input type="text" name="fname" value="'''+fname+'''" /></div>

    <div class="field_label">Last Name *</div>
    <div class="field"><input type="text" name="lname" value="'''+lname+'''" /></div>
    
    <div class="field_label">Phone Number</div>
    <div class="field"><input type="text" name="phone" value="'''+phone+'''" /></div>

    <div class="field_label">Subscribe</div>
    <div class="field"><input type="checkbox" name="subscribe" checked="checked" />
    <span>Subscribe to newsletter and promotions</span></div>
    
    <div>Address</div>
    
    <div class="field_label">Address line</div>
    <div class="field"><input type="text" name="address" value="'''+address+'''" /></div>
    <div class="field_label">City</div>
    <div class="field"><input type="text" name="city" value="'''+city+'''" /></div>
    <div class="field_label">State</div>
    <div class="field"><input type="text" name="state" size="4" value="'''+state+'''" />
    <span>Enter 2 characters state, ex: GA</span>
    </div>
    
    <div class="field_label">Zip code</div>
    <div class="field"><input type="text" name="zip_code" value="'''+zip_code+'''" /></div>

    <div class="field_label">Country</div>
    <div class="field"><input type="text" name="country" value="'''+country+'''" />
    </div>

    <div>Payment info</div>
    
    <div class="field_label">Credit Card Number</div>
    <div class="field"><input type="text" name="cc" value="'''+cc+'''" /></div>
    <div class="field_label">Expiry month</div>
    <div class="field"><input type="text" name="mnth" size="4" value="'''+mnth+'''" />
    <span>Enter 2 digits month, ex: 12</span>
    </div>
    <div class="field_label">Expiry year</div>
    <div class="field"><input type="text" name="yr" size="4" value="'''+yr+'''" />
    <span>Enter 4 digits year, ex: 2030</span>
    </div>
    <div class="field_label">CSV code</div>
    <div class="field"><input type="text" name="csv" size="4" value="'''+csv+'''" />
    <span>On the back of the card</span>
    </div>
    
    <div class="field_label">Card Type</div>
    <div class="field"><select name="cctype"><option value="visa" '''+visa+'''>Visa</option><option value="mastercard" '''+mastercard+'''>Mastercard</option></select></div>
    
    <div class="field_label"></div>
    <div class="field">* Required fields <br /><input type="submit" text="Register" onclick=" if( document.getElementById(\'password1\').value != document.getElementById(\'password2\').value ) { alert(\'Passwords do not match!\'); return false; }" /></div>

    </form>
    '''

    return template_head+'Create an Account'+template_body+page_content+template_footer
@app.route('/', methods=('GET', 'POST'))
def index():
    index_template = '''<h1>Welcome</h1>

            <h2>Featured Books</h2>

            <a class="book" href="book.html?img=/images/books/05.jpg&title=Software Engineering&author=Sommerville&price=15">
                <img src="/static/images/books/05.jpg" />
                <span>Software Engineering</span>
                <span>SommerVille</span>
                <span>$15</span>
                <span>ISBN: 123456987</span>
            </a>

            <a class="book" href="book.html?img=images/books/06.jpg&title=Computer Networks&author=Andrew S. Tanenbaum&price=25">
                <img src="/static/images/books/06.jpg" />
                <span>Computer Networks</span>
                <span>Andrew S. Tanenbaum</span>
                <span>$25</span>
                <span>ISBN: 123456987</span>
            </a>

            <a class="book" href="book.html?img=images/books/03.jpg&title=C How to program&author=Dietel&price=40">
                <img src="/static/images/books/03.jpg" />
                <span>C How to program</span>
                <span>Dietel</span>
                <span>$40</span>
                <span>ISBN: 123456987</span>
            </a>

            <h2>Top Sellers</h2>

            <a class="book" href="book.html?img=images/books/02.jpg&title=Data Mining&author=Vipin Kumar&price=50">
                <img src="/static/images/books/02.jpg" />
                <span>Data Mining</span>
                <span>Vipin Kumar</span>
                <span>$50</span>
                <span>ISBN: 123456987</span>
            </a>

            <a class="book" href="book.html?img=images/books/04.jpg&title=Operating Systems&author=Greg Gagne&price=18">
                <img src="/static/images/books/04.jpg" />
                <span>Operating Systems</span>
                <span>Greg Gagne</span>
                <span>$18</span>
                <span>ISBN: 123456987</span>
            </a>

            <a class="book" href="book.html?img=images/books/01.jpg&title=Rome History&author=John Smith&price=15">
                <img src="/static/images/books/01.jpg" />
                <span>Rome History</span>
                <span>John Smith</span>
                <span>$15</span>
                <span>ISBN: 123456987</span>
            </a>
            ''' #index_template

    return template_head+'Team3 Book Store'+template_body+index_template+template_footer
@app.route('/confirmation', methods=('GET', 'POST'))
def confirmation():
    page_content = '''

            <div class="msg">Account has been created, please activate it using the code that was sent to your email.</div>
            ''' #page_content

    return template_head+'Confirmation'+template_body+page_content+template_footer
    
if __name__=='__main__':
    app.run()