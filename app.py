from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import random
import json
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://linlbopoiknkri:82beb352c58d03e9e580c00f5d8434b56bc4ae9b4868d08106641df8380f1a53@ec2-54-77-90-39.eu-west-1.compute.amazonaws.com:5432/dcaur7p267os7d'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'zybrzubryachestiy'
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'taide.catering@gmail.com'
app.config['MAIL_PASSWORD'] = 'helpporuoanpito'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class Localization:
    dictionary_eng = {
        'menu_artcatering': 'Art Catering',
        'menu_menus': 'Menus',
        'menu_create': 'Create',
        'menu_calendar': 'Calendar',
        'menu_signup': 'Sing up',
        'menu_contact': 'Contact',
        'menu_aboutus': 'About us',
        'menu_admin': 'Admin',
        'menu_logout': 'Logout',
        'signin_title': 'Sign-up or register',
        'signin_text1': 'Get 5% discount by making order via our web-page',
        'signin_text2': 'For new customers only - Get additional 5% new customer welcome discount by registering on our web-site.',
        'signin_button': 'Sign-in',
        'signin_smalltext1': 'By clicking Sign up, you agree to the terms of use.',
        'signin_smalltext2': "Don't have an account? ",
        'signin_smalltext3': "Register here."


    }

    dictionary_fi = {
        'menu_artcatering': 'Art Catering',
        'menu_menus': 'Menus',
        'menu_create': 'Luoda',
        'menu_calendar': 'Kalenteri',
        'menu_signup': 'Kirjaudu',
        'menu_contact': 'Ota yhteyttä',
        'menu_aboutus': 'Meistä',
        'menu_admin': 'Admin',
        'menu_logout': 'Ulos',
        'signin_title': 'Kirjaudu tai rekisteröidy',
        'signin_text1': 'Saat 5% alennuksen tekemällä tilauksen nettisivujemme kautta',
        'signin_text2': 'Vain uusille asiakkaille - Saat ylimääräisen 5% uusien asiakkaiden tervetuloalennuksen rekisteröitymällä verkkosivuillemme.',
        'signin_button': 'Kirjaudu',
        'signin_smalltext1': 'Klikkaamalla Rekisteröidy hyväksyt käyttöehdot.',
        'signin_smalltext2': 'Eikö sinulla ole tiliä? ',
        'signin_smalltext3': 'Rekisteröidy täällä.'

    }

    dictionary_ru = {
        'menu_artcatering': 'Art Кейтеринг',
        'menu_menus': 'Меню',
        'menu_create': 'Создать',
        'menu_calendar': 'Календарь',
        'menu_signup': 'Войти',
        'menu_contact': 'Контакты',
        'menu_aboutus': 'О нас',
        'menu_admin': 'Админ',
        'menu_logout': 'Выйти',
        'signin_title': 'Kirjaudu tai rekisteröidy',
        'signin_text1': 'Saat 5% alennuksen tekemällä tilauksen nettisivujemme kautta',
        'signin_text2': 'Vain uusille asiakkaille - Saat ylimääräisen 5% uusien asiakkaiden tervetuloalennuksen rekisteröitymällä verkkosivuillemme.',
        'signin_button': 'Kirjaudu',
        'signin_smalltext1': 'Klikkaamalla Rekisteröidy hyväksyt käyttöehdot.',
        'signin_smalltext2': 'Eikö sinulla ole tiliä? ',
        'signin_smalltext3': 'Rekisteröidy täällä.'
    }

    dict = {'EN': dictionary_eng, 'FI': dictionary_fi, 'RU': dictionary_ru}

    def return_dictionary(lang):
        if lang == 'FI':
            dictionary = Localization.dict['FI']
        elif lang == 'EN':
            dictionary = Localization.dict['EN']
        elif lang == 'RU':
            dictionary = Localization.dict['RU']
        return dictionary


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), primary_key=False)
    price = db.Column(db.Integer)
    category = db.Column(db.String(100), primary_key=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200))
    updatetime = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<products {self.id}>"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), primary_key=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=True)
    updatetime = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<users {self.id}>"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), primary_key=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(300), nullable=False)
    message = db.Column(db.VARCHAR(1000), nullable=False)
    updatetime = db.Column(db.Date, default=datetime.utcnow)
    publicity = db.Column(db.String(100), default="No")
    replied = db.Column(db.String(100), default="No")

    def __repr__(self):
        return f"<feedback {self.id}>"


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer(), nullable=False)
    subject = db.Column(db.VARCHAR(200), nullable=False)
    message = db.Column(db.VARCHAR(1000), nullable=False)
    updatetime = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<reply {self.id}>"


db.create_all()


class Item:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.total = self.quantity * self.product.price

    def item_get_id(self):
        return self.product.id

    def item_change_quantity(self):
        self.quantity = self.quantity + 1
        self.total = self.quantity * self.product.price

    def get_quantity(self):
        return self.quantity

    def get_item_total_price(self):
        return self.product.price * self.quantity

    def to_string(self):
        return "ID: " + str(self.product.id) + " Quantity: " + str(self.quantity)


class ShoppingCard:
    def __init__(self):
        self.productlist = []

    def additem(self, item):
        added = False
        for element in self.productlist:
            if element.item_get_id() == item.item_get_id():
                element.item_change_quantity()
                added = True
                break

        if not added:
            self.productlist.append(item)

    def deleteitem(self, id):
        for element in self.productlist:
            if element.item_get_id() == id:
                self.productlist.remove(element)

    def count_card_total(self):
        card_total = 0
        for element in self.productlist:
            card_total = card_total + element.total
        return card_total

    def to_string(self):
        for_print = "shopping cart: "
        for element in self.productlist:
            for_print = for_print + ", " + element.to_string()
        return for_print


@app.route('/')
@app.route('/index')
def indexpage():  # put application's code here
    if not session['user_lang']:
        session['user_lang'] = "EN"
    dictionary = Localization.return_dictionary(session['user_lang'])
    return render_template("index.html", dictionary=dictionary)


@app.route('/<string:lang>')
def change_lang(lang):
    if lang == 'fi':
        session['user_lang'] = "FI"
    elif lang == 'en':
        session['user_lang'] = "EN"
    elif lang == 'ru':
        session['user_lang'] = "RU"

    dictionary = Localization.return_dictionary(session['user_lang'])

    return render_template("index.html", dictionary = dictionary)

@app.route('/admin')
def admin():  # put application's code here
    dictionary = Localization.return_dictionary(session['user_lang'])
    return render_template("adminmain.html", dictionary=dictionary)


@app.route('/menus')
def menus():  # put application's code here
    dictionary = Localization.return_dictionary(session['user_lang'])
    return render_template("menus.html", dictionary=dictionary)


@app.route('/shop')
def shopcreate():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = Products.query.all();

    return render_template("create.html", products=products, dictionary=dictionary)


@app.route('/shop/<int:id>/readmore')
def readmore(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product = Products.query.get_or_404(id)
    return render_template("productpage.html", product=product, dictionary=dictionary)


@app.route('/shop/<int:id>/addtocard')
def addtocard(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product = Products.query.get_or_404(id)

    user_id = session['user_id']

    if 'user_cart' in session:
        product_string = str(product.id) + ", "
        session['user_cart'] = session['user_cart'] + product_string


    else:

        product_string = str(product.id) + ", "
        session['user_cart'] = product_string


    return redirect("/shop")


@app.route('/shoppingcard/<int:id>/delete')
def delete_item_shoppingcard(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product_id = str(id)
    user_id = session['user_id']
    old_cart = session['user_cart'].split(", ")
    old_cart.remove("")
    new_cart = []
    for el in old_cart:
        if el == product_id:
           continue

        else:
            new_cart.add(el)

    new_shopping_cart = ""
    for el in new_cart:
        new_shopping_cart = new_shopping_cart + el +", "

    session['user_cart'] = new_shopping_cart
    print("New_shopping_cart")
    print (new_shopping_cart)

    return redirect("/shoppingcard")

@app.route('/shoppingcard/<int:id>/minus')
def minus_item_shoppingcard(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product_id = str(id)
    user_id = session['user_id']
    old_cart = session['user_cart'].split(", ")
    old_cart.remove("")
    for el in old_cart:
        if el == product_id:
            old_cart.remove(product_id)
            break

    new_shopping_cart = ""
    for el in old_cart:
        new_shopping_cart = new_shopping_cart + el + ", "

    session['user_cart'] = new_shopping_cart
    print("New_shopping_cart")
    print (new_shopping_cart)

    return redirect("/shoppingcard")

@app.route('/shoppingcard/<int:id>/plus')
def plus_item_shoppingcard(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product_id = str(id)
    session['user_cart'] = session['user_cart']+ product_id +", "

    return redirect("/shoppingcard")


@app.route('/shoppingcard')
def shoppingcard():
    dictionary = Localization.return_dictionary(session['user_lang'])
    user_id = session['user_id']

    if not session['user_cart']:
        return render_template("shoppingcardempty.html", dictionary=dictionary)

    else:
        cart = session['user_cart'].split(", ")
        cart.remove("")
        cart.sort()
        print(cart)

        if len(cart) == 0:
            return render_template("shoppingcardempty.html", dictionary=dictionary)

        else:
            products_in_card = {}
            counter = 1

            for i in range(len(cart)):
                if i == len(cart)-1:
                    products_in_card[cart[i]] = counter
                    break

                if cart[i] == cart[i+1]:
                    counter = counter+1

                else:
                    products_in_card[cart[i]] = counter
                    counter = 1

        cart_full = ShoppingCard()
        for key in products_in_card:
            print(key)
            product_id = key
            if product_id!= "" and product_id!= " ":
                quantity = products_in_card[product_id]
                print(quantity)

                product = Products.query.get_or_404(product_id)
                print("Price :" )
                print(product.price)

                item_card = Item(product, quantity)
                print (item_card.to_string())
                item_card.get_item_total_price()
                cart_full.additem(item_card)

        total = cart_full.count_card_total()
        alv = total*0.24
        alv = float('{:.2f}'.format(alv))
        return render_template("shoppingcard.html", cart=cart_full, alv=alv, total=total, dictionary=dictionary)


@app.route('/checkout/')
def checkout():
    dictionary = Localization.return_dictionary(session['user_lang'])
    user_id = session['user_id']

    if not session['user_cart']:
        return render_template("shoppingcardempty.html", dictionary=dictionary)

    else:
        cart = session['user_cart'].split(", ")
        cart.remove("")
        cart.sort()
        print(cart)

        if len(cart) == 0:
            return render_template("shoppingcardempty.html", dictionary=dictionary)

        else:
            products_in_card = {}
            counter = 1

            for i in range(len(cart)):
                if i == len(cart)-1:
                    products_in_card[cart[i]] = counter
                    break

                if cart[i] == cart[i+1]:
                    counter = counter+1

                else:
                    products_in_card[cart[i]] = counter
                    counter = 1

        cart_full = ShoppingCard()
        for key in products_in_card:
            print(key)
            product_id = key
            if product_id!= "" and product_id!= " ":
                quantity = products_in_card[product_id]
                print(quantity)

                product = Products.query.get_or_404(product_id)
                print("Price :" )
                print(product.price)

                item_card = Item(product, quantity)
                print (item_card.to_string())
                item_card.get_item_total_price()
                cart_full.additem(item_card)

        total = cart_full.count_card_total()
        alv = total*0.24
        alv = float('{:.2f}'.format(alv))
        return render_template("checkout.html", cart=cart_full, alv=alv, total=total, dictionary=dictionary)




@app.route('/about')
def about():  # put application's code here
    dictionary = Localization.return_dictionary(session['user_lang'])
    return render_template("about.html", dictionary=dictionary)


@app.route('/contact')
def contacts():  # put application's code here
    dictionary = Localization.return_dictionary(session['user_lang'])
    return render_template("contacts.html", dictionary=dictionary)


@app.route('/contact', methods=['POST', 'GET'])
def feedback():
    dictionary = Localization.return_dictionary(session['user_lang'])
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        subject = request.form['customertext']
        message = request.form['subject']

        contact1 = Feedback(name=name, email=email, subject=subject, message=message)

        try:
            db.session.add(contact1)
            db.session.commit()
            sending_email_feedbackform(name, email)
            return redirect('/', dictionary=dictionary)

        except:

            print("При отправке вашего отзыва произошла ошибка")

            return "При отправке вашего отзыва произошла ошибка"

    return render_template("contacts.html", dictionary=dictionary)


def sending_email_feedbackform(name, email):
    msg = Message('You letter to Simple Catering.', sender='taide.catering@gmail.com', recipients=[email])
    msg.body = "Hey, " + name + "! Thank you for contacting Simple Catering! We will answer for your letter as soon as possible."
    mail.send(msg)
    return "Message sent!"


@app.route('/orders')
def admin_orders():  # put application's code here
    dictionary = Localization.return_dictionary(session['user_lang'])
    return render_template("orders.html", dictionary=dictionary)


@app.route('/productsadmin')
def productsadmin():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = Products.query.all();

    return render_template("productsadmin.html", products=products, dictionary=dictionary)


@app.route('/productsadmin/<int:id>/delete')
def deleteproduct(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product = Products.query.get_or_404(id);

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect("/productsadmin", dictionary=dictionary)
    except:
        return ("An error occurred while deleting the product")

        return redirect("/productsadmin", dictionary=dictionary)


@app.route('/productsadmin/<int:id>/update', methods=['POST', 'GET'])
def updateproduct(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product = Products.query.get(id)
    if request.method == "POST":
        print("collect info for update")
        product.id = id
        product.title = request.form['productname']
        product.price = request.form['productprice']
        product.category = request.form['category']
        product.description = request.form['subject']
        file = request.files['filename']

        if file.filename != '':
            product.photo = file.filename

        if file and file.filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        try:

            db.session.commit()
            print("commit")
            return redirect('/admin', dictionary=dictionary)

        except:
            print("При редактировании account произошла ошибка")

            return "При редактировании account произошла ошибка"

    else:
        return render_template("productupdate.html", product=product, dictionary=dictionary)


@app.route('/customersadmin/<int:id>/delete')
def deletecustomer(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    user = Users.query.get_or_404(id);

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect("/customersadmin", dictionary=dictionary)
    except:
        return ("An error occurred while deleting the product")

        return redirect("/customersadmin", dictionary=dictionary)


@app.route('/customersadmin/<int:id>/update', methods=['POST', 'GET'])
def updateuser(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    user = Users.query.get(id)
    if request.method == "POST":
        user.id = id
        user.name = request.form['name']
        user.email = request.form['email']
        if request.form['password'] == request.form['passwordRepeat']:
            user.password = request.form['password']

        try:

            db.session.commit()
            return redirect('/customersadmin', dictionary=dictionary)

        except:
            print("При редактировании account произошла ошибка")

            return "При редактировании account произошла ошибка"

    else:
        return render_template("customersadminupdate.html", user=user, dictionary=dictionary)


@app.route('/aboutuser/<int:id>/update', methods=['POST', 'GET'])
def updateuseritself(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    user = Users.query.get(id)
    if request.method == "POST":
        user.id = id
        user.name = request.form['name']
        user.email = request.form['email']
        if request.form['password'] == request.form['passwordRepeat']:
            user.password = request.form['password']

        try:

            db.session.commit()
            return redirect('/aboutuser', dictionary=dictionary)

        except:
            print("При редактировании account произошла ошибка")

            return "При редактировании account произошла ошибка"

    else:
        return render_template("customersadminupdate.html", user=user, dictionary=dictionary)


@app.route('/customersadmin')
def customerssadmin():
    dictionary = Localization.return_dictionary(session['user_lang'])
    users = Users.query.all();

    return render_template("customersadmin.html", users=users, dictionary=dictionary)


@app.route('/feedbacksadmin')
def feedbacksadmin():
    dictionary = Localization.return_dictionary(session['user_lang'])
    feedback = Feedback.query.all();

    return render_template("feedbacksadmin.html", feedback=feedback, dictionary=dictionary)


@app.route('/feedbacksadmin/<int:id>/delete')
def deletefeedback(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    feedback = Feedback.query.get_or_404(id);

    try:
        db.session.delete(feedback)
        db.session.commit()
        return redirect("/feedbacksadmin", dictionary=dictionary)
    except:
        return ("An error occurred while deleting the feedback")

        return redirect("/feedbacksadmin", dictionary=dictionary)


@app.route('/feedbacksadmin/<int:id>/reply', methods=['POST', 'GET'])
def reply_feedback(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    feedback = Feedback.query.get(id)
    customeremail = feedback.email
    if request.method == "POST":
        idreply = random.randint(100000, 999999)
        feedback_id = id
        subject = request.form['subject']
        message = request.form['message']
        publicity = "No"
        reply = "No"

        try:
            sending_reply_customerfeedback(customeremail, subject, message)
            reply = Reply(id=idreply, feedback_id=feedback_id, subject=subject, message=message)
            print(idreply)
            print(feedback_id)
            print(subject)
            print(message)
            db.session.add(reply)
            db.session.commit()
            return redirect('/feedbacksadmin', dictionary=dictionary)

        except:
            print("При редактировании account произошла ошибка")

            return "При редактировании account произошла ошибка"

    else:
        return render_template("feedbackadminreply.html", feedback=feedback, dictionary=dictionary)


def sending_reply_customerfeedback(email, subject, message):
    msg = Message(subject, sender='taide.catering@gmail.com', recipients=[email])
    msg.body = message
    mail.send(msg)
    return "Message sent!"


@app.route('/aboutuser/<int:id>/update', methods=['POST', 'GET'])
@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    dictionary = Localization.return_dictionary(session['user_lang'])
    if request.method == "POST":

        name = request.form['productname']
        price = request.form['productprice']
        category = request.form['category']
        description = request.form['subject']
        file = request.files['filename']
        numberid = random.randint(100000, 999999)
        print(numberid)

        if file.filename == '':
            flash("No image selected for upload")
            return render_template("addproduct.html", dictionary=dictionary)

        if file and file.filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        product = Products(id=numberid, title=name, price=price, category=category, description=description,
                           photo=file.filename)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/', dictionary=dictionary)

        except:
            print("При добавлении товара произошла ошибка")

            return "При добавлении товара произошла ошибка"

    return render_template("addproduct.html", dictionary=dictionary)


@app.route('/signup')
def signup_open():
    dictionary = Localization.return_dictionary(session['user_lang'])
    return render_template("signup.html", dictionary=dictionary)


@app.route('/aboutuser')
def aboutuser():
    dictionary = Localization.return_dictionary(session['user_lang'])
    return render_template("aboutuser.html", dictionary=dictionary)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    dictionary = Localization.return_dictionary(session['user_lang'])
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if email and password:

            user = Users.query.filter_by(email=email).first()

            if user.password == password:
                session['user'] = user.name
                session['user_email'] = user.email
                session['user_id'] = user.id
                print(session['user'])
                print(session['user_email'])
                print(session['user_id'])
                flash('You were successfully logged in')

                render_template("index.html", dictionary=dictionary)
            else:
                flash('Login or password is not correct')
        else:
            flash('Login or password is not given')

    return render_template("signup.html", dictionary=dictionary)


@app.route('/register', methods=['POST', 'GET'])
def register():
    dictionary = Localization.return_dictionary(session['user_lang'])
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']

        if request.form['password'] == request.form['passwordRepeat']:
            password = request.form['password']
            numberid = random.randint(10000, 99999)
            date = datetime.utcnow()
            print(date)
            user = Users(id=numberid, name=name, email=email, password=password, updatetime=date)

        try:
            db.session.add(user)
            db.session.commit()
            sending_email(name, email)
            return redirect('/signup', dictionary=dictionary)

        except:

            print("При регистрации произошла ошибка")

            return "При регистрации произошла ошибка"

    return render_template("register.html", dictionary=dictionary)


def sending_email(name, email):
    msg = Message('Hello from the other side!', sender='taide.catering@gmail.com', recipients=[email])
    msg.body = "Hey, " + name + "! You are successfully registered on Simple Catering."
    mail.send(msg)
    return "Message sent!"


@app.route('/logout')
def logout():
    dictionary = Localization.return_dictionary(session['user_lang'])
    session.clear()
    session['user'] = "0"
    session['user_email'] = "0"
    session['user_cart'] = ""


    print("gjkexblkjc")

    return redirect(url_for('menus'), dictionary=dictionary)




if __name__ == '__main__':
    app.run()
