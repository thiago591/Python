from datetime import datetime

from . import db


class ModeloBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_atualizacao = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
