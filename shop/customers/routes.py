import os
import secrets

from flask import redirect, session, render_template, url_for, flash, request, current_app

from shop.__init__ import db, app, photos, search
from shop.products.forms import Addproducts
from shop.products.models import Brand, Category, Addproduct
from shop.customers.forms import CustomerRegisterForm


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    # if form.validate_on_submit():
    #     hash_password = bcrypt.generate_password_hash(form.password.data)
    #     register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
    #     db.session.add(register)
    #     flash(f'Welcome {form.name.data} Thank you for registering', 'success')
    #     db.session.commit()
    #     return redirect(url_for('login'))
    return render_template('customer/register.html', form=form)
