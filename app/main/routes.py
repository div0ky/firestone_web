from flask import make_response, request, render_template, url_for, redirect, send_from_directory, send_file, abort
from flask_login import login_required, current_user
from app.main import bp
import os
from app import db
from app.models import User
from datetime import datetime
from app.models import Post
import requests

# If the api's root address is accessed
@bp.route('/')
@bp.route('/index')
def index():
    # response = requests.get('https://firestone.div0ky.com/version/all')
    response = requests.get('http://localhost:5000/version/all')
    _versions = response.json()
    bot_latest = _versions['bot']
    web_latest = _versions['web']
    docs_latest = _versions['docs']
    changes = Post.query.filter_by(version=bot_latest).all()
    added = [x for x in changes if x.change_type == "Added"]
    changed = [x for x in changes if x.change_type == "Changed"]
    fixed = [x for x in changes if x.change_type == "Fixed"]
    removed = [x for x in changes if x.change_type == "Removed"]
    return render_template('index.html', changes=changes, bot_latest=bot_latest, web_latest=web_latest,
                           docs_latest=docs_latest, added=added, changed=changed, fixed=fixed, removed=removed)

########################################################################################

@bp.route('/u/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user, posts=[])

########################################################################################

@bp.route('/changelog')
def changelog():
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 5, False)
    return render_template('changelog.html', posts=posts.items, pagination=posts)

########################################################################################

@bp.route('/changelog/<string:version>')
def version_changelog(version):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.change_type.asc()).filter_by(version=version).paginate(page, 5, False)
    return render_template('version_changelog.html', posts=posts.items, pagination=posts, bot_latest=version)

########################################################################################

@bp.route('/download')
def download():
    version = request.args.get('ver')
    if not version:
        return abort(400)
    upload_directory = 'static/files/'
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    print(f'v{version}')
    return send_from_directory(upload_directory, f'Firestone_Idle_Bot_{version}.exe', as_attachment=True)
########################################################################################

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip_address = request.environ['REMOTE_ADDR']
        else:
            ip_address = request.environ['HTTP_X_FORWARDED_FOR']

        current_user.ip_address = ip_address
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

########################################################################################