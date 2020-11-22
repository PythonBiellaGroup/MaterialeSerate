from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from project.utenti.models import Utente

'''
Tutti i messaggi sono stati personalizzati in italiano
Tolta la validazione standard nella form
'''

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email obbligatoria'), Length(1, 64),
                                             Email(message="Email non valida")])
    password = PasswordField('Password', validators=[DataRequired(message='Password obbligatoria')])
    remember_me = BooleanField('Ricordami su questo sito')
    submit = SubmitField('Entra')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email obbligatoria'), Length(1, 64),
                                             Email(message="Email non valida")])
    username = StringField('Username', validators=[
        DataRequired(message='Username obbligatorio'), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Nome utente deve essere composto solo da lettere, numeri, punti o underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password obbligatoria'), EqualTo('password2', message='Le due password devono combaciare')])
    password2 = PasswordField('Conferma password', validators=[DataRequired(message='Conferma password obbligatoria')])
    submit = SubmitField('Registrati')

    def validate_email(self, field):
        if Utente.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(u'Email già registrata.')

    def validate_username(self, field):
        if Utente.query.filter_by(username=field.data).first():
            raise ValidationError(u'Username già in uso.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Vecchia password', validators=[DataRequired(message='Vecchia password obbligatoria')])
    password = PasswordField('Nuova password', validators=[
        DataRequired(message='Nuova password obbligatoria'), EqualTo('password2', message='Le due passwords devono essere uguali')])
    password2 = PasswordField('Conferma nuova password',
                              validators=[DataRequired(message='Conferma nuova password obbligatoria')])
    submit = SubmitField('Aggiorna password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email obbligatoria'), Length(1, 64),
                                             Email(message="Email non valida")])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Nuova password', validators=[
        DataRequired(message='Nuova password obbligatoria'), EqualTo('password2', message='Le due passwords devono essere uguali')])
    password2 = PasswordField('Conferma password', validators=[DataRequired(message='Conferma nuova password obbligatoria')])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('Nuova Email', validators=[DataRequired(message='Nuova email obbligatoria'), Length(1, 64),
                                                 Email(message="Email non valida")])
    password = PasswordField('Password', validators=[DataRequired(message='Password obbligatoria')])
    submit = SubmitField('Email aggiornata')

    def validate_email(self, field):
        if Utente.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(u'Email già registrata.')