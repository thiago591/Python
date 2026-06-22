# Aluno: Thiago Pereira Resende

from . import db
from .base import ModeloBase


class OfertaTroca(ModeloBase):
    __tablename__ = "ofertas_troca"

    colecionador_id = db.Column(
        db.Integer,
        db.ForeignKey("colecionadores.id"),
        nullable=False,
    )
    observacao = db.Column(db.String(255), nullable=True)

    colecionador = db.relationship("Colecionador", back_populates="ofertas")
    itens = db.relationship(
        "ItemOferta",
        back_populates="oferta",
        cascade="all, delete-orphan",
    )

    @classmethod
    def listar_com_colecionador(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()


class ItemOferta(ModeloBase):
    __tablename__ = "itens_oferta"

    oferta_id = db.Column(
        db.Integer,
        db.ForeignKey("ofertas_troca.id"),
        nullable=False,
    )
    figurinha_id = db.Column(
        db.Integer,
        db.ForeignKey("figurinhas.id"),
        nullable=False,
    )
    tipo = db.Column(db.String(20), nullable=False)  # "oferece" ou "deseja"
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    oferta = db.relationship("OfertaTroca", back_populates="itens")
    figurinha = db.relationship("Figurinha", back_populates="itens_oferta")
