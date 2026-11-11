import re
from flask import flash

def processar_e_validar_cadastro(dados_formulario):
    """
    Recebe os dados brutos do formulário, valida e retorna
    um dicionário com o resultado e os dados limpos ou erros.
    """
    nome = dados_formulario.get("cad-nome", "").strip()
    email = dados_formulario.get("cad-email", "").strip()
    senha = dados_formulario.get("cad-senha", "")
    confirmar = dados_formulario.get("cad-confirmar", "")

    erros = {}

    # Validações
    if len(nome) < 3:
        erros["cad-nome"] = "Nome deve ter ao menos 3 caracteres"

    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        erros["cad-email"] = "Informe um e-mail válido"

    if len(senha) < 6:
        erros["cad-senha"] = "Senha deve ter ao menos 6 caracteres"

    if senha != confirmar or not confirmar:
        erros["cad-confirmar"] = "As senhas não coincidem"

    # Se houver erros, dispara os flashes e retorna falso
    if erros:
        for campo, mensagem in erros.items():
            flash(mensagem, campo)
        return {"sucesso": False, "usuario": None}

    # Se passar na validação, retorna sucesso e o dicionário pronto
    usuario_valido = {
        "nome": nome,
        "email": email,
        "senha": senha
    }
    return {"sucesso": True, "usuario": usuario_valido}
