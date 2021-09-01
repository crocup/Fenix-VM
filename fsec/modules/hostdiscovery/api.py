from flask import Blueprint, jsonify
from flask_login import login_required
from fsec.modules.hostdiscovery.hostdiscovery import result_scanner, HostDiscovery

hostdiscovery = Blueprint('hostdiscovery', __name__)


@hostdiscovery.route('/api/v1/host/discover/', methods=['POST'])
@login_required
def hdiscovery_index():
    """
    дописать .....
    """
    result_scanner(HostDiscovery('192.168.1.0/24'))
    return jsonify(success=True)
