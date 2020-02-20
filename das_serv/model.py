from datetime import datetime

from sqlalchemy.sql import func

from extensions import db


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)


class Metrics(db.Model):
    __tablename__ = 'metrics'
    id = db.Column('id', db.Integer, primary_key=True)
    client = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    cpu_value = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime)

    def __init__(self, client, cpu_value):
        self.client = client
        self.cpu_value = cpu_value
        self.pub_date = datetime.now()

    @staticmethod
    def create_metric(session, client_id, cpu_value):
        metric = Metrics(client=client_id, cpu_value=cpu_value)
        session.add(metric)
        session.commit()

    @staticmethod
    def get_metrics(limit=100):
        return Metrics.query.order_by(Metrics.pub_date.desc()).limit(limit).all()

    @staticmethod
    def get_metrics_info(session, limit=None):
        q = session.query(Metrics.cpu_value).order_by(Metrics.pub_date.desc())
        if limit:
            sub = q.limit(limit).subquery()
        else:
            sub = q.subquery()

        max_cpu, min_cpu, avg_cpu = session.query(
            func.max(sub.c.cpu_value),
            func.min(sub.c.cpu_value),
            func.avg(sub.c.cpu_value)
        ).first()

        return {'max_cpu': max_cpu, 'min_cpu': min_cpu, 'avg_cpu': round(avg_cpu, 2)}


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def create_all(app):
    db.create_all(app=app)
