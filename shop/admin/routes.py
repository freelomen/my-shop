from flask import render_template, request, redirect, url_for, flash
from shop.admin.forms import RegistrationForm
from shop.__init__ import app, db, bcrypt
from shop.admin.models import User


@app.route('/home')
def home():
    return render_template('admin/index.html', title="Admin page")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome, {form.name.data}! Thanks for registering', 'success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Registration page")
