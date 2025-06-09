from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User


class ItemForm(FlaskForm):
    name = StringField('Название предмета', validators=[DataRequired()])
    submit = SubmitField('Добавить')
    description = TextAreaField('Описание')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    submit = SubmitField('Login')