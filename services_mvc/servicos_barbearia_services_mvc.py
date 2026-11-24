from repositorio import ServicoRepositorio
from models import Servico
from sqlalchemy.exc import IntegrityError
from enums import EnumNomesPastaImagem
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from utilitarios import ValidadorDeImagens
from werkzeug.utils import secure_filename
from flask import flash


class ServicoBarbearia:
    
    def __init__(self):
        self.__servico_repositorio = ServicoRepositorio()
        
    def consultar_todos_servicos(self):
        return self.__servico_repositorio.consultar_todos_servicos()
 
    def consultar_servico_nome(self, nome_servico):
        return self.__servico_repositorio.consultar_servico_nome(nome_servico)
    
    def consultar_descricoes_servico(self):
        return self.__servico_repositorio.consultar_descricoes_servico()
    
    def consultar_todos_servicos_resumo(self):
        return self.__servico_repositorio.consultar_todos_os_servicos_resumo()
    
    def cadastrar_servico_barbearia(self, foto_servico, novo_descricao, novo_valor, novo_duracao):
        
        try:
                    
            servico = Servico(
                foto_servico=EnumNomesPastaImagem.IMAGEM_PADRAO.value,
                descricao_servico=novo_descricao,
                valor= Decimal(novo_valor or -1),
                duracao= int(novo_duracao or -1),
                status_servico=True,
                data_cadastro=datetime.now(),
                data_atualizacao= datetime.now()  
            )
            #validar campos com o especialista
            servico.validarValoresVazios()
            servico.validarValorDuracao()
            
            #salvar a imagem na pasta
            #extensão | validar extensao | pegar o novo nome da imagem
            
            servico.foto_servico = ValidadorDeImagens.nomeImagem(secure_filename(foto_servico.filename), "servicos") 
            
            resposta_repositorio = self.__servico_repositorio.cadastrar_servico(servico)
            
            ValidadorDeImagens.salvarImagem(foto_servico, EnumNomesPastaImagem.IMAGEMS_SERVICOS, servico.foto_servico)
            
            return resposta_repositorio
            
        except IntegrityError as error:
            raise Exception("Erro ao cadastrar o serviço!")
            
        except (ValueError, TypeError, InvalidOperation):
            raise Exception("Campos duração e valor só aceitam números.")
        
        
    def editar_servico_barbearia(self, id, imagem_form, img_padrao, imagem_anterior, descricao_servico, valor, duracao, ativo):
        
        try:
            id_servico = int(id)
            status_ativo = int(ativo)
            
            servico = Servico(
                id_servico=id_servico,
                descricao_servico=descricao_servico,
                valor=Decimal(valor),
                duracao=int(duracao),
                data_atualizacao=datetime.now(timezone.utc),
                status_servico=status_ativo  
            )
            
            servico.foto_servico = ValidadorDeImagens.editarImagem(imagem_anterior,imagem_form,EnumNomesPastaImagem.IMAGEMS_SERVICOS, img_padrao, "servicos")
            
            if not self.__servico_repositorio.atualizar(servico):
                raise Exception("Error ao tentar atualizar o serviço, tente novamente!")
             
        except (IntegrityError, ValueError, TypeError, ArithmeticError) :
            raise Exception("Os campos Preço e duração só aceitam números!")
        
        
    def excluir_servico_barbearia(self, id_servico, foto_nome):
        if self.__servico_repositorio.excluir(id_servico):
            ValidadorDeImagens.excluir_imagem(foto_nome, EnumNomesPastaImagem.IMAGEMS_SERVICOS)
            return
        
        raise Exception("O serviço não foi excluido.")

    def consultar_todos_servicos(self):
            return self.__servico_repositorio.consultar_todos_servicos()
    
    def listar_servicos_ativos(self):
        return self.__servico_repositorio.listar_ativos()

    def buscar_servico_id(self, id_servico):
        return self.__servico_repositorio.buscar_por_id(id_servico)
           
        
        
        
    