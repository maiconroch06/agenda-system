
from DAO.barbeiro_dao import BarbeiroDAO


class BarbeiroRepositorio:
    
    def __init__(self):
        self.__barbeiroDao = BarbeiroDAO()
        
    def realizar_login(self, email):
        return self.__barbeiroDao.realizar_login_dao(email)
    
    def salvar(self, barbeiro):
        return self.__barbeiroDao.cadastrar(barbeiro)

    
    def buscar_por_id(self, id_barbeiro):
        return self.__barbeiroDao.buscar_por_id(id_barbeiro)

    
    def listar_todos(self):
        return self.__barbeiroDao.consultar_todos()
    
    def consultar_barbeiro_nome(self, nome_barbeiro):
        return self.__barbeiroDao.consultar_barbeiro_nome(nome_barbeiro)

    def listar_todos_ativos(self):
        return self.__barbeiroDao.consultar_todos_ativos()
    
    def listar_agendamentos_barbeiro(self, id_barbeiro):
        return self.__barbeiroDao.consultar_agendamentos_barbeiro(id_barbeiro)
    
    def atualizar(self, barbeiro):
        return self.__barbeiroDao.atualizar_informacoes_barbeiro(barbeiro)

    def consultar_faltas_por_barbeiro_ativo(self):
        return self.__barbeiroDao.consultar_faltas_dos_barbeiros_ativo()
    
    def consultar_faltas_mensais_barbeiros_ativo(self, data_inicio_mes, data_final_mes):
        return self.__barbeiroDao.consultar_faltas_mensais_barbeiros_ativo( data_inicio_mes, data_final_mes)
        
    def atualizar_status_agendamento(self, id_agendamento, status_agendamento, data_hoje):
        return self.__barbeiroDao.atualizar_status_agendamento(id_agendamento, status_agendamento, data_hoje)
    
    def atualizar_status_agendamento(self, id_agendamento, status_agendamento, data_hoje, motivo_cancelamento):
        return self.__barbeiroDao.atualizar_status_agendamento(id_agendamento, status_agendamento, data_hoje, motivo_cancelamento)