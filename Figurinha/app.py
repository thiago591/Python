# Aluno: Thiago Pereira Resende
from flask import Flask, redirect, url_for

from controllers import figurinhas_bp
from models import Colecionador, Figurinha, db


def criar_app():
    app = Flask(__name__, template_folder="views/templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aula11_figurinhas.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(figurinhas_bp)

    @app.route("/")
    def home():
        return redirect(url_for("figurinhas.index"))

    with app.app_context():
        db.create_all()
        popular_banco_se_vazio()

    return app


def popular_banco_se_vazio():
    if Colecionador.query.first() is None:
        db.session.add_all(
            [
                Colecionador(apelido="Joaozinho", cidade="Belo Horizonte"),
                Colecionador(apelido="Maria10", cidade="Contagem"),
                Colecionador(apelido="CraqueBH", cidade="Betim"),
            ]
        )

    if Figurinha.query.first() is None:
        db.session.add_all(
            [
                Figurinha(numero=10, nome_jogador="Neymar", time="Brasil"),
                Figurinha(numero=7, nome_jogador="Vini Jr", time="Brasil"),
                Figurinha(numero=9, nome_jogador="Richarlison", time="Brasil"),
                Figurinha(numero=30, nome_jogador="Messi", time="Argentina"),
                Figurinha(numero=11, nome_jogador="Mbappe", time="Franca"),
            ]
        )

    db.session.commit()


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
