from models.Endereco import Endereco
from models.Barbearia import Barbearia
from models.Usuario import Usuario
from models.gestor import Gestor

def initialize():
    
    try:
        id_endereco = Endereco.inserirEnderecoPadrao() 
        cnpj = Barbearia.inserirBarbeariaPadrao(id_gestor,id_endereco) 
        id_usuario = Usuario.inserirUsuarioGestor(id_endereco)
        Gestor.inserirGestor(id_usuario,cnpj )
    except Exception as erro :
        print(erro + " Erro ao tentar se comunicar com o banco de dados")