from repositorio import BarbeariaRepositorio


class BarbeariaService():
        
    @staticmethod
    def consultar_cnpj_barbearia():
        return BarbeariaRepositorio.buscar_cnpj()
       