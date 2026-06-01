from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alunos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)  


with app.app_context():
    db.create_all()


@app.route('/')
def lista():
    
    alunos = Aluno.query.order_by(Aluno.id.desc()).all()
    
    total_alunos = len(alunos) 
    return render_template('lista.html', alunos=alunos, total_alunos=total_alunos)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone'] 
        
        novo_aluno = Aluno(nome=nome, email=email, telefone=telefone)
        db.session.add(novo_aluno)
        db.session.commit()
        return redirect(url_for('lista'))
    return render_template('formulario.html', aluno=None)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    aluno = Aluno.query.get_or_404(id)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.email = request.form['email']
        aluno.telefone = request.form['telefone'] 
        db.session.commit()
        return redirect(url_for('lista'))
    return render_template('formulario.html', aluno=aluno)


@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('lista'))

if __name__ == '__main__':
    app.run(debug=True)
