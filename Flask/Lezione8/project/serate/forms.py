from time import strftime
from flask_wtf import FlaskForm
from wtforms import (
    Form,
    validators,
    StringField,
    IntegerField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
    DateField
)
from wtforms.validators import DataRequired, Length

'''
Serata Form
'''
class SerataForm(FlaskForm):
    nome = StringField(
        u'Titolo della serata', 
        validators=[Length(min=-1, max=100, message='Massimo 100 caratteri')]
    )
    descrizione = StringField(
        u'Descrizione', 
        validators=[Length(min=-1, max=255, message='Massimo 255 caratteri')]
    )
    '''
    Nella form data DD/MM/YYYY e ora HH:MM sono due input field separati
    Nella tabella c'è un solo campo
    La logica di combinazione tra i due campi è nel controller (routes.py)
    '''
    data = DateField(u'Data', format='%d/%m/%Y')
    txt_time = StringField(
        u'Ore minuti',
        validators=[Length(min=-1, max=5, message='Formato HH:MM')]
    )
    link_partecipazione = StringField(
        u"Link di partecipazione all'incontro",
        validators=[Length(min=-1, max=255, message='Massimo 255 caratteri')]
    )
    link_registrazione = StringField(
        u"Link della registrazione dell'incontro",
        validators=[Length(min=-1, max=255, message='Massimo 255 caratteri')]
    )
    submit = SubmitField('Conferma')