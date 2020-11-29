#from datetime import datetime
import datetime

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

from sqlalchemy import desc,asc

from flask_login import login_required

from project.serate.models import Serata
from project.corsi.models import Corso
from project.serate.forms import SerataForm

from project import db
from project.decorators import admin_required

# Define blueprint
serate_blueprint = Blueprint(
    "serate", 
     __name__, 
    template_folder="templates", 
    static_folder='../static'
)

'''
Lista delle serate in ordine di data
'''
@serate_blueprint.route("/prossime", methods=["GET"])
def prossime():
    # Filtro data futura, ordinamento per data
    lista_serate = Serata.query.filter(Serata.data > datetime.datetime.now()).order_by(asc(Serata.data)).all()
    # Creo una lista parallela dei corsi collegati alle serate
    lista_corsi = [ Corso.query.filter_by(id=s.corso_id).first() for s in lista_serate ]
    # Nel template non è possibile iterare su due liste, quindi zippo le due liste e le passo
    zipped_data = zip(lista_serate, lista_corsi)
    return render_template(
        'serate_prossime.html', 
        zipped_data=zipped_data
    )

'''
Lista di tutte le serate in ordine di data
'''
@serate_blueprint.route("/lista", methods=["GET"])
@login_required
def lista():
    # Filtro data futura, ordinamento per data
    lista_serate = Serata.query.order_by(desc(Serata.data)).all()
    # Creo una lista parallela dei corsi collegati alle serate
    lista_corsi = [ Corso.query.filter_by(id=s.corso_id).first() for s in lista_serate ]
    # Nel template non è possibile iterare su due liste, quindi zippo le due liste e le passo
    zipped_data = zip(lista_serate, lista_corsi)
    return render_template(
        'serate_lista.html', 
        zipped_data=zipped_data
    )

'''
Cancellazione serata
'''
@serate_blueprint.route("/delete/<int:id>", methods=('GET', 'POST'))
@login_required
def serata_delete(id):
    my_serata = Serata.query.filter_by(id=id).first()
    try:        
        #TODO Capire errore "sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.NoneType' is not mapped"
        db.session.delete(my_serata)
        db.session.commit()
        flash('Cancellazione avvenuta con successo.', 'success')
    except Exception as e:
        db.session.rollback()
        flash("Errore durante la cancellazione della serata: %s" % str(e), 'danger')
    return redirect(url_for('serate.lista'))

'''
Edit serata
'''
@serate_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_serata(id):
    my_serata = Serata.query.get_or_404(id)
    form = SerataForm(serata=my_serata)
    if form.validate_on_submit():
        my_serata.nome = form.nome.data
        my_serata.descrizione = form.descrizione.data
        # Gestione data e ora in due campi separati
        form_data = form.data.data
        txt_time = form.txt_time.data
        if not txt_time:
            txt_time = "00:00"
        # Converto in oggetto datetime.time per combinarlo con la data
        # in fase di creazione oggetto Serata
        data_time = datetime.datetime.strptime(txt_time, '%H:%M').time()
        my_serata.data = datetime.datetime.combine(form_data,data_time)
        my_serata.txt_time = form.txt_time.data
        my_serata.link_partecipazione = form.link_partecipazione.data
        my_serata.link_registrazione = form.link_registrazione.data
        db.session.add(my_serata)
        db.session.commit()
        flash('Serata aggiornata','success')
        return redirect(url_for('serate.lista'))

    form.nome.data = my_serata.nome
    form.descrizione.data = my_serata.descrizione
    form.data.data = my_serata.data
    form.txt_time.data = my_serata.data.strftime('%H:%M')
    form.link_partecipazione.data = my_serata.link_partecipazione
    form.link_registrazione.data = my_serata.link_registrazione
    return render_template('serata_edit.html', form=form, serata=my_serata)
