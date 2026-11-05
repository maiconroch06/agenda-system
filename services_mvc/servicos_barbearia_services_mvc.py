from repositorio import ServicoRepositorio
from models import Servico
from sqlalchemy.exc import IntegrityError
from enums import EnumNomesPastaImagem
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from utilitarios import ValidadorDeImagens


class ServicoBarbearia:
    
    def __init__(self):
        self.servico_repositorio = ServicoRepositorio()
        
    def consultar_todos_servicos(self):
        return self.servico_repositorio.consultar_todos_servicos()
    
    def cadastrar_servico_barbearia(self, foto_servico, novo_descricao, novo_valor, novo_duracao):
        
        try:
            servico = Servico(
                id = -1,
                foto_nome=EnumNomesPastaImagem.IMAGEM_PADRAO.value,
                descricao=novo_descricao,
                valor= Decimal(novo_valor or -1),
                duracao= int(novo_duracao or -1),
                status_servico=1,
                data_cadastro=datetime.now(timezone.utc),
                data_atualizacao= datetime.now(timezone.utc)  
            )
            
            #validar campos com o especialista
            servico.valoresVazios()
            servico.valoresValidos()
            
            #salvar a imagem na pasta
            #extensão | validar extensao | pegar o novo nome da imagem
            extensao = ValidadorDeImagens.extensao_foto_servico(foto_servico)
            ValidadorDeImagens.imgem_extensao_valida(extensao)
            servico.foto_nome = ValidadorDeImagens.salvarImagem(foto_servico, EnumNomesPastaImagem.IMAGEMS_SERVICOS, extensao)
            
            self.servico_repositorio.cadastrar_servico(servico)
            
        except IntegrityError as error:
            raise Exception("Erro ao cadastrar o serviço!")
            
        except (ValueError, TypeError, InvalidOperation):
            raise Exception("Campos duração e valor só aceitam números.")
        
        
        
        
        
        
        
        
    