from flask import render_template, session, request, redirect, url_for, flash

from shop.__init__ import app, db, bcrypt
from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import User
from shop.products.models import Addproduct, Brand, Category


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Сначала войдите в систему', 'danger')

        return redirect(url_for('login'))

    products = Addproduct.query.all()

    return render_template('admin/index.html', title="Панель управления", products=products)


@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Сначала войдите в систему', 'danger')

        return redirect(url_for('login'))

    brands = Brand.query.order_by(Brand.id.desc()).all()

    return render_template('admin/brand.html', title="Бренды", brands=brands)


@app.route('/categories')
def categories():
    if 'email' not in session:
        flash(f'Сначала войдите в систему', 'danger')

        return redirect(url_for('login'))

    categories = Category.query.order_by(Category.id.desc()).all()

    return render_template('admin/brand.html', title="Категории", categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'{form.name.data}, зарегистрирован в системе', 'success')

        return redirect(url_for('login'))

    return render_template('admin/register.html', form=form, title="Регистрация")


@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'{user.name}, вошел в систему', 'success')

            return redirect(url_for('admin'))
        else:
            flash('Пароль неверный', 'danger')

            return redirect(url_for('login'))

    return render_template('admin/login.html', form=form, title="Вход")
