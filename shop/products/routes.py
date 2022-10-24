import os
import secrets

from flask import redirect, render_template, url_for, flash, request, current_app, session
from shop.__init__ import db, app, photos, search
from shop.products.forms import Addproducts
from shop.products.models import Brand, Category, Addproduct


def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()

    return brands


def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()

    return categories


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()). \
        paginate(page=page, per_page=8)

    return render_template('products/index.html', title="Главная", products=products,
                           brands=brands(), categories=categories())


@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name', 'description'], limit=6)
    return render_template('products/result.html', products=products, brands=brands(), categories=categories())


@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)

    return render_template('products/single_page.html', title=product.name, product=product,
                           brands=brands(), categories=categories())


@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)

    return render_template('products/index.html', title="Главная", brand=brand, brands=brands(),
                           categories=categories(), get_brand=get_brand)


@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_category = Category.query.filter_by(id=id).first_or_404()
    category = Addproduct.query.filter_by(category=get_category).paginate(page=page, per_page=8)

    return render_template('products/index.html', title="Главная", category=category, categories=categories(),
                           brands=brands(), get_category=get_category)


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'Бренд "{getbrand}" был добавлен', 'success')
        db.session.commit()

        return redirect(url_for('brands'))

    return render_template('products/addbrand.html', title="Добавить товар", brands='brands')


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        flash(f'Бренд "{updatebrand.name}" изменен на "{brand}"', 'success')
        updatebrand.name = brand
        db.session.query(Brand).filter_by(id=id).update({'name': updatebrand.name})
        db.session.commit()

        return redirect(url_for('brands'))

    return render_template('products/updatebrand.html', title='Изменить бренд', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        try:
            db.session.query(Brand).filter_by(id=id).delete()
            db.session.commit()
            flash(f'Бренд "{brand.name}" удален', 'success')

            return redirect(url_for('brands'))
        except Exception as e:
            print(e)
            flash(f'Бренд "{brand.name}" не удален', 'warning')

            return redirect(url_for('brands'))


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'Категория "{getcategory}" была добавлена', 'success')
        db.session.commit()

        return redirect(url_for('categories'))

    return render_template('products/addbrand.html', title='Добавить категорию')


@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        flash(f'Категория "{updatecategory.name}" изменена на "{category}"', 'success')
        updatecategory.name = category
        db.session.query(Category).filter_by(id=id).update({'name': updatecategory.name})
        db.session.commit()

        return redirect(url_for('categories'))

    return render_template('products/updatebrand.html', title='Изменить категорию', updatecategory=updatecategory)


@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        try:
            db.session.query(Category).filter_by(id=id).delete()
            db.session.commit()
            flash(f'Категория "{category.name}" удалена', 'success')

            return redirect(url_for('categories'))
        except Exception as e:
            print(e)
            flash(f'Категория "{category.name}" не удалена', 'warning')

            return redirect(url_for('categories'))


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        color = form.color.data
        description = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, color=color,
                            description=description, category_id=category, brand_id=brand,
                            image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'Товар "{name}" добавлен', 'success')
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', form=form, title="Добавить товар",
                           brands=brands, categories=categories)


@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.color = form.color.data
        product.description = form.description.data
        db.session.query(Addproduct).filter_by(id=id).\
            update({'name': product.name,
                    'price': product.price,
                    'discount': product.discount,
                    'brand_id': product.brand_id,
                    'category_id': product.category_id,
                    'stock': product.stock,
                    'color': product.color,
                    'description': product.description})
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
                db.session.query(Addproduct).filter_by(id=id).update({'image_1': product.image_1})
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
                db.session.query(Addproduct).filter_by(id=id).update({'image_1': product.image_1})
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
                db.session.query(Addproduct).filter_by(id=id).update({'image_2': product.image_2})
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
                db.session.query(Addproduct).filter_by(id=id).update({'image_2': product.image_2})
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
                db.session.query(Addproduct).filter_by(id=id).update({'image_3': product.image_3})
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
                db.session.query(Addproduct).filter_by(id=id).update({'image_3': product.image_3})
        flash(f'Товар "{product.name}" обновлен', 'success')
        db.session.commit()

        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.color
    form.description.data = product.description

    return render_template('products/updateproduct.html', form=form, title='Обновить продукт', product=product,
                           brands=brands, categories=categories)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
            db.session.query(Addproduct).filter_by(id=id).delete()
            db.session.commit()
            flash(f'Товар "{product.name}" удален', 'success')

            return redirect(url_for('admin'))
        except Exception as e:
            print(e)
            flash(f'Товар "{product.name}" не удален', 'warning')

            return redirect(url_for('admin'))
