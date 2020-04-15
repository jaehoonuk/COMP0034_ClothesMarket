# Author: 15061865

from flask import render_template, flash, session, redirect, request, url_for

from app import db, bcrypt, photos
from app.main import bp
from app.main.forms import SignupForm, LoginForm, SellForm, ShippingForm, CheckoutForm
from app.main.basket import Basket
from app.models import User, Item, ShippingInfo, Order

from sqlalchemy import func, or_

import stripe

import uuid

@bp.route('/')
def index():
    itemsForSale = Item.query.join(User).order_by(Item.date_posted.desc()).all()
    return render_template('index.html', itemsForSale=itemsForSale)

@bp.route('/store')
@bp.route('/store/<category>')
def store(category=None):
    page = request.args.get('p', 1, type=int)
    itemsForSale = Item.query.join(User).order_by(Item.date_posted.desc()).paginate(page=page, per_page=8)

    if category:
        itemsForSale = Item.query.filter(func.lower(Item.category) == func.lower(category)).join(User).order_by(Item.date_posted.desc()).paginate(page=page, per_page=8)

    return render_template('store.html', itemsForSale=itemsForSale, category=category)

@bp.route('/item/<id>')
def item(id):
    item = Item.query.filter_by(itemId=id).join(User).first()
    if(item):
        return render_template('item.html', item=item)
    else:
        flash(f'Invalid item id.', 'error')
        return redirect(request.args.get('next') or '/')


@bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if session.get('logged_in'):
        flash(f'You are already logged in.', 'warning')
        return redirect(request.args.get('next') or '/')

    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(f'The email address you entered already exists. Please try again.', 'error')
            return redirect('/signup')

        password_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(fullName=form.fullName.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Thank you for registering! You can now login.', 'success')
        return redirect('/login')
    else:
        if form.errors:
            error_msg = list(form.errors.values())[0][0]
            flash(f'{error_msg} Please try again.', 'error')

    return render_template('signup.html', form=form)

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('logged_in'):
        flash(f'You are already logged in.', 'warning')
        return redirect(request.args.get('next') or '/')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.userId
            session['logged_in'] = True
            flash(f'Welcome {user.fullName}! You are now logged in.', 'success')
            return redirect(request.args.get('next') or '/')
        else:
            flash(f'Invalid email or password! Please try again.', 'error')

    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    session.pop('user_id')
    session.pop('logged_in')
    flash(f'You have been logged out!', 'success')
    return redirect(request.args.get('next') or '/')

@bp.route('/sell', methods=['POST', 'GET'])
def sell():
    if not session.get('logged_in'):
        flash(f'Please login to continue.', 'warning')
        return redirect('/login')

    form = SellForm()
    if form.validate_on_submit():
        fileName = photos.save(request.files.get('imageUrl'), None, str(uuid.uuid4()) + ".")
        imageUrl = '/static/images/uploads/' + fileName
        item = Item(userId=int(session['user_id']), productName=form.productName.data, manufacturer=form.manufacturer.data, quantity=form.quantity.data, category=form.category.data, price=form.price.data, estimatedPrice=form.estimatedPrice.data, imageUrl=imageUrl)
        db.session.add(item)
        db.session.commit()
        flash(f'You item has been posted for sale!', 'success')
        return redirect('/item/' + str(item.itemId))
    else:
        if form.errors:
            error_msg = list(form.errors.values())[0][0]
            flash(f'{error_msg} Please try again.', 'error')

    return render_template('sell.html', form=form)

@bp.route('/account', methods=['POST', 'GET'])
def account():
    if not session.get('logged_in'):
        flash(f'Please login to continue.', 'warning')
        return redirect('/login')

    shippingForm = ShippingForm()
    shippingInfo = ShippingInfo.query.filter_by(userId=int(session['user_id'])).first()

    if shippingForm.validate_on_submit():
        if shippingInfo:
            shippingInfo.streetAddress = shippingForm.streetAddress.data
            shippingInfo.houseNumber = shippingForm.houseNumber.data
            shippingInfo.zipCode = shippingForm.zipCode.data
            shippingInfo.city = shippingForm.city.data
            shippingInfo.country = shippingForm.country.data
            db.session.commit()
        else:
            shippingInfo = ShippingInfo(userId=int(session['user_id']), streetAddress=shippingForm.streetAddress.data, houseNumber=shippingForm.houseNumber.data, zipCode=shippingForm.zipCode.data, country=shippingForm.country.data, city=shippingForm.city.data)
            db.session.add(shippingInfo)
            db.session.commit()

        flash(f'You shipping information has been updated!', 'success')
        return redirect(request.args.get('next') or request.referrer or url_for(default))
    else:
        if shippingForm.errors:
            error_msg = list(shippingForm.errors.values())[0][0]
            flash(f'{error_msg} Please try again.', 'error')

    itemsForSale = Item.query.filter_by(userId=int(session['user_id'])).order_by(Item.date_posted.desc()).all()

    orders = Order.query.filter_by(userId=int(session['user_id'])).order_by(Order.date.desc()).all()

    return render_template('account.html', shippingForm=shippingForm, shippingInfo=shippingInfo, itemsForSale=itemsForSale, orders=orders)

@bp.route('/basket')
def basket():
    if session.get('basket'):
        basket = Basket(session['basket'])
    else:
        basket = None
    return render_template('basket.html', basket=basket)


@bp.route('/buyNow/<itemId>')
def buyNow(itemId):
    if not session.get('logged_in'):
        flash(f'Please login to continue.', 'warning')
        return redirect('/login')

    user = User.query.filter_by(userId=int(session['user_id'])).first()

    shippingForm = ShippingForm()
    checkoutForm = CheckoutForm()
    shippingInfo = ShippingInfo.query.filter_by(userId=int(session['user_id'])).first()
    item = Item.query.filter_by(itemId=itemId).first();
    basket = Basket()
    basket.addItem(item)
    serializedBasket = basket.serialize()
    session['basket'] = serializedBasket

    return render_template('checkout.html', basket=basket, shippingInfo=shippingInfo, shippingForm=shippingForm, checkoutForm=checkoutForm, user=user)

@bp.route('/addToCart/<itemId>')
def addToCart(itemId):
    item = Item.query.filter_by(itemId=itemId).first();

    if not session.get('basket'):
        basket = Basket()
        basket.addItem(item)
        serializedBasket = basket.serialize()
        session['basket'] = serializedBasket
    else:
        basket = Basket(session['basket'])
        basket.addItem(item)
        serializedBasket = basket.serialize()
        session['basket'] = serializedBasket
        
    flash(f'The item has been added to your basket!', 'success')
    return redirect(request.args.get('next') or request.referrer or url_for(default))

@bp.route('/removeFromCart/<itemId>')
def removeFromCart(itemId):
    if not session.get('basket'):
        return redirect(request.args.get('next') or request.referrer or url_for(default))
    else:
        basket = Basket(session['basket'])
        basket.removeItem(itemId)
        serializedBasket = basket.serialize()
        session['basket'] = serializedBasket
        flash(f'The item has been removed from your basket!', 'success')
        return redirect(request.args.get('next') or request.referrer or url_for(default))

@bp.route('/checkout', methods=['POST', 'GET'])
def checkout():
    if not session.get('logged_in'):
        flash(f'Please login to continue.', 'warning')
        return redirect('/login')

    if not session.get('basket'):
        flash(f'Your basket is empty!', 'error')
        return redirect(request.args.get('next') or request.referrer or url_for(default))

    user = User.query.filter_by(userId=int(session['user_id'])).first()
    basket = Basket(session['basket'])
    shippingForm = ShippingForm()
    checkoutForm = CheckoutForm()
    shippingInfo = ShippingInfo.query.filter_by(userId=int(session['user_id'])).first()

    if checkoutForm.validate_on_submit():
        # customer = stripe.Customer.create(name=user.fullName, email=user.email)

        order = Order(userId=int(session['user_id']), shippingId=shippingInfo.shippingId, totalPrice=basket.totalPrice)
        for id in basket.items:
            item = Item.query.filter_by(itemId=int(id)).first()
            order.items.append(item)
        db.session.add(order)
        db.session.commit()

        charge = stripe.Charge.create(
            amount=basket.totalPrice*100,
            currency='gbp',
            source=checkoutForm.stripeToken.data,
            description="ClothesMarket Order #" + str(order.orderId),
            receipt_email=user.email
        )

        session.pop('basket')

        flash(f'Your purchase has been submitted!', 'success')
        return redirect('/checkoutcomplete')
    else:
        if checkoutForm.errors:
            print(checkoutForm.errors)
            error_msg = list(checkoutForm.errors.values())[0][0]
            flash(f'{error_msg} Please try again.', 'error')

    return render_template('checkout.html', basket=basket, shippingInfo=shippingInfo, shippingForm=shippingForm, checkoutForm=checkoutForm, user=user)

@bp.route('/checkoutcomplete')
def checkoutcomplete():
    if not session.get('logged_in'):
        flash(f'Please login to continue.', 'warning')
        return redirect('/login')

    return render_template('checkout_complete.html')

@bp.route('/search', methods=['POST', 'GET'])
def search():
    q = request.form['q']
    if q == "":
        flash(f'Please enter a search query.', 'error')
        return redirect('/store')
    results = Item.query.filter(or_(Item.productName.contains(q), Item.manufacturer.like(q), Item.category.like(q))).join(User).order_by(Item.date_posted.desc()).all()
    if not results:
        flash(f'No items matched your search query.', 'warning')
        return redirect('/store')

    return render_template('store.html', itemSearchResults=results, query=q)
