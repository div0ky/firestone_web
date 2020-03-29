from app.models import License, User
from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required

from app.admin import bp
from app.admin.forms import LoginForm
from app.models import License, User


@bp.route('/list')
@login_required
def list_active_bots():
    _licenses = License.query.all()
    if _licenses is not None:
        bot = []
        for _license in _licenses:
            if _license.last_seen + timedelta(minutes=5) >= datetime.utcnow():
                bot.append({'license_key': _license.license_key, 'email': _license.email, 'country': _license.country,
                            'order_number': _license.order_number, 'last_seen': _license.last_seen, 'age': 'active'})
            else:
                bot.append({'license_key': _license.license_key, 'email': _license.email, 'country': _license.country,
                            'order_number': _license.order_number,
                            'last_seen': _license.last_seen + timedelta(minutes=5), 'age': 'inactive'})

    return render_template('list.html', alive=bot)