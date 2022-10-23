from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, TextAreaField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed


class Addproducts(Form):
    name = StringField('Название', [validators.DataRequired()])
    price = FloatField('Стоимость', [validators.DataRequired()])
    discount = IntegerField('Скидка', default=0)
    stock = IntegerField('Количество', [validators.DataRequired()])
    color = StringField('Цвета', [validators.DataRequired()])
    description = TextAreaField('Описание', [validators.DataRequired()])

    image_1 = FileField('Первое изображение', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('Второе изображение', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Третье изображение', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
