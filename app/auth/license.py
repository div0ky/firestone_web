from functools import wraps
from flask import request, jsonify
from app.models import License
from datetime import datetime
from app import db

import requests, json

def valid_license_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        license_key = request.args.get('key')

        if not license_key:
            return jsonify({'success': False, 'message': 'Missing expected argument.'}), 400

        data = {
            'product_permalink': 'Pztmb',
            'license_key': license_key,
            'increment_uses_count': 'false'
        }

        response = requests.post('https://api.gumroad.com/v2/licenses/verify', data=data)
        response = json.loads(response.text)
        if response['success']:

            key_info = response['purchase']
            _email = key_info['email']
            _country = key_info['ip_country']
            _order_number = key_info['order_number']
            _last_seen = datetime.utcnow()

            _refunded = bool(key_info['refunded'])
            _disputed = bool(key_info['disputed'])
            _chargedback = bool(key_info['chargebacked'])

            if not _refunded and not _disputed and not _chargedback:
                _license_found = License.query.filter_by(license_key=license_key).first()

                if not _license_found:
                    new_license = License(license_key=license_key, email=_email, country=_country, order_number=_order_number, last_seen=_last_seen)
                    db.session.add(new_license)
                    db.session.commit()

                return f(*args, **kwargs)
            else:
                return jsonify({'success': False, 'message': 'Provided license key is invalid.'})
        else:
            return jsonify({'success': False, 'message': 'Provided license key is invalid.'})
    return decorator
