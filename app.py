from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
SECRET_KEY = '64b99e7cedfdbd0318ba6c19de17ace22514b2a7f63bd0c4de91b946fa69d3eafb4b5fe3444445729ee4'

app.config.update(
    DEBUG=False,
    SECRET_KEY=SECRET_KEY,
    SQLALCHEMY_DATABASE_URI='sqlite:///sushi-delivery.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

meal_orders_association = db.Table('meals_orders',
                                   db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')),
                                   db.Column('order_id', db.Integer, db.ForeignKey('orders.id'))
                                   )


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    orders = db.relationship("Order", back_populates="users")


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    orders = db.relationship("Order", secondary=meal_orders_association, back_populates="meals")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    meals = db.relationship("Meal", back_populates="categories")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(25), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    ordered_meals = db.relationship("Meal", secondary=meal_orders_association, back_populates="orders")


@app.route("/")
@app.route("/index")
def index():
    return render_template("main.html")


@app.route("/cart/")
def cart_view():
    return render_template("cart.html")


@app.route("/account/")
def account_view():
    return render_template("account.html")


@app.route("/auth/")
def auth_view():
    return render_template("auth.html")


@app.route("/register/")
def register_view():
    return render_template("register.html")


@app.route("/logout/")
def logout_view():
    return render_template("login.html")


@app.route("/ordered/")
def ordered_view():
    return render_template("ordered.html")


@app.errorhandler(404)
def render_not_found(error):
    return f'<center><h1>Ничего не нашлось!</h1><img src="/static/Ошибка 404.png" alt="Фото потерялось..."></center>'


@app.errorhandler(500)
def server_error(error):
    return f'<center><h1>Вы сломали сервер! Ошибка {error}</h1></center>'


if __name__ == '__main__':
    app.run(debug=True)
