from datetime import datetime

from flask import render_template, redirect, request, flash, url_for, g, jsonify, current_app
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from guess_language import guess_language

from app.main import bp
from app import translator
from app.main.forms import EditProfileForm, EmptyForm, PostForm, SearchForm
from app.models import User, Post


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        User.commit_user()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == ' UNKNOWN' or len(language) > 5:
            language = ''
        post_ = Post(body=form.post.data, author=current_user, language=language)
        Post.add_post(post_)
        flash(_('Your post is now live'))
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='home', posts=posts.items, current_user=current_user,
                           form=form, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user_ = User.get_user_by_username(username=username)
    if not user_:
        render_template('errors/404.html')
    page = request.args.get('page', 1, type=int)
    posts = User.get_posts_of_user(user=user_).paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'],
                                                        error_out=False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user_, posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        User.commit_user()
        flash(_('Your changes have been saved'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, title='Edit Profile')


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    user_ = User.get_user_by_username(username=username)
    if user_ is None:
        flash(_('User %(username)s not found', username=username))
        return redirect(url_for('main.index'))
    if user_ == current_user:
        flash(_('You cannot follow yourself'))
        return redirect(url_for('main.user', username=username))

    current_user.follow(user_)
    flash(_('You are now following %(username)s', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user_ = User.get_user_by_username(username=username)
    if user_ is None:
        flash(_('User %(username)s not found', username=username))
        return redirect(url_for('main.index'))
    if user_ == current_user:
        flash(_('You cannot unfollow yourself'))
        return redirect(url_for('main.user', username=username))

    current_user.unfollow(user_)
    flash(_('You are now unfollowed %(username)s', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translator.translate(request.form['text'],
                                                 request.form['source_language'],
                                                 request.form['dest_language'])})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    print(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    # next_url = url_for('main.search', q=g.search_form.q.data, page=page+1) if total > page * current_app.config['POSTS_PER_PAGE'] else None
    # prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
    #     if page > 1 else None
    # return render_template('search.html', title=_('Search'), posts=posts,
    #                        next_url=next_url, prev_url=prev_url)
    return 'hello'