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

#from project.utenti.forms import TagForm
from project.utenti.models import Utente
from project.ruoli.models import Ruolo
from project.blog.models import Post
from project import db
from project.decorators import admin_required

from sqlalchemy import desc,asc

from project.utenti.forms import (
    EditProfileForm,
    EditProfileAdminForm,
)

# Define blueprint
utenti_blueprint = Blueprint(
    "utenti", 
     __name__, 
    template_folder="templates", 
    static_folder='../static'
)



'''
ROUTES per la gestione dei PROFILI
'''
@utenti_blueprint.route('/<username>') 
def user(username):    
    u = Utente.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = u.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['PBG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=u, posts=posts,
                           pagination=pagination)

@utenti_blueprint.route('/edit-profile', methods=['GET', 'POST']) 
@login_required 
def edit_profile():    
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Profilo aggiornato con successo','success')
        return redirect(url_for('utenti.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location    
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@utenti_blueprint.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = Utente.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.ruolo = Ruolo.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('Profilo aggiornato','success')
        return redirect(url_for('utenti.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

'''
Lista utenti
'''
@utenti_blueprint.route('/lista', methods=['GET', 'POST'])
@login_required
def lista():
    # Lista utenti in ordine alfabetico
    lista_utenti = Utente.query.order_by(asc(Utente.username)).all()
    return render_template(
        'utenti_lista.html', 
        lista_utenti=lista_utenti
    )

'''
Cancellazione utenti
'''
@utenti_blueprint.route("/delete/<int:id>", methods=('GET', 'POST'))
@login_required
@admin_required
def utente_delete(id):
    my_user = Utente.query.filter_by(id=id).first()
    try:        
        db.session.delete(my_user)
        db.session.commit()
        flash('Cancellazione avvenuta con successo.', 'success')
    except Exception as e:
        db.session.rollback()
        flash("Errore durante la cancellazione utente: %s" % str(e), 'danger')
    return redirect(url_for('utenti.lista'))

