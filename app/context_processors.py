from .blueprints.shop.models import Category, Cart, Product
from flask_login import current_user
from flask import current_app as app, session

@app.context_processor
def get_product_categories():
    return { 'product_categories': [c for c in Category.query.order_by(Category.name).all()] }

@app.context_processor
def get_subtotal():
    if current_user.is_anonymous:
        return { 'subtotal': 0} 
    else:
        return { 'subtotal': round(sum([Product.query.get(i.product_id).price for i in Cart.query.filter_by(user_id=current_user.get_id()).all()]), 2) }

@app.context_processor
def get_grandtotal():
    if current_user.is_anonymous:
        return { 'grandtotal': 0}
    else:
        return { 'grandtotal': round(sum([Product.query.get(i.product_id).price+Product.query.get(i.product_id).tax for i in Cart.query.filter_by(user_id=current_user.get_id()).all()]), 2) }

@app.context_processor
def get_cart_items():
    if current_user.is_anonymous:
        return { 'cart_item': []}
    else:
        return { 'cart_items': Cart.query.filter_by(user_id=current_user.get_id()).all() }

@app.context_processor
def get_display_cart():
    cart_list = {}
    if current_user.is_anonymous:
        session['display_cart'] = cart_list
        return { 'display_cart': cart_list.values() }
    else:
        for i in Cart.query.filter_by(user_id=current_user.id).all():
            product = Product.query.get(i.product_id)
            if i.product_id not in cart_list.keys():
                cart_list[product.id] = {
                    'id': i.id,
                    'product_id': product.id,
                    'quantity': 1,
                    'name': product.name,
                    'image': product.image,
                    'description': product.description,
                    'price': product.price
                }
            else: 
                cart_list[product.id]['quantity'] += 1
        session['display_cart'] = cart_list
        return { 'display_cart': cart_list.values() }