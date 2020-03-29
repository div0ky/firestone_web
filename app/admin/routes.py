from app import db
from app.models import License
from flask import make_response, json, render_template
from app.admin import bp
from datetime import datetime, timedelta


@bp.route('/current')
def report_active_bots():
    _licenses = License.query.all()
    if _licenses is not None:
        for x in _licenses:
            print(x.license_key)
        bot = []
        recently_alive = []
        for _license in _licenses:
            if _license.last_seen + timedelta(minutes=5) >= datetime.utcnow():
                bot.append({'license_key': _license.license_key, 'email': _license.email, 'country': _license.country,
                            'order_number': _license.order_number, 'last_seen': _license.last_seen, 'age': 'active'})
            else:
                bot.append({'license_key': _license.license_key, 'email': _license.email, 'country': _license.country,
                            'order_number': _license.order_number,
                            'last_seen': _license.last_seen + timedelta(minutes=5), 'age': 'inactive'})
        for b in bot:
            print(b['age'])

    return render_template('current.html', alive=bot)
