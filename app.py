from flask import Flask, render_template

app = Flask(__name__)


# redirect link to homepage
@app.route('/')
def index():
    return render_template('index.html')


# redirect link to login
@app.route('/login')
def login():
    return render_template('login.html')


# redirect link to register
@app.route('/register')
def register():
    return render_template('register.html')


# redirect link to cart
@app.route('/cart')
def cart():
    return render_template('cart.html')

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

if __name__ == '__main__':
    app.run(debug=True)

