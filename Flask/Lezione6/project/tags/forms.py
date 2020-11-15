from flask_wtf import FlaskForm

from wtforms import (
    Form,
    validators,
    StringField,
)
from wtforms.validators import DataRequired, Length

'''
Tag Form
'''
class TagForm(FlaskForm):
    name = StringField(u'Titolo tag', validators=[Length(min=-1, max=255, message='Massimo 255 caratteri')])
