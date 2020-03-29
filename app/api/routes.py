from datetime import datetime

from flask import request, jsonify

from app import db
from app.api import bp
from app.auth.license import valid_license_required
from app.models import License


@bp.route('/map', methods=['GET'])
@valid_license_required
def provide_map_nodes():
    _map_nodes = "(393,350),(620,425),(265,635),(245,960),(590,772),(715,735),(800,975),(875,875),(1000,640),(1190,640),(1270,795),(1285,485),(1578,540),(1578,365),(410,725),(815,775),(1040,410),(1375,350),(1570,365),(1460,800),(1300,985),(760,565),(830,690),(875,555),(1440,645),(1440,910),(1560,980),(830,395),(465,445),(1550,740),(1290,688),(488,330),(380,575),(400,725),(500,740),(1045,970),(1280,590),(710,925),(1380,480),(1515,620),(1395,995),(960,1068),(540,630),(500,540),(1020,770),(1135,830),(530,845)"
    return jsonify({'success': True, 'nodes': _map_nodes})

@bp.route('/alive', methods=['GET'])
@valid_license_required
def keep_alive():
    _license_key = request.args.get('key')
    _license = License.query.filter_by(license_key=_license_key).first()
    if _license is not None:
        _license.last_seen = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Last Alive has been updated.'})
    return jsonify({'success': False, 'message': 'Could not update last alive.'}), 500