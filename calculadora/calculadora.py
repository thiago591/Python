import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calcular():
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operacao = request.form['operacao']
        
        resultado = 0
        etapas = ""

        
        if operacao == '+':
            resultado = num1 + num2
            etapas = f'{num1} + {num2} = {resultado}'
        elif operacao == '-':
            resultado = num1 - num2
            etapas = f'{num1} - {num2} = {resultado}'
        elif operacao == '*':
            resultado = num1 * num2
            etapas = f'{num1} * {num2} = {resultado}'
        elif operacao == '/':
            if num2 != 0:
                resultado = num1 / num2
                etapas = f'{num1} * {num2} = {resultado}'
            else:
                etapas = "Erro: Divisão por zero!"
                resultado = None

        return render_template('index.html', etapas=etapas, resultado=resultado)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
