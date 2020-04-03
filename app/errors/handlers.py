from flask import make_response, request, render_template
from app import db
from app.errors import bp

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('/errors/404.html'), 404

########################################################################################

@bp.app_errorhandler(500)
def page_not_found(error):
    db.session.rollback()
    response = make_response(f"This address does not exist: {request.url}")
    response.mimetype = 'text/plain'
    response.status_code = 500
    return response

########################################################################################

@bp.app_errorhandler(405)
def page_not_found(error):
    db.session.rollback()
    response = make_response(f"Used method is not permitted.")
    response.mimetype = 'text/plain'
    response.status_code = 405
    return response

########################################################################################

@bp.app_errorhandler(401)
def page_not_found(error):
    db.session.rollback()
    response = make_response(f"You do not have permission to view this resource.")
    response.mimetype = 'text/plain'
    response.status_code = 401
    return response

########################################################################################

@bp.app_errorhandler(400)
def bad_request(error):
    db.session.rollback()
    return render_template('/errors/400.html'), 400