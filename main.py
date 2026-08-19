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

    #esse modelo é um dicionário
    estado_siglas =  {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins"
}
    #Esse formato seria uma lista;
    #estados = [
    #{"sigla": "AC", "nome": "Acre"},
    #]
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