from models.endereco import Endereco
from models.barbearia import Barbearia
from models.usuarios import Usuario
from models.gestor import Gestor
from models.estados import Estados
from database import db

def initialize():
        try:
            id_endereco=0;
            cnpj_barbearia=None;

            if (Estados.inserirEstadosDefault() == 1):
                id_endereco = Endereco.inserirEnderecoPadrao()
              
                if (id_endereco != 0):
                    cnpj_barbearia = Barbearia.inserirBarbeariaPadrao(id_endereco)
                    id_gestor = Usuario.inserirUsuarioGestor(id_endereco)

                    if (cnpj_barbearia is not None and id_gestor > 0):
                        Gestor.inserirGestor(id_gestor,cnpj_barbearia)

            db.session.commit() # aplica todas os transações
                 
        except Exception as erro :
            db.session.rollback() # Desfaz tudo (as transações) caso ocorra algum erro.
            print(f"{erro} - Erro ao tentar se comunicar com o banco de dados")
            raise