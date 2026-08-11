import os
import sqlite3
from functools import wraps

import requests
from flask import (
    Flask, flash, g, jsonify, redirect, render_template,
    request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-troque-em-producao"
)
app.config["DATABASE"] = os.path.join(app.instance_path, "tarefas.sqlite3")

os.makedirs(app.instance_path, exist_ok=True)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'pendente'
                CHECK(status IN ('pendente', 'andamento', 'concluida')),
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );
        """
    )
    db.commit()


@app.cli.command("init-db")
def init_db_command():
    """Cria as tabelas do banco."""
    with app.app_context():
        init_db()
    print("Banco de dados inicializado.")



def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.before_request
def load_logged_user():
    user_id = session.get("user_id")
    g.user = None

    if user_id is not None:
        g.user = get_db().execute(
            "SELECT id, nome, email FROM usuarios WHERE id = ?",
            (user_id,),
        ).fetchone()


@app.context_processor
def inject_user():
    return {"current_user": g.user}


@app.route("/registro", methods=("GET", "POST"))
def registro():
    if g.user is not None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar_senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "danger")
        elif senha != confirmar:
            flash("As senhas não coincidem.", "danger")
        elif len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "danger")
        else:
            db = get_db()
            try:
                cursor = db.execute(
                    """
                    INSERT INTO usuarios (nome, email, senha)
                    VALUES (?, ?, ?)
                    """,
                    (nome, email, generate_password_hash(senha)),
                )
                db.commit()
                session.clear()
                session["user_id"] = cursor.lastrowid
                flash("Conta criada com sucesso!", "success")
                return redirect(url_for("dashboard"))
            except sqlite3.IntegrityError:
                flash("Este e-mail já está cadastrado.", "danger")

    return render_template("auth/registro.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if g.user is not None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        user = get_db().execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()

        if user is None or not check_password_hash(user["senha"], senha):
            flash("E-mail ou senha inválidos.", "danger")
        else:
            session.clear()
            session["user_id"] = user["id"]
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login"))


VALID_STATUSES = {"pendente", "andamento", "concluida"}


@app.route("/")
def index():
    if g.user:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    status_filter = request.args.get("status", "todas")
    search_query = request.args.get("q", "").strip()
    allowed_filters = {"todas", "pendente", "andamento", "concluida"}

    if status_filter not in allowed_filters:
        status_filter = "todas"

    db = get_db()

    where = ["usuario_id = ?"]
    params = [g.user["id"]]
    if status_filter != "todas":
        where.append("status = ?")
        params.append(status_filter)
    if search_query:
        where.append("(titulo LIKE ? OR descricao LIKE ?)")
        like = f"%{search_query}%"
        params.extend([like, like])

    tarefas = db.execute(
        f"SELECT * FROM tarefas WHERE {' AND '.join(where)} ORDER BY id DESC",
        tuple(params),
    ).fetchall()

    resumo = db.execute(
        """
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(status = 'pendente'), 0) AS pendente,
            COALESCE(SUM(status = 'andamento'), 0) AS andamento,
            COALESCE(SUM(status = 'concluida'), 0) AS concluida
        FROM tarefas WHERE usuario_id = ?
        """,
        (g.user["id"],),
    ).fetchone()
    total = resumo["total"] or 0
    percentual = round((resumo["concluida"] / total) * 100) if total else 0
    resumo = dict(resumo)
    resumo["percentual"] = percentual

    return render_template(
        "dashboard.html",
        tarefas=tarefas,
        status_filter=status_filter,
        search_query=search_query,
        resumo=resumo,
    )


@app.route("/nova_tarefa", methods=("GET", "POST"))
@login_required
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "pendente")

        if not titulo:
            flash("O título da tarefa é obrigatório.", "danger")
        elif status not in VALID_STATUSES:
            flash("Status inválido.", "danger")
        else:
            db = get_db()
            db.execute(
                """
                INSERT INTO tarefas (titulo, descricao, status, usuario_id)
                VALUES (?, ?, ?, ?)
                """,
                (titulo, descricao, status, g.user["id"]),
            )
            db.commit()
            flash("Tarefa criada com sucesso!", "success")
            return redirect(url_for("dashboard"))

    return render_template("tarefa_form.html", tarefa=None)


def get_user_task(task_id):
    return get_db().execute(
        """
        SELECT * FROM tarefas
        WHERE id = ? AND usuario_id = ?
        """,
        (task_id, g.user["id"]),
    ).fetchone()


@app.route("/editar/<int:task_id>", methods=("GET", "POST"))
@login_required
def editar(task_id):
    tarefa = get_user_task(task_id)

    if tarefa is None:
        flash("Tarefa não encontrada.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "pendente")

        if not titulo:
            flash("O título da tarefa é obrigatório.", "danger")
        elif status not in VALID_STATUSES:
            flash("Status inválido.", "danger")
        else:
            db = get_db()
            db.execute(
                """
                UPDATE tarefas
                SET titulo = ?, descricao = ?, status = ?
                WHERE id = ? AND usuario_id = ?
                """,
                (titulo, descricao, status, task_id, g.user["id"]),
            )
            db.commit()
            flash("Tarefa atualizada!", "success")
            return redirect(url_for("dashboard"))

    return render_template("tarefa_form.html", tarefa=tarefa)


@app.post("/excluir/<int:task_id>")
@login_required
def excluir(task_id):
    tarefa = get_user_task(task_id)

    if tarefa is None:
        flash("Tarefa não encontrada.", "danger")
    else:
        db = get_db()
        db.execute(
            "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
            (task_id, g.user["id"]),
        )
        db.commit()
        flash("Tarefa excluída.", "success")

    return redirect(url_for("dashboard"))


@app.post("/concluir/<int:task_id>")
@login_required
def concluir(task_id):
    tarefa = get_user_task(task_id)

    if tarefa is None:
        flash("Tarefa não encontrada.", "danger")
    else:
        db = get_db()
        novo_status = (
            "concluida" if tarefa["status"] != "concluida" else "pendente"
        )
        db.execute(
            """
            UPDATE tarefas SET status = ?
            WHERE id = ? AND usuario_id = ?
            """,
            (novo_status, task_id, g.user["id"]),
        )
        db.commit()
        flash("Status da tarefa atualizado.", "success")

    return redirect(url_for("dashboard"))


@app.get("/api/progresso")
@login_required
def api_progresso():
    rows = get_db().execute(
        """
        SELECT status, COUNT(*) AS quantidade
        FROM tarefas
        WHERE usuario_id = ?
        GROUP BY status
        """,
        (g.user["id"],),
    ).fetchall()

    counts = {"pendente": 0, "andamento": 0, "concluida": 0}
    for row in rows:
        counts[row["status"]] = row["quantidade"]

    return jsonify(counts)


@app.route("/dashboard/progresso")
@login_required
def dashboard_progresso():
    return render_template("progresso.html")


@app.get("/api/frase")
@login_required
def api_frase():
    try:
        response = requests.get(
            "https://api.adviceslip.com/advice",
            timeout=5,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        data = response.json()
        return jsonify({"frase": data["slip"]["advice"]})
    except (requests.RequestException, KeyError, ValueError):
        return jsonify(
            {"frase": "Continue aprendendo: pequenos passos constroem grandes resultados."}
        )


@app.get("/api/resumo")
@login_required
def api_resumo():
    row = get_db().execute(
        """
        SELECT COUNT(*) AS total,
               COALESCE(SUM(status = 'pendente'), 0) AS pendente,
               COALESCE(SUM(status = 'andamento'), 0) AS andamento,
               COALESCE(SUM(status = 'concluida'), 0) AS concluida
        FROM tarefas WHERE usuario_id = ?
        """,
        (g.user["id"],),
    ).fetchone()
    total = row["total"] or 0
    return jsonify({**dict(row), "percentual": round((row["concluida"] / total) * 100) if total else 0})


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "FocusBoard", "version": "2.0"})

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG", "1") == "1")
