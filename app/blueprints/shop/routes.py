from app import db
from .import bp as shop
from flask import render_template, redirect, url_for, request, flash, session, jsonify, current_app as app
from .models import Product, Category, Cart
from app.blueprints.authentication.models import User
from flask_login import login_required, current_user
from datetime import datetime as dt

@shop.route('/', methods=['GET'])
@login_required
def index():
    context = {
        'products': Product.query.all()
    }
    return render_template('shop/index.html', **context)

@shop.route('/product', methods=['GET'])
def single():
    product_id = request.args.get('id')
    context = {
        'p': Product.query.get(product_id)
    }
    return render_template('shop/single.html', **context)

@shop.route('/category', methods=['GET'])
def category():
    category_id = request.args.get('id')
    print(request.args)
    context = {
        'category': Category.query.get(category_id),
        'products': Product.query.filter_by(category_id=category_id).all()
    }
    return render_template('shop/index.html', **context)

@shop.route('/cart', methods=['GET'])
def show_cart():
    context = {
        'products': [Product.query.get(i.product_id) for i in Cart.query.filter_by(user_id=current_user.id).all()]
    }
    return render_template('shop/cart.html', **context)

@shop.route('/cart/remove', methods=['GET'])
def delete_from_cart():
    product_id = request.args.get('id')
    [db.session.delete(i) for i in Cart.query.filter_by(product_id=product_id).all()]
    db.session.commit()
    flash(f'{Product.query.get(product_id).name} removed successfully.', 'warning')
    return redirect(url_for('shop.show_cart'))

@shop.route('/cart/add', methods=['GET'])
def add_to_cart():
    user = User.query.get(current_user.id)
    if not user.is_customer:
        user.is_customer = True
        db.session.commit()
    product_id = request.args.get('product_id')
    data = {
        'user_id': user.id,
        'product_id': product_id,
    }
    cart = Cart()
    cart.from_dict(data)
    cart.save()
    flash(f'{Product.query.get(product_id).name} added successfully', 'success')
    return redirect(request.referrer)