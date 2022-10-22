from wtforms import StringField, PasswordField, validators, ValidationError
from flask_wtf import FlaskForm
from shop.admin.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Имя', [validators.Length(min=4, max=25)])
    username = StringField('Никнейм', [validators.Length(min=4, max=25)])
    email = StringField('Электронный адрес', [
        validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Новый пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароль должны совпадать')])
    confirm = PasswordField('Повторите пароль')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Никнейм уже занят')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Электронный адрес уже занят')


class LoginForm(FlaskForm):
    email = StringField('Электронный адрес', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Пароль', [validators.DataRequired()])
