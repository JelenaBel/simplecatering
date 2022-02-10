from flask import Flask,  render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import random
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://ferotzlrxzwgkq:fa5fb5eaf6d79e3d2f2899aefd971cdf4c780eb6812bacd5cd6120577afcc582@ec2-54-220-53-223.eu-west-1.compute.amazonaws.com:5432/dbg4nb233p895s'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'zybrzubryachestiy'
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Products(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), primary_key=False)
    price = db.Column(db.Integer )
    category = db.Column(db.String(100), primary_key=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200))

    def __repr__(self):
        return f"<products {self.id}>"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), primary_key=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<users {self.id}>"


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

            return redirect('/signup')

        except:

            print("При регистрации произошла ошибка")

            return "При регистрации произошла ошибка"

    return render_template("register.html")


@app.route('/logout')
def logout():
    session['user'] = "0"
    session['user_email'] = "0"

    print("gjkexblkjc")


    return redirect(url_for('menus'))



if __name__ == '__main__':
    app.run()
