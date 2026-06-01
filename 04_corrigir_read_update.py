def listar_alunos():
    """READ — retorna todos os alunos ordenados por nome."""
    
    return Aluno.query.order_by(Aluno.nome).all()


def buscar_aluno(aluno_id):
    """READ — busca um aluno pelo id."""
 
    return db.session.get(Aluno, aluno_id)


def atualizar_aluno(aluno_id, novo_nome, novo_email):
    """UPDATE — altera nome e e-mail."""
    aluno = buscar_aluno(aluno_id)
    if not aluno:
        return False

    aluno.nome = novo_nome
    aluno.email = novo_email

  
    db.session.commit()

    return True
