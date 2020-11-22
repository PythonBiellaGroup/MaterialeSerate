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
from flask_login import login_required
from sqlalchemy import desc,asc
import datetime

from project.corsi.forms import CorsiForm, write_to_disk
from project.serate.forms import SerataForm
from project.serate.models import Serata
from project.corsi.models import Corso
from project import db


# Define blueprint
corsi_blueprint = Blueprint(
    "corsi", 
    __name__, 
    template_folder="templates",
    static_folder='../static'
)

'''
Lista dei corsi in ordine alfabetico
'''
@corsi_blueprint.route("/lista", methods=["GET"])
def lista():
    # Ordinamento alfabetico ascendente per titolo
    lista_corsi = Corso.query.order_by(asc(Corso.nome)).all()
    return render_template(
        'corsi_lista.html', 
        lista_corsi=lista_corsi
    )


'''
Creazione di un corso (senza serate e senza tags)
'''
@corsi_blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = CorsiForm()

    if form.validate_on_submit():

        name = form.name.data
        teacher = form.teacher.data
        level = form.level.data
        description = form.description.data

        n_course = Corso(name, teacher, level, description)
        db.session.add(n_course)

        form.name.data = ""
        form.teacher.data = ""
        form.level.data = ""
        form.description.data = ""
        
        try:
            db.session.commit()
            flash('Corso creato correttamente', 'success')
            return redirect(url_for('corsi.lista'))
        except Exception as e:
            db.session.rollback()
            flash("Errore durante la creazione del corso: %s" % str(e), 'danger')

    return render_template("corsi_create.html", form=form)


'''
Visualizzazione di un corso (con gestione serate e tags (TODO))
'''
@corsi_blueprint.route("/<int:corso_id>", methods=('GET', 'POST'))
def dettaglio_corso(corso_id):
    
    # Gestione aggiunta serate
    form = SerataForm()
    if form.validate_on_submit():

        data = form.data.data #date (not datetime!) object
        txt_time = form.txt_time.data #string formato HH:MM
        if not txt_time:
            txt_time = "00:00"
        # Converto in oggetto datetime.time per combinarlo con la data
        # in fase di creazione oggetto Serata
        data_time = datetime.datetime.strptime(txt_time, '%H:%M').time()
        nome =  form.nome.data
        descrizione = form.descrizione.data
        link_partecipazione = form.link_partecipazione.data
        link_registrazione = form.link_registrazione.data

        nuova_serata = Serata(
            nome, 
            descrizione, 
            datetime.datetime.combine(data,data_time), # Combino data con ore-minuti
            link_partecipazione,
            link_registrazione)
        nuova_serata.corso_id = corso_id
        # Reset dei campi della form
        form.data.data = ""
        form.txt_time.data = ""
        form.nome.data = ""
        form.descrizione.data = ""
        form.link_partecipazione.data = ""
        form.link_registrazione.data = ""

        db.session.add(nuova_serata)
        try:
            db.session.commit()
            flash('Inserimento avvenuto con successo.', 'success')
        except Exception as e:
            flash("Errore durante l'inserimento della serata: %s" % str(e), 'error')
            db.session.rollback()
    
    corso = Corso.query.get_or_404(corso_id)
    return render_template('corsi_dettaglio.html', corso=corso, form=form)


'''
Cancellazione di un corso
'''
@corsi_blueprint.route("/delete/<int:id>", methods=('GET', 'POST'))
@login_required
def corso_delete(id):
    '''
    Delete corso
    '''
    my_course = Corso.query.filter_by(id=id).first()
    db.session.delete(my_course)
    try:
        db.session.commit()
        flash('Cancellazione avvenuta con successo.', 'success')
    except Exception as e:
        db.session.rollback()
        flash("Errore durante la cancellazione del corso: %s" % str(e), 'danger')
    return redirect(url_for('corsi.lista'))