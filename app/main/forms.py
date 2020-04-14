# Author: Jinho Lee

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed

class SignupForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    fullName = StringField('fullName', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirmPassword', message='Passwords must match.')])
    confirmPassword = PasswordField('confirmPassword')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class SellForm(FlaskForm):
    productName = StringField('productName', validators=[DataRequired()])
    manufacturer = StringField('manufacturer', validators=[DataRequired()])
    imageUrl = FileField('imageUrl', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'gif', 'png'], 'Image files only!')])
    category = StringField('category', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    estimatedPrice = IntegerField('estimatedPrice', validators=[DataRequired()])

class ShippingForm(FlaskForm):
    streetAddress = StringField('streetAddress', validators=[DataRequired()])
    houseNumber = StringField('houseNumber', validators=[DataRequired()])
    zipCode = StringField('zipCode', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])

class CheckoutForm(FlaskForm):
    stripeToken = StringField('stripeToken')