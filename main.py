from flask import Flask, render_template

app = Flask(__name__)

# Tela 1: Página Inicial
@app.route("/")
def homaPage():
    return render_template("homePage.html")

# Tela 2: Autenticação / Login
@app.route('/autenticacao')
def autenticacao():
    return render_template('autenticacao.html')

# Tela 3: Meus Agendamentos
@app.route('/agendamentos')
def agendamentos():
    return render_template('agendamentos.html')

# Tela 3: Meus Agendamentos
@app.route('/agendamentos')
def agendamentos():
    return render_template('agendamentos.html')

# Tela 3: Meus Agendamentos
@app.route('/agendamentos')
def agendamentos():
    return render_template('agendamentos.html')

# Tela 3: Meus Agendamentos
@app.route('/agendamentos')
def agendamentos():
    return render_template('agendamentos.html')

# Tela 3: Meus Agendamentos
@app.route('/agendamentos')
def agendamentos():
    return render_template('agendamentos.html')

if __name__ == "__main__":
    app.run(debug=True)
