import json
from datetime import datetime

from flask import request, jsonify
from flask_login import login_required, current_user

from app import db
from app.api import bp
from app.auth.license import valid_license_required
from app.models import License, User


@bp.route('/map', methods=['GET'])
@valid_license_required
def provide_map_nodes():
    _map_nodes = "(393,350),(620,425),(265,635),(245,960),(590,772),(715,735),(800,975),(875,875),(1000,640),(1190,640),(1270,795),(1285,485),(1578,540),(1578,365),(410,725),(815,775),(1040,410),(1375,350),(1570,365),(1460,800),(1300,985),(760,565),(830,690),(875,555),(1440,645),(1440,910),(1560,980),(830,395),(465,445),(1550,740),(1290,688),(488,330),(380,575),(400,725),(500,740),(1045,970),(1280,590),(710,925),(1380,480),(1515,620),(1395,995),(960,1068),(540,630),(500,540),(1020,770),(1135,830),(530,845)"
    return jsonify({'success': True, 'nodes': _map_nodes})

########################################################################################

@bp.route('/alive', methods=['GET'])
@valid_license_required
def keep_alive():
    _license_key = request.args.get('key')
    _license = License.query.filter_by(license_key=_license_key).first()
    if _license is not None:
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip_address = request.environ['REMOTE_ADDR']
        else:
            ip_address = request.environ['HTTP_X_FORWARDED_FOR']

        if _license.all_ips:
            all_ips = _license.all_ips.split(',')
            if ip_address not in all_ips:
                all_ips.append(ip_address)
            _license.all_ips = (',').join(all_ips)
        else:
            all_ips = ip_address
            _license.all_ips = all_ips

        _license.current_ip = ip_address
        _license.last_seen = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Last Alive has been updated.', 'edition': _license.edition})
    return jsonify({'success': False, 'message': 'Could not update last alive.'}), 500

########################################################################################

@bp.route('/version/<item>')
def versions(item):
    try:
        with open('app/static/versions.json', 'r') as file:
            items = json.load(file)
    except Exception as e:
        return jsonify({'success': False, "message": e})
    if item == "all":
        return jsonify(items)
    else:
        return f"{items[item]}"

########################################################################################

@bp.route('/badge')
def badge():
    type = request.args.get('type')
    try:
        with open('app/static/versions.json', 'r') as file:
            items = json.load(file)
    except Exception as e:
        return jsonify({'success': False, "message": e})

    color = '437c90'
    style = 'flat-square'

    bot_latest = items['bot']
    web_latest = items['web']
    docs_latest = items['docs']

    if type == 'bot':
        return jsonify({"schemaVersion": 1, "label": 'bot', 'message': bot_latest, 'color': color, 'style': style})
    elif type == 'web':
        return jsonify({"schemaVersion": 1, "label": 'web', 'message': web_latest, 'color': color, 'style': style})
    elif type == 'docs':
        return jsonify({"schemaVersion": 1, "label": 'docs', 'message': docs_latest, 'color': color, 'style': style})
    else:
        return jsonify({"schemaVersion": 1, "label": 'error', 'message': 'invalid', 'color': 'dc3545', 'style': style, 'isError': True})

########################################################################################

@bp.route('/badge/<user>')
@login_required
def badge(user):
        _user = User.query.filter_by(username=user).first()
        if not _user:
            return jsonify({"schemaVersion": 1, "label": 'error', 'message': 'invalid', 'color': 'dc3545', 'style': style, 'isError': True})

        color = '437c90'
        style = 'flat-square'
        edition = _user.edition

        return jsonify({"schemaVersion": 1, "label": 'Firestone Idle Bot', 'message': edition, 'color': color, 'style': style})