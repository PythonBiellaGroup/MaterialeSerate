from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    session,
    current_app,
)
from flask_login import (
    login_user, 
    logout_user, 
    login_required,
    current_user,
)
#Per le email
from project.email import send_email

from project.utenti.models import Utente
from project.ruoli.models import Ruolo
from project.blog.models import Post
from project import db
from project.decorators import admin_required

from sqlalchemy import desc,asc

from project.auth.forms import (
    LoginForm, 
    RegistrationForm, 
    ChangePasswordForm,
    PasswordResetRequestForm, 
    PasswordResetForm, 
    ChangeEmailForm,
)

# Define blueprint
auth_blueprint = Blueprint(
    "auth", 
     __name__, 
    template_folder="templates", 
    static_folder='../static'
)

#Funzione di controllo (su conferma utenti) che viene eseguita prima di ogni request
@auth_blueprint.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

#Route alla pagina di richiesta mail conferma
@auth_blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        print(current_user)
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')

#Gestione login
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Utente.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            '''
            next contiene la pagina originaria nel caso l'utente fosse stato
            rediretto alla login
            '''
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Mail o password non validi','danger')
    return render_template('login.html', form=form)

#Gestione logout
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Utente disconnesso.','success')
    return redirect(url_for('main.index'))

#Gestione registrazione
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Utente(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        #Token e mail
        token = user.generate_confirmation_token()
        send_email(user.email, 'Conferma registrazione',
                   '/email/confirm', user=user, token=token)
        flash('Una mail di conferma è stata inviata', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

#Gestione conferma utente tramite token da mail di conferma
@auth_blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Registrazione confermata, grazie!', 'success')
    else:
        flash('Link di conferma non valido o scaduto.', 'danger')
    return redirect(url_for('main.index'))

#Nuovo invio email di conferma
@auth_blueprint.route('/confirm')
@login_required
def resend_confirmation():
    #Token e mail
    token = current_user.generate_confirmation_token()

    send_email(current_user.email, 'Conferma il tuo account',
               '/email/confirm', user=current_user, token=token)

    flash('Una nuova mail di conferma è stata inviata', 'success')
    return redirect(url_for('main.index'))

#Gestione cambio password
@auth_blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password aggiornata', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Password non valida', 'danger')
    return render_template("change_password.html", form=form)


#Gestione reset password
@auth_blueprint.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = Utente.query.filter_by(email=form.email.data.lower()).first()
        if user:
            #Token e mail
            token = user.generate_reset_token()

            send_email(user.email, 'Ripristino password dimenticata',
                       '/email/reset_password',
                       user=user, token=token)
            flash('Una email con istruzioni è stata inviata', 'success')
            
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


@auth_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if Utente.reset_password(token, form.password.data):
            db.session.commit()
            flash('Password aggiornata', 'success')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('reset_password.html', form=form)

#Gestione cambio email
@auth_blueprint.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            #Token e mail
            send_email(new_email, 'Conferma nuovo indirizzo email',
                       '/email/change_email',
                       user=current_user, token=token)
            
            flash('Email inviata al tuo nuovo indirizzo email', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Email o password non validi', 'danger')
    return render_template("change_email.html", form=form)


@auth_blueprint.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Email aggiornata', 'success')
    else:
        flash('Richiesta non valida', 'danger')
    return redirect(url_for('main.index'))
