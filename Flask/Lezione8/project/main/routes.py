
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import current_user

from project.ruoli.models import Permission
from project.blog.forms import PostForm
from project.blog.models import Post

from project import db

main_blueprint = Blueprint(
    "main",
    __name__, 
    template_folder="templates",
    static_folder='../static'
)

'''
Permissions may also need to be checked from templates, 
so the Permission class with all its constants needs to be accessible to them. 
To avoid having to add a template argument in every render_template() call, 
a context processor can be used. 
Context processors make variables available to all templates during rendering
'''
@main_blueprint.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

@main_blueprint.route("/", methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    # Paginazione sui post
    page = request.args.get('page', 1, type=int)
    query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['PBG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination)