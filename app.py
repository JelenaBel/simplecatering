from flask import Flask,  render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import random
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://kejlhjougftxhg:b84959d4f70d021ae06b0b6e678d62db38ff093ef430c60c0265a5b187d6377f@ec2-52-211-158-144.eu-west-1.compute.amazonaws.com:5432/d4kp34r5liihrn'

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


class Products(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), primary_key=False)
    price = db.Column(db.Integer )
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
    publicity = db.Column(db.String(100), default = "No")
    replied = db.Column(db.String(100), default = "No")


    def __repr__(self):
        return f"<feedback {self.id}>"

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer(), db.ForeignKey('feedback.id'))
    subject = db.Column(db.VARCHAR(200), nullable=False)
    message = db.Column(db.VARCHAR(1000), nullable=False)
    updatetime = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<reply {self.id}>"

db.create_all()


@app.route('/')
def indexpage():  # put application's code here
    return render_template("index.html")


@app.route('/admin')
def admin():  # put application's code here
    return render_template("adminmain.html")


@app.route('/menus')
def menus():  # put application's code here
    return render_template("menus.html")


@app.route('/shop')
def shopcreate():
    products = Products.query.all();

    return render_template("create.html", products=products)


@app.route('/about')
def about():  # put application's code here
    return render_template("about.html")



@app.route('/contact')
def contacts():  # put application's code here
    return render_template("contacts.html")


@app.route('/contact', methods=['POST', 'GET'])
def feedback():
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

    return render_template("contacts.html")


def sending_email_feedbackform(name, email):
    msg = Message('You letter to Simple Catering.', sender='taide.catering@gmail.com', recipients=[email])
    msg.body = "Hey, "+name+"! Thank you for contacting Simple Catering! We will answer for your letter as soon as possible."
    mail.send(msg)
    return "Message sent!"


@app.route('/orders')
def admin_orders():  # put application's code here
    return render_template("orders.html")


@app.route('/productsadmin')
def productsadmin():
    products = Products.query.all();

    return render_template("productsadmin.html", products=products)


@app.route('/productsadmin/<int:id>/delete')
def deleteproduct(id):
    product = Products.query.get_or_404(id);

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect ("/productsadmin")
    except:
        return ("An error occurred while deleting the product")

        return redirect  ("/productsadmin")


@app.route('/productsadmin/<int:id>/update', methods=['POST', 'GET'])
def updateproduct(id):
    product = Products.query.get(id)
    if request.method == "POST":
        print ("collect info for update")
        product.id = id
        product.title = request.form['productname']
        product.price = request.form['productprice']
        product.category = request.form['category']
        product.description = request.form['subject']
        file = request.files['filename']


        if file.filename!= '':
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
        return render_template("productupdate.html", product=product)


@app.route('/customersadmin/<int:id>/delete')
def deletecustomer(id):
    user = Users.query.get_or_404(id);

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect ("/customersadmin")
    except:
        return ("An error occurred while deleting the product")

        return redirect  ("/customersadmin")


@app.route('/customersadmin/<int:id>/update', methods=['POST', 'GET'])
def updateuser(id):
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
        return render_template("customersadminupdate.html", user=user)


@app.route('/aboutuser/<int:id>/update', methods=['POST', 'GET'])


def updateuseritself(id):
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
        return render_template("customersadminupdate.html", user=user)


@app.route('/customersadmin')
def customerssadmin():
    users = Users.query.all();

    return render_template("customersadmin.html", users=users)


@app.route('/feedbacksadmin')
def feedbacksadmin():
    feedback = Feedback.query.all();

    return render_template("feedbacksadmin.html", feedback=feedback)


@app.route('/feedbacksadmin/<int:id>/delete')
def deletefeedback(id):
    feedback = Feedback.query.get_or_404(id);

    try:
        db.session.delete(feedback)
        db.session.commit()
        return redirect ("/feedbacksadmin")
    except:
        return ("An error occurred while deleting the feedback")

        return redirect  ("/feedbacksadmin")


@app.route('/feedbacksadmin/<int:id>/reply', methods=['POST', 'GET'])
def reply_feedback(id):
    feedback = Feedback.query.get(id)
    customeremail = feedback.email
    if request.method == "POST":
        idreply = random.randint(100000, 999999)
        feedback_id = id
        subject = request.form['subject']
        message = request.form['message']


        try:
            sending_reply_customerfeedback(customeremail, subject, message)
            reply = Reply(id=idreply, feedback_id=feedback_id, subject=subject, message=message)
            db.session.commit(reply)
            return redirect('/feedbacksadmin')

        except:
            print("При редактировании account произошла ошибка")

            return "При редактировании account произошла ошибка"

    else:
        return render_template("feedbackadminreply.html", feedback=feedback)


def sending_reply_customerfeedback(email, subject,  message):
    msg = Message(subject, sender='taide.catering@gmail.com', recipients=[email])
    msg.body = message
    mail.send(msg)
    return "Message sent!"

@app.route('/aboutuser/<int:id>/update', methods=['POST', 'GET'])



@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if request.method == "POST":

        name = request.form['productname']
        price = request.form['productprice']
        category = request.form['category']
        description = request.form['subject']
        file = request.files['filename']
        numberid= random.randint(100000, 999999)
        print(numberid)

        if file.filename == '':
            flash("No image selected for upload")
            return render_template("addproduct.html")

        if file and file.filename:

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        product = Products(id=numberid, title=name, price=price, category=category, description=description, photo=file.filename)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')

        except:
            print("При добавлении товара произошла ошибка")

            return "При добавлении товара произошла ошибка"

    return render_template("addproduct.html")


@app.route('/signup')
def signup_open():
    return render_template("signup.html")


@app.route('/aboutuser')
def aboutuser():
    return render_template("aboutuser.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if email and password:

            user = Users.query.filter_by(email=email).first()
            print(user.name)
            print(user.email)
            if user.password == password:
                session['user'] = user.name
                session['user_email'] = user.email
                session['user_id'] = user.id
                print(session['user'])
                print(session['user_email'])
                print(session['user_id'])
                flash('You were successfully logged in')

                render_template("index.html")
            else:
                flash('Login or password is not correct')
        else:
            flash('Login or password is not given')

    return render_template("signup.html")



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']

        if request.form['password'] == request.form['passwordRepeat']:
            password = request.form['password']
            numberid = random.randint(10000, 99999)
            print(numberid)
            user = Users(id=numberid, name=name, email=email, password=password)

        try:
            db.session.add(user)
            db.session.commit()
            sending_email(name, email)
            return redirect('/signup')

        except:

            print("При регистрации произошла ошибка")

            return "При регистрации произошла ошибка"

    return render_template("register.html")


def sending_email(name, email):
    msg = Message('Hello from the other side!', sender='obyelousova@gmail.com', recipients=[email])
    msg.body = "Hey,"+name+" you are successfully registered on Simple Catering."
    mail.send(msg)
    return "Message sent!"


@app.route('/logout')
def logout():
    session['user'] = "0"
    session['user_email'] = "0"

    print("gjkexblkjc")


    return redirect(url_for('menus'))



if __name__ == '__main__':
    app.run()
