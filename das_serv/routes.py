from flask import Blueprint
from flask import render_template
from flask import request

from extensions import db


app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def index():
    from model import Metrics

    local_metrics = {}
    total_metrics = {}
    metrics = Metrics.get_metrics(limit=100)
    if metrics:
        local_metrics = Metrics.get_metrics_info(db.session, limit=100)
        total_metrics = Metrics.get_metrics_info(db.session, limit=None)

    return render_template(
        'index.html',
        title='Система сбора информации',
        metrics=metrics,
        total_metrics=total_metrics,
        local_metrics=local_metrics
    )


@app_bp.route('/send_metric', methods=['POST'])
def send_metric():
    from model import Metrics, Client, get_or_create

    if request.method == 'POST':
        data = request.json
        if data.get('client') and data.get('value'):
            client = get_or_create(db.session, Client, name=data['client'])
            Metrics.create_metric(db.session, client.id, data['value'])
            return 'OK', 200
    return 'FAIL', 500
