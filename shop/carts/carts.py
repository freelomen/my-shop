import os
import secrets

from flask import redirect, session, render_template, url_for, flash, request, current_app

from shop.__init__ import db, app, photos
from shop.products.forms import Addproducts
from shop.products.models import Brand, Category, Addproduct


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if product_id and quantity and colors and request.method == "POST":
            DictItems = {product_id: {'name': product.name, 'price':float(product.price), 'discount': product.discount,
                                      'color': colors, 'quantity': quantity, 'image': product.image_1,
                                      'colors': product.color}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("Этот продукт уже есть в корзине")
        #             # for key, item in session['Shoppingcart'].items():
        #             #     if int(key) == int(product_id):
        #             #         session.modified = True
        #             #         item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
