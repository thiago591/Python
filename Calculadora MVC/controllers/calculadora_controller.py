import math

from flask import Blueprint, render_template, request

from models import Operacao

calculadora_bp = Blueprint("calculadora", __name__)


@calculadora_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return _calcular()
    return render_template(
        "calculadora.html",
        etapas="",
        resultados="",
        historico=Operacao.listar_recentes(),
    )


def _calcular():
    """Controller — lê o formulário, calcula e pede ao Model para salvar."""
    num1 = float(request.form["num1"])
    operacao = request.form["operacao"]
    num2 = None
    etapas = ""
    resultado = ""

    if operacao == "sqrt":
        if num1 < 0:
            resultado = "Erro: número negativo"
            etapas = f"Não existe raiz real de {num1}."
        else:
            resultado = math.sqrt(num1)
            etapas = f"√{num1} = {resultado}"
    else:
        num2_valor = request.form.get("num2", "").strip()
        if not num2_valor:
            return render_template(
                "calculadora.html",
                etapas="Informe o segundo número para esta operação.",
                resultados="",
                historico=Operacao.listar_recentes(),
            )
        num2 = float(num2_valor)

        if operacao == "+":
            resultado = num1 + num2
            etapas = f"{num1} + {num2} = {resultado}"
        elif operacao == "-":
            resultado = num1 - num2
            etapas = f"{num1} - {num2} = {resultado}"
        elif operacao == "*":
            resultado = num1 * num2
            etapas = f"{num1} * {num2} = {resultado}"
        elif operacao == "/":
            if num2 != 0:
                resultado = num1 / num2
                etapas = f"{num1} / {num2} = {resultado}"
            else:
                resultado = "Erro: Divisão por zero"
                etapas = "Não é possível dividir por zero."
        elif operacao == "**":
            resultado = num1 ** num2
            etapas = f"{num1} ** {num2} = {resultado}"
        else:
            resultado = "Operação inválida"
            etapas = "A operação selecionada é inválida."

    Operacao.salvar(num1, num2, operacao, etapas, resultado)

    return render_template(
        "calculadora.html",
        etapas=etapas,
        resultados=resultado,
        historico=Operacao.listar_recentes(),
    )