from flask import Blueprint, render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user

from project import db
from project.decorators import permission_required

from project.blog.forms import PostForm
from project.commenti.forms import CommentForm

from project.blog.models import Post
from project.commenti.models import Comment
from project.ruoli.models import Permission


# Define blueprint
commenti_blueprint = Blueprint(
    "commenti", 
     __name__, 
    template_folder="templates", 
    static_folder='../static'
)


'''
Gestione commenti da moderare
'''
@commenti_blueprint.route('/')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    # Paginazione sui commenti
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['PBG_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


'''
Ri-abilita commento
'''
@commenti_blueprint.route('/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))

'''
Disabilita commento
'''
@commenti_blueprint.route('/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))

