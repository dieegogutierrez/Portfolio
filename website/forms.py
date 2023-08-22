from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    name = StringField(label='Name: ', validators=[DataRequired()])
    email = EmailField(label='E-mail: ', validators=[DataRequired()])
    phone = StringField(label='Phone(Optional): ')
    message = TextAreaField(label='Message', validators=[DataRequired()])
    submit = SubmitField(label='Send')