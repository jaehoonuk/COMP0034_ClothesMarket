# Author: Jaehoon Lim

from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, unique=True)
    fullName = db.Column(db.Text)
    password = db.Column(db.Text)
    shippingInfo = db.relationship('ShippingInfo', backref='user', uselist=False)
    itemsForSale = db.relationship('Item', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.userId)

class Item(db.Model):
    __tablename__ = 'item'

    itemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    manufacturer = db.Column(db.Text)
    productName = db.Column(db.Text)
    category = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    estimatedPrice = db.Column(db.Integer)
    imageUrl = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Item {}>'.format(self.itemId)


class ShippingInfo(db.Model):
    __tablename__ = 'shippingInfo'

    shippingId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    streetAddress = db.Column(db.Text)
    houseNumber = db.Column(db.Text)
    zipCode = db.Column(db.Text)
    city = db.Column(db.Text)
    country = db.Column(db.Text)
    order = db.relationship('Order', backref='shippingInfo', uselist=False)

    def __repr__(self):
        return '<ShippingInfo {}>'.format(self.shippingId)

order_item_table = db.Table('association', db.Model.metadata,
    db.Column('orderId', db.Integer, db.ForeignKey('order.orderId')),
    db.Column('itemId', db.Integer, db.ForeignKey('item.itemId'))
)

class Order(db.Model):
    __tablename__ = 'order'

    orderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    items = db.relationship("Item", secondary=order_item_table)
    totalPrice = db.Column(db.Integer)
    shippingId = db.Column(db.Integer, db.ForeignKey('shippingInfo.shippingId'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Order {}>'.format(self.orderId)