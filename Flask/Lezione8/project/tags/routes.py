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

from project.tags.forms import TagForm
from project.tags.models import Tag
from project import db
from project.decorators import admin_required

from sqlalchemy import desc,asc

# Define blueprint
tags_blueprint = Blueprint(
    "tags", 
     __name__, 
    template_folder="templates", 
    static_folder='../static'
)    

'''
Lista dei tags con la possibilità di creazione di nuovo tag
'''
@tags_blueprint.route("/", methods=('GET', 'POST'))
@login_required
def tags():
    # Ordinamento alfabetico ascendente per "name"
    lista_tags = Tag.query.order_by(asc(Tag.name)).all()
    '''
    Crea nuovo tag
    '''
    form = TagForm()
    if form.validate_on_submit():
        tag_name = form.name.data
        n_tag = Tag(tag_name)
        db.session.add(n_tag)
        form.name.data = ""
        try:
            db.session.commit()
            flash('Tag creato correttamente', 'success')
            return redirect(url_for('tags.tags'))
        except Exception as e:
            db.session.rollback()
            flash("Errore durante la creazione del tag: %s" % str(e), 'danger')

    return render_template('tags_lista.html', form=form, lista_tags=lista_tags)

'''
Cancellazione tag
'''
@tags_blueprint.route("/delete/<int:id>", methods=('GET', 'POST'))
@login_required
@admin_required
def tag_delete(id):
    '''
    Delete tag
    '''
    my_tag = Tag.query.filter_by(id=id).first()
    db.session.delete(my_tag)
    try:
        db.session.commit()
        flash('Cancellazione avvenuta con successo.', 'success')
    except Exception as e:
        db.session.rollback()
        flash("Errore durante la cancellazione del tag: %s" % str(e), 'danger')
    return redirect(url_for('tags.tags'))

'''
Modifica tag by id
'''
@tags_blueprint.route("/<id>", methods=('GET', 'POST'))
@login_required
@admin_required
def edit_tag(id):
    '''
    Edit tag
    :param id: Id from tag
    '''
    my_tag = Tag.query.filter_by(id=id).first()
    form = TagForm(obj=my_tag)
    if form.validate_on_submit():
        form.populate_obj(my_tag)
        db.session.add(my_tag)
        try:
            db.session.commit()
            flash('Aggiornamento avvenuto con successo', 'success')
        except Exception as e:
            db.session.rollback()
            flash("Errore durante l'aggiornamento del tag: %s" % str(e), 'danger')
    return render_template(
        '/tags_edit.html',
        form=form,tag=my_tag)
