from flask import Flask 

from blueprints.auth.auth_bp import auth_bp
from blueprints.companies.companies_bp import companies_bp
from blueprints.customer.customer_bp import customer_bp
from blueprints.employee.employee_bp import employee_bp
from blueprints.public.public_bp import public_bp
from blueprints.register.register_bp import register_bp


app = Flask(__name__)

# Declarando modulos (onde vai ficar as rotas, logica de negocio e comunicação com o banco)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(companies_bp, url_prefix='/companies')
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(public_bp, url_prefix='/')
app.register_blueprint(register_bp, url_prefix='/register')


# @app.route("/login")
# def loginPage():
#     return render_template("all-authentication.html")

# @app.route("/cadastro-usuario")
# def singUpUser():
#     return render_template("user-register.html")

# @app.route("/cadastrar-endereco", methods=["POST"])
# def singUpAddress():
#     tipoEndereco = int(request.form["tipo-end"])
#     #tipoEndereco = request.form.get("tipo-end",type=int)
#     # Se idade não existir, retorna: None -> é uma busca opcional, diferente do anterior.
#     typepersona = ["Usuário", "Empresa"]

#     #esse modelo é um dicionário
#     estado_siglas =  {
#     "AC": "Acre",
#     "AL": "Alagoas",
#     "AP": "Amapá",
#     "AM": "Amazonas",
#     "BA": "Bahia",
#     "CE": "Ceará",
#     "DF": "Distrito Federal",
#     "ES": "Espírito Santo",
#     "GO": "Goiás",
#     "MA": "Maranhão",
#     "MT": "Mato Grosso",
#     "MS": "Mato Grosso do Sul",
#     "MG": "Minas Gerais",
#     "PA": "Pará",
#     "PB": "Paraíba",
#     "PR": "Paraná",
#     "PE": "Pernambuco",
#     "PI": "Piauí",
#     "RJ": "Rio de Janeiro",
#     "RN": "Rio Grande do Norte",
#     "RS": "Rio Grande do Sul",
#     "RO": "Rondônia",
#     "RR": "Roraima",
#     "SC": "Santa Catarina",
#     "SP": "São Paulo",
#     "SE": "Sergipe",
#     "TO": "Tocantins"
# }
#     #Esse formato seria uma lista;
#     #estados = [
#     #{"sigla": "AC", "nome": "Acre"},
#     #]
#     return render_template("adress-register.html", tipoEndereco=tipoEndereco, typepersona=typepersona[tipoEndereco], estado_siglas=estado_siglas)


# @app.route("/finalizar-cadastro-usuario", methods=["POST"])
# def finishRegister():
#        return render_template("finish-register.html")

# @app.route("/panel-categoria-do-usuario", methods=["POST","GET"])
# def userCategoryTypePanel():
#        return render_template("user-category-type-panel.html")

# @app.route("/cadastrar-empresa", methods=["POST","GET"])
# def singUpEnterprise():
#     categoriasEmpresas = ["Selecione uma categoria","Barbearia","Salão de beleza","Estética"]
#     return render_template("company-register.html", categoriasEmpresas=categoriasEmpresas)


# @app.route("/painel-Administrativo", methods=["POST"])
# def panelAdmin():
#        return render_template("painel-administrativo.html")



if __name__ == "__main__":
    app.run(debug=True)