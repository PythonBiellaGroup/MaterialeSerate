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
blog_blueprint = Blueprint(
    "blog", 
     __name__, 
    template_folder="templates", 
    static_folder='../static'
)

'''
Visualizzazione post e inserimento commento
'''
@blog_blueprint.route('/post/<int:id>', methods=['GET', 'POST'])
def view_post(id):
    p = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=p,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Commento pubblicato','success')
        return redirect(url_for('blog.view_post', id=p.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (p.comments.count() - 1) // \
            current_app.config['PBG_COMMENTS_PER_PAGE'] + 1
    pagination = p.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['PBG_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[p], form=form,
                           comments=comments, pagination=pagination)

'''
Modifica post
'''
@blog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('Post aggiornato', 'success')
        return redirect(url_for('blog.view_post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

