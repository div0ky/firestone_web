from flask import make_response, request
from flask_login import login_required, current_user
from app.main import bp
from app import db
from datetime import datetime

# If the api's root address is accessed
@bp.route('/')
def root():
    response = make_response('div0ky API v0.4', 200)
    response.mimetype = 'text/plain'
    return response

# @bp.before_request
# def before_request():
#     if current_user.is_authenticated:
#         if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
#             ip_address = request.environ['REMOTE_ADDR']
#         else:
#             ip_address = request.environ['HTTP_X_FORWARDED_FOR']
#
#         current_user.ip_address = ip_address
#         current_user.last_seen = datetime.utcnow()
#
#         db.session.commit()