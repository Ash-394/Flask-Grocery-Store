# models.py
from sqlalchemy.sql import func
from . import db
from flask_login import UserMixin
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)

    def __init__(self, user_id, total_amount):
        self.user_id = user_id
        self.total_amount = total_amount

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacture_date = db.Column(db.String(10), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    section = db.relationship('Section', backref=db.backref('products', lazy=True))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'user'

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('cart', uselist=False))

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    cart = db.relationship('Cart', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

