# from redis import Redis
# from rq import Queue
# import json
# from omicron.inventory import Inventory
# from flask import jsonify, Blueprint, redirect, url_for, render_template
# from flask_login import login_required
#
# q = Queue(connection=Redis(), default_timeout=3600)
# api = Blueprint('api', __name__)
#
#
# # @api.route('/inventory', methods=['POST'])
# # @login_required
# # def inventory_post():
# #     with open('omicron/config.json', 'r') as f:
# #         config_json = json.load(f)
# #     target_mask = config_json["network"]["ip"]
# #     inventory_service = Inventory(target=target_mask)
# #     results = q.enqueue_call(inventory_service.result_scan, result_ttl=500)
# #     # return results.id
# #     # return redirect(url_for('main.inventory'), code=307)
# #     return render_template('inventory.html', name="current_user.name", uid=results.id)
#
#
# @api.route('/api/v1/inventory/result/<uuid>')
# @login_required
# def result(uuid):
#     try:
#         job = q.fetch_job(uuid)
#         if job.is_finished:
#             return jsonify({"status": job.result}), 200
#         else:
#             return jsonify({"status": "pending"}), 202
#     except Exception as e:
#         pass