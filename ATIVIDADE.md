# Atividade Aula 11 — Cenário MVC completo (vale **1,0 ponto**)

## O que vocês vão fazer

1. Escolher **um** cenário (A, B ou C)
2. Copiar os arquivos da pasta `cenarios/` para as pastas corretas da **Aula 11**
3. Completar **Model + Controller + View** (tem `TODO ALUNO` em tudo)
4. Registrar o Blueprint no `app.py` e link no `layout.html`

Leia também: **`COMO_MONTAR.md`**

---

## Cenários

| Código | Pasta | Tema |
|--------|-------|------|
| **A** | `cenarios/A_locadora/` | Locadora de veículos |
| **B** | `cenarios/B_cinema/` | Cinema / sessões |
| **C** | `cenarios/C_figurinhas/` | Troca de figurinhas Copa |

Cada pasta tem:

```
models/          → classes do banco (completar FK, relationship)
controllers/     → rotas Flask (Blueprint)
views/templates/ → HTML + Jinja2
app_registro_EXEMPLO.py  → o que colar no app.py
```

---

## Para onde copiar (Aula 11)

| Origem (cenário) | Destino (projeto) |
|------------------|-------------------|
| `models/*.py` | `flask/Aula11/models/` |
| `controllers/*_controller.py` | `flask/Aula11/controllers/` |
| `views/templates/cenario/` | `flask/Aula11/views/templates/` |

Atualize também:

- `models/__init__.py` (veja `__init___EXEMPLO.txt` do cenário)
- `controllers/__init__.py` (importe seu Blueprint)
- `app.py` (register_blueprint)
- `views/templates/layout.html` (link no menu)

---

## Critérios de avaliação (1,0 pt)

| Item | Peso |
|------|------|
| `ModeloBase` + 3 tabelas com FK corretas | 0,35 |
| Controller: listar + cadastrar funcionando | 0,35 |
| View: Jinja (`for`, `if`, `url_for`) corretos | 0,20 |
| Projeto roda sem erro + Blueprint registrado | 0,10 |

---

## Cenário A — Locadora

**Tabelas:** ClienteLocadora, Veiculo, Locacao (2 FKs)  
**Telas:** lista de locações + formulário nova locação  
**URL:** `/locadora/`

---

## Cenário B — Cinema

**Tabelas:** Filme, Sala, Sessao (+ Ingresso opcional)  
**Telas:** programação de sessões + cadastrar sessão  
**URL:** `/cinema/`

---

## Cenário C — Figurinhas

**Tabelas:** Colecionador, Figurinha, OfertaTroca, ItemOferta  
**Telas:** mural de ofertas + nova oferta de troca  
**URL:** `/figurinhas/`

---

## Entrega

- Repositório / pasta com Aula 11 modificada **ou**
- Print do navegador + arquivos `.py` e `.html` corrigidos

No topo de um arquivo, comente:

```python
# Cenário: B - Cinema
# Aluno: Seu Nome
```

---

## Dica da profe

Comece pelo **Model** (banco), depois **Controller** (rotas), por último **View** (HTML).  
Se der erro, leia o terminal — ele quase sempre diz qual arquivo está faltando.

Boa sorte!
