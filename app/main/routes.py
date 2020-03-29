from flask import make_response, request, render_template, url_for, redirect
from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.models import User
from datetime import datetime

# If the api's root address is accessed
@bp.route('/')
@bp.route('/index')
def index():
    # return render_template('index.html', page_title="Welcome!", page_lead="You'll likely need to login for this site to be of any use to you.")
    return redirect(url_for('auth.login'))

@bp.route('/u/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user, posts=[])

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