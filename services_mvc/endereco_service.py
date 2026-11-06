from repositorio import EnderecoRepositorio
from models import Endereco

class EnderecoService:

    __endereco_repositorio = EnderecoRepositorio()

    @classmethod
    def cadastrar_endereco(cls, endereco: Endereco):
        if(endereco is not None):
            endereco.id = cls.__endereco_repositorio.salvar(endereco)
            return endereco
            
