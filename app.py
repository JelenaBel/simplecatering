from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import random
import json
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oyicnymisbwvmr:98f76173ebf06900a7c721a068c6ca7f4bfedd2b61b2cf0c42f36b621bcc3939@ec2-54-228-125-183.eu-west-1.compute.amazonaws.com:5432/d73bs3hispaghi'
# this is new database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()
app.config['SECRET_KEY'] = 'zybrzubryachestiy'
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'taide.catering@gmail.com'
app.config['MAIL_PASSWORD'] = 'icdhffokoinrxzpl'
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
        'signin_smalltext3': "Register here.",
        'main_title1': 'Best catering service for different events',
        'main_title2': 'Only best ingredients from chosen suppliers',
        'main_title3': 'We are offering big choice of ready made menus',
        'main_title': 'ART Catering',
        'main_subtitle1': 'Our services',
        'main_subtitle2': "Menus",
        'main_subtitle3': "Create menu",
        'main_subtitle4': 'Best ingredients',
        'main_subtitle5': "Private events",
        'main_subtitle6': "Corporate events",
        'main_subtitle7': 'Waitress service',
        'main_subtitle8': "Delivery",
        'main_text1': 'We are serving all types of events. Table service, buffet, standing buffet',
        'main_text2': "We are offering wide range of ready made menus with different price",
        'main_text3': "You can create your own menu from our dishes in our create section",
        'main_text4': 'We are using only best ingredients from chosen food suppliers',
        'main_text5': "Weddings, birthdays, parties, children birthdays.",
        'main_text6': "We are serving all type of corporate events from small scale up to 500 persons",
        'main_text7': 'We are offering our waitress service in case you need it',
        'main_text8': "We are serving events in Helsinki, Espoo, Vantaa, Kauniainen, Tuusula, Kerävä ja Järvenpää",

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
        'signin_smalltext3': 'Rekisteröidy täällä.',
        'main_title1': 'Paras catering-palvelu erilaisiin tapahtumiin',
        'main_title2': 'Vain parhaat ainesosat valituilta toimittajilta',
        'main_title3': 'Tarjoamme laajan valikoiman valmiita ruokalistoja',
        'main_title': 'ART Catering',
        'main_subtitle1': 'Palvelumme',
        'main_subtitle2': "Menut",
        'main_subtitle3': "Luo valikko",
        'main_subtitle4': 'Parhaat ainesosat',
        'main_subtitle5': "Yksityiset tapahtumat",
        'main_subtitle6': "Yritystapahtumat",
        'main_subtitle7': 'Tarjoilijapalvelu',
        'main_subtitle8': "Toimitus",
        'main_text1': 'Palvelemme kaikenlaisia tapahtumia. Pöytätarjoilu, buffet, seisova buffet',
        'main_text2': "Tarjoamme laajan valikoiman valmiita menuja eri hinnoilla",
        'main_text3': "Voit luoda oman ruokalistasi meidän luomisosiossa",
        'main_text4': 'Käytämme vain parhaita raaka-aineita valituilta elintarviketoimittajilta',
        'main_text5': "Häät, syntymäpäivät, juhlat, lasten syntymäpäivät.",
        'main_text6': "Palvelemme kaikenlaisia ​​yritystilaisuuksia pienestä 500 hengelle asti",
        'main_text7': 'Tarjoamme tarjoilijapalveluamme, jos tarvitset sitä',
        'main_text8': "Palvelemme tapahtumia Helsingissä, Espoossa, Vantaalla, Kauniaisissa, Tuusulassa, Kerävällä ja Järvenpäällä",

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

    dict = {'en': dictionary_eng, 'fi': dictionary_fi, 'ru': dictionary_ru}

    def return_dictionary(lang):
        if 'user_lang' in session:
            if lang == 'fi':
                dictionary = Localization.dict['fi']
            elif lang == 'en':
                dictionary = Localization.dict['en']
            elif lang == 'ru':
                dictionary = Localization.dict['en']
        else:
            session["user_lang"] = 'en'

            dictionary = Localization.dict['en']

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
    phone = db.Column(db.VARCHAR(30))
    billing_address = db.Column(db.VARCHAR(200))
    billing_city = db.Column(db.VARCHAR(200))
    billing_zip_code = db.Column(db.VARCHAR(200))
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


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.VARCHAR(200), nullable=False)
    payment = db.Column(db.VARCHAR(1000), nullable=False)
    shipping_address = db.Column(db.VARCHAR(200), nullable=False)
    shipping_city = db.Column(db.VARCHAR(200), nullable=False)
    shipping_zip_code = db.Column(db.VARCHAR(200), nullable=False)
    order_date = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<reply {self.id}>"


class OrderItems(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.VARCHAR(200), nullable=False)
    price = db.Column(db.VARCHAR(1000), nullable=False)
    updatetime = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<reply {self.id}>"


