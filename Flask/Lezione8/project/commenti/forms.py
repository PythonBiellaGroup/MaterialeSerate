from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms import ValidationError

class CommentForm(FlaskForm):
    body = StringField('Inserisci qui il tuo commento', validators=[DataRequired(message='Inserisci un testo')])
    submit = SubmitField('Conferma')
