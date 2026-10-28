from datetime import datetime
class BarbeiroHasServicos:

    def __init__(
        self,
        id_servico: int,
        id_barbeiro: int,
        data_cadastro: datetime
    ):
        self.id_servico = id_servico
        self.id_barbeiro = id_barbeiro
        self.data_cadastro = data_cadastro

    def consultarIdServico(self):
        return self.id_servico

    def consultarIdBarbeiro(self):
        return self.id_barbeiro

    def consultarDataCadastro(self):
        return self.data_cadastro

    def atualizarDataCadastro(self, data: datetime):
        self.data_cadastro = data

    def __str__(self):
        return (
            f"BarbeiroHasServicos("
            f"id_servico={self.id_servico}, "
            f"id_barbeiro={self.id_barbeiro}, "
            f"data_cadastro={self.data_cadastro})"
        )
