from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    #body = PageDownField("Cosa vuoi condividere?", render_kw={'placeholder':'content'}, validators=[DataRequired(message='Inserisci un testo')])
    body = PageDownField("", validators=[DataRequired(message='Inserisci un testo')])
    submit = SubmitField('Conferma')