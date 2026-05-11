from flask import Flask 
app = Flask(__name__) @app.route('/decorator') 
def decorator(): return """ <h1>O que é um Decorator em Python?</h1> <p><b>O que é:</b> Um decorator é uma função que recebe outra função como argumento para estender ou modificar seu comportamento sem alterá-la permanentemente.</p> <p><b>Para que serve:</b> Serve para evitar repetição de código (DRY), sendo comum em logs, autenticação e, no caso do Flask, para definir rotas.</p> <p><b>Uso no Flask:</b> O <code>@app.route</code> é um decorator que diz ao Flask qual URL deve disparar a função logo abaixo dele.</p> """ 
if __name__ == '__main__': app.run(debug=True)

