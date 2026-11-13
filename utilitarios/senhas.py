from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash

class Senha():
    @staticmethod    
    def validar_senha(senha_usuario, senha_informada):
        if not check_password_hash(senha_usuario, senha_informada):
            raise Exception("Senha invalida, tente novamente!")
            
    @staticmethod
    def gerar_senha(senha):
        return generate_password_hash(senha)