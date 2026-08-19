from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def homaPage():
    return render_template("homePage.html")


@app.route("/login")
def loginPage():
    return render_template("autenticacao.html")

@app.route("/cadastro_usuario")
def singUpUser():
    return render_template("cadastro_usuario.html")

@app.route("/cadastrar_endereco", methods=["POST"])
def singUpAddress():
    tipoEndereco = int(request.form["tipo-end"])
    #tipoEndereco = request.form.get("tipo-end",type=int)
    # Se idade não existir, retorna: None -> é uma busca opcional, diferente do anterior.
    typepersona = ["Proprietário", "Empresa"]
    estado_siglas = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF",
    "ES", "GO", "MA", "MT", "MS", "MG", "PA",
    "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
    "RO", "RR", "SC", "SP", "SE", "TO"
    ]
    return render_template("cadastrar_endereco.html", tipoEndereco=tipoEndereco, typepersona=typepersona[tipoEndereco], estado_siglas=estado_siglas)

@app.route("/cadastrar_empresa", methods=["POST"])
def singUpEnterprise():
    categoriasEmpresas = ["Selecione uma categoria","Barbearia","Salão de beleza","Estética"]
    return render_template("cadastroEmpresa.html", categoriasEmpresas=categoriasEmpresas)


@app.route("/painelAdministrativo", methods=["POST"])
def completeRegistration():
       return render_template("painelAdministrativo.html")



if __name__ == "__main__":
    app.run(debug=True)