from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .colecionador import Colecionador
from .figurinha import Figurinha
from .oferta import ItemOferta, OfertaTroca

__all__ = [
    "db",
    "ModeloBase",
    "Colecionador",
    "Figurinha",
    "OfertaTroca",
    "ItemOferta",
]
