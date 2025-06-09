from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ItemForm(FlaskForm):
    name = StringField(
        'Название предмета',
        validators=[DataRequired(), Length(max=100)]
    )
    description = TextAreaField(
        'Описание',
        validators=[Length(max=500)]
    )
    submit = SubmitField('Сохранить')

