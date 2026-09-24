from models.Endereco import Endereco
from models.Barbearia import Barbearia
from models.Usuario import Usuario

def initialize():
    
    try:
        id_endereco = Endereco.inserirEnderecoPadrao()
        id_gestor = Usuario.inserirUsuarioGestor(id_endereco)
        Barbearia.inserirBarbeariaPadrao(id_gestor,id_endereco) 
    except Exception as erro :
        print(erro + " Erro ao tentar se comunicar com o banco de dados")