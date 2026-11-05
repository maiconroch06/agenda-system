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
            
            servico.foto_nome = ValidadorDeImagens.salvarImagem(foto_servico, EnumNomesPastaImagem.IMAGEMS_SERVICOS)
            
            self.servico_repositorio.cadastrar_servico(servico)
            
        except IntegrityError as error:
            raise Exception("Erro ao cadastrar o serviço!")
            
        except (ValueError, TypeError, InvalidOperation):
            raise Exception("Campos duração e valor só aceitam números.")
        
        
    def editar_servico_barbearia(self, id, imagem_form, img_padrao, imagem_anterior, descricao_servico, valor, duracao, ativo):
        
        try:
            id_servico = int(id)
            status_ativo = int(ativo)
            
            servico = Servico(
                id=id_servico,
                descricao=descricao_servico,
                valor=Decimal(valor),
                duracao=int(duracao),
                data_atualizacao=datetime.now(timezone.utc),
                status_servico=status_ativo  
            )
            
            servico.foto_nome = ValidadorDeImagens.editarImagem(imagem_anterior,imagem_form,EnumNomesPastaImagem.IMAGEMS_SERVICOS, img_padrao)
            
            if not self.servico_repositorio.atualizar(servico):
                raise Exception("Error ao tentar atualizar o serviço, tente novamente!")
             
        except (IntegrityError, ValueError, TypeError, ArithmeticError) :
            raise Exception("Os campos Preço e duração só aceitam números!")
        
        
    def excluir_servico_barbearia(self, id_servico):
        if self.servico_repositorio.excluir(id_servico):
            return
        
        raise Exception("O serviço não foi excluido.")
           
        
        
        
    