class Payments(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    order_total = db.Column(db.Float(), nullable=False)
    order_alv = db.Column(db.Float(), nullable=False)
    payment_status = db.Column(db.VARCHAR(200), nullable=False)
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

    dictionary = Localization.dict['en']

    if 'user_lang' in session:
        if 'user_lang' == "en":
            dictionary = Localization.return_dictionary('en')
        elif 'user_lang' == "fi":
            dictionary = Localization.return_dictionary('fi')
        elif 'user_lang' == "ru":
            dictionary = Localization.return_dictionary('ru')
            return render_template("index.html", dictionary=dictionary)
    else:
        session['user_lang'] = "en"
        dictionary = Localization.return_dictionary('en')
        return render_template("index.html", dictionary=dictionary)

    return render_template("index.html", dictionary=dictionary)


@app.route('/<string:lang>')
def change_lang(lang):
    if 'user_lang' in session:
        if lang == 'fi':
            session['user_lang'] = "fi"
        elif lang == 'en':
            session['user_lang'] = "en"
        elif lang == 'ru':
            session['user_lang'] = "ru"
    else:
        session['user_lang'] = "fi"

    dictionary = Localization.return_dictionary(session['user_lang'])

    return render_template("index.html", dictionary = dictionary)


@app.route('/shop')
def shopcreate():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = Products.query.all();

    return render_template("create.html", products=products, dictionary=dictionary)


@app.route('/menus')
def menus_show():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = db.session.query(Products).filter(Products.category == "Menus").all()
    print (len(products))


    return render_template("menus.html", products=products, dictionary=dictionary)


@app.route('/mains')
def mains_dishes():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = db.session.query(Products).filter(Products.category == "Mains").all()

    return render_template("mains.html", products=products, dictionary=dictionary)


@app.route('/sides')
def sides():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = db.session.query(Products).filter(Products.category == "Sides").all()

    return render_template("sides.html", products=products, dictionary=dictionary)


@app.route('/salads')
def salads():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = db.session.query(Products).filter(Products.category == "Salads").all()

    return render_template("salads.html", products=products, dictionary=dictionary)


@app.route('/bites')
def bites():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = db.session.query(Products).filter(Products.category == "Bites").all()

    return render_template("bites.html", products=products, dictionary=dictionary)


@app.route('/deserts')
def deserts():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = db.session.query(Products).filter(Products.category == "Deserts").all()

    return render_template("deserts.html", products=products, dictionary=dictionary)

@app.route('/shop/<int:id>/readmore')
def readmore(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product = Products.query.get(id)
    return render_template("productpage.html", product=product, dictionary=dictionary)


@app.route('/shop/<int:id>/addtocard')
def addtocard(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product = Products.query.get(id)
    if 'user_id' in session:
        user_id = session['user_id']
    else:
       return render_template("pleaseregister.html", dictionary = dictionary)

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
            new_cart.append(el)

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

    if 'user_id' in session:
        user_id = session['user_id']
    else:
        return render_template("pleaseregister.html", dictionary=dictionary)

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

                product = Products.query.get(product_id)
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


@app.route('/pay', methods=["POST"])
def pay():
    dictionary = Localization.return_dictionary(session['user_lang'])
    order_id = random.randint(100000, 999999)
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
            if i == len(cart) - 1:
                products_in_card[cart[i]] = counter
                break

            if cart[i] == cart[i + 1]:
                counter = counter + 1

            else:
                products_in_card[cart[i]] = counter
                counter = 1

    cart_full = ShoppingCard()
    for key in products_in_card:
        product_id = key
        if product_id != "" and product_id != " ":
            quantity = products_in_card[product_id]
            print(quantity)

            product = Products.query.get(product_id)
            print("Price :")
            print(product.price)

            item_card = Item(product, quantity)
            print(item_card.to_string())
            item_card.get_item_total_price()
            cart_full.additem(item_card)

    total = cart_full.count_card_total()
    alv = total * 0.24
    alv = float('{:.2f}'.format(alv))

    print("pay!!!!\n")
    id = session['user_id']
    name = request.form['firstName']
    lastname = request.form['lastName']
    email = request.form['email']
    phone = request.form['phone']
    billing_address = request.form['address']
    billing_address2 = request.form['address2']
    billing_city = request.form['country']
    billing_zip_code = request.form['zip']
    shipping_address = request.form['shipping_address']
    shipping_address2 = request.form['shipping_address2']
    shipping_city = request.form['shipping_city']
    shipping_zip = request.form['shipping_zip']
    name = name + " " + lastname
    billing_address = billing_address + ', ' + billing_address2
    numberid = session['user_id']
    order_date = datetime.utcnow()

    for key in products_in_card:
        product_id = key
        if product_id != "" and product_id != " ":
            quantity = products_in_card[product_id]
            product = Products.query.get(product_id)
            price = product.price * quantity
            orderitem = OrderItems(order_id=order_id, product_id=product_id, quantity=quantity, price=price,
                                   updatetime=order_date)
            try:
                db.session.add(orderitem)
                db.session.commit()


            except:
                print("При добавлении списка товаров произошла ошибка")

                return "При добавлении списка товаров произошла ошибка"

    print(numberid)
    user: Users = Users.query.get(numberid)
    password = user.password
    user.phone = phone
    user.billing_address=billing_address
    user.billing_city = billing_city
    user.billing_zip_code = billing_zip_code




    order = Orders(order_id=order_id, customer_id=numberid, status="accepted", payment="paid",
                   shipping_address=shipping_address, shipping_city=shipping_city, shipping_zip_code=shipping_zip,
                   order_date=order_date)
    payment = Payments(order_id=order_id, customer_id=numberid, order_total = total, order_alv = alv, payment_status = "Paid", updatetime = order_date )


    try:
        db.session.commit()
        db.session.add(order)
        db.session.add(payment)
        db.session.commit()
        session['user_cart'] = ""
        return redirect('/thankorder')

    except:
        print("При добавлении товара произошла ошибка")

        return "При добавлении товара произошла ошибка"
        render_template("ordermistake.html")

@app.route('/thankorder')
def thankorder():
    dictionary = Localization.return_dictionary(session['user_lang'])
    return render_template("thankorder.html", dictionary=dictionary)


@app.route('/checkout', methods=["POST", "GET"])
def checkout():
    dictionary = Localization.return_dictionary(session['user_lang'])
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        return render_template("pleaseregister.html", dictionary=dictionary)

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

                product = Products.query.get(product_id)
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
            return redirect('/')

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

@app.route('/ordersadmin')
def ordersadmin():
    dictionary = Localization.return_dictionary(session['user_lang'])
    orders = Orders.query.all()

    return render_template("ordersadmin.html", orders=orders, dictionary=dictionary)


@app.route('/paymentsadmin')
def paymentsadmin():
    dictionary = Localization.return_dictionary(session['user_lang'])
    payments = Payments.query.all()
    total = 0
    totalalv= 0
    for el in payments:
        total = total + el.order_total
        totalalv = totalalv+el.order_alv
    return render_template("paymentsadmin.html", payments=payments, total = total, totalalv = totalalv, dictionary=dictionary)

@app.route('/productsadmin')
def productsadmin():
    dictionary = Localization.return_dictionary(session['user_lang'])
    products = Products.query.all();

    return render_template("productsadmin.html", products=products, dictionary=dictionary)


@app.route('/productsadmin/<int:id>/delete')
def deleteproduct(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    product = Products.query.get(id);

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect("/productsadmin")
    except:
        return ("An error occurred while deleting the product")

        return redirect("/productsadmin")


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
            return redirect('/admin')

        except:
            print("При редактировании account произошла ошибка")

            return "При редактировании account произошла ошибка"

    else:
        return render_template("productupdate.html", product=product, dictionary=dictionary)


@app.route('/customersadmin/<int:id>/delete')
def deletecustomer(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    user = Users.query.get(id);

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect("/customersadmin")
    except:
        return ("An error occurred while deleting the product")

        return redirect("/customersadmin")


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
            return redirect('/customersadmin')

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
            return redirect('/aboutuser')

        except:
            print("При редактировании account произошла ошибка")

            return "При редактировании account произошла ошибка"

    else:
        return render_template("customersadminupdate.html", user=user, dictionary=dictionary)


@app.route('/customersadmin')
def customerssadmin():
    dictionary = Localization.return_dictionary(session['user_lang'])
    users = Users.query.all()

    return render_template("customersadmin.html", users=users, dictionary=dictionary)


@app.route('/feedbacksadmin')
def feedbacksadmin():
    dictionary = Localization.return_dictionary(session['user_lang'])
    feedback = Feedback.query.all();

    return render_template("feedbacksadmin.html", feedback=feedback, dictionary=dictionary)


@app.route('/feedbacksadmin/<int:id>/delete')
def deletefeedback(id):
    dictionary = Localization.return_dictionary(session['user_lang'])
    feedback = Feedback.query.get(id);

    try:
        db.session.delete(feedback)
        db.session.commit()
        return redirect("/feedbacksadmin")
    except:
        return ("An error occurred while deleting the feedback")

        return redirect("/feedbacksadmin")


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
            return redirect('/feedbacksadmin')

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
            return redirect('/admin')

        except:
            print("При добавлении товара произошла ошибка")

            return "При добавлении товара произошла ошибка"

    return render_template("addproduct.html", dictionary=dictionary)



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
            return redirect('/signup')

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

    session.clear()
    session['user'] = "0"
    session['user_email'] = "0"
    session['user_cart'] = ""



    print("gjkexblkjc")

    return redirect("/")




if __name__ == '__main__':
    app.run()
