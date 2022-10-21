import os
import secrets

from flask import redirect, session, render_template, url_for, flash, request, current_app

from shop.__init__ import db, app, photos
from shop.products.forms import Addproducts
from shop.products.models import Brand, Category, Addproduct


def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).\
        paginate(page=page, per_page=8)

    return render_template('products/index.html', title="Home page", products=products,
                           brands=brands(), categories=categories())


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

    return render_template('products/index.html', title="Home page", brand=brand, brands=brands(),
                           categories=categories(), get_brand=get_brand)


@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_category = Category.query.filter_by(id=id).first_or_404()
    category = Addproduct.query.filter_by(category=get_category).paginate(page=page, per_page=8)

    return render_template('products/index.html', title="Home page", category=category, categories=categories(),
                           brands=brands(), get_category=get_category)


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

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
        flash(f'The product {name} was added in database', 'success')
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', form=form, title="Add product page",
                           brands=brands, categories=categories)


@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
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

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        flash('The product was updated', 'success')
        db.session.commit()

        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.color
    form.description.data = product.description

    return render_template('products/updateproduct.html', form=form, title='Update Product', product=product,
                           brands=brands, categories=categories)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))

            db.session.delete(product)
            db.session.commit()

            flash(f'The product {product.name} was delete from your record', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            print(e)

            flash(f'Can not delete the product', 'warning')
            return redirect(url_for('admin'))


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database', 'success')
        db.session.commit()

        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands='brands')


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')

    if request.method == "POST":
        updatebrand.name = brand
        db.session.commit()
        flash(f'The brand {updatebrand.name} was changed to {brand}', 'success')
        return redirect(url_for('brands'))

    return render_template('products/updatebrand.html', title='Update brand', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        try:
            db.session.delete(brand)
            db.session.commit()
            flash(f'The brand {brand.name} was deleted', 'success')
            return redirect(url_for('brands'))
        except:
            flash(f'The brand {brand.name} can not be deleted', 'warning')
            return redirect(url_for('brands'))


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'The category {getcategory} was added to your database', 'success')
        db.session.commit()

        return redirect(url_for('addcategory'))

    return render_template('products/addbrand.html')


@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')

    if request.method == "POST":
        flash(f'The category {updatecategory.name} was changed to {category}', 'success')
        updatecategory.name = category
        db.session.commit()
        return redirect(url_for('categories'))

    return render_template('products/updatebrand.html', title='Update category', updatecategory=updatecategory)


@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    if 'email' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))

    category = Category.query.get_or_404(id)

    if request.method == "POST":
        try:
            db.session.delete(category)
            db.session.commit()
            flash(f'The brand {category.name} was deleted', 'success')
            return redirect(url_for('categories'))
        except:
            flash(f'The brand {category.name} can not be deleted', 'warning')
            return redirect(url_for('categories'))
