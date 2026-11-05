from flask import current_app, flash
from enums import EnumNomesPastaImagem
import time
import os
from werkzeug.utils import secure_filename
from execoes import ImagemErrorExcecao

class ValidadorDeImagens:

    # Função verifica a extensão do arquivo
    @classmethod
    def imgem_extensao_valida(cls, extensao:str):
        # valida a imagem
        if (extensao != '.png' and extensao!='.jpg' and extensao!='.jpeg' and extensao != EnumNomesPastaImagem.IMAGEM_PADRAO.value):
            raise ImagemErrorExcecao("O sistema só aceita imagens em formato png ou jpg")
    
    @classmethod
    def extensao_foto_servico(cls, imagem):
                                           
        if imagem and imagem.filename:
            # pega a extensao
            imagemTemp = secure_filename(imagem.filename)
            extensao = os.path.splitext(imagemTemp)[1]
            return extensao
            
        return EnumNomesPastaImagem.IMAGEM_PADRAO.value        
    
    
    
    # Função para salvar a imagem
    @classmethod
    def salvarImagem(cls, imagem, nomePasta):
        # O nome pode ser criptografado, mas deixei assim para acompanhar as imagems enviadas
        # nesse caso ele esta pegando o tempo em nanoSegundos;
        
        extensao_ou_default_imagem = cls.extensao_foto_servico(imagem)
        cls.imgem_extensao_valida(extensao_ou_default_imagem) 
        
        try:
            if extensao_ou_default_imagem != EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                foto_nome = f"servicos_{int(time.time_ns())}{extensao_ou_default_imagem}"        
                # crio o caminho da pasta
                pasta = os.path.join(
                    current_app.root_path,
                    current_app.config['UPLOAD_FILES'] ,
                    nomePasta.value) 
                        
                # crio automaticamente a pasta caso não exista!
                os.makedirs(pasta,exist_ok=True)
                        
                #crio o caminho da pasta com o nome
                caminho = os.path.join(pasta, foto_nome)
                        
                #salvo a imagem no caminho
                imagem.save(caminho)
                
                return foto_nome

            return extensao_ou_default_imagem
        
        except (OSError, FileNotFoundError, IsADirectoryError):
            raise Exception("Error ao tentar salvar a imagem no servidor")


    # Função para editar uma imagem
    @classmethod
    def editarImagem(cls, nome_imagem_anterior: str, nova_imagem, nome_pasta:EnumNomesPastaImagem, imagem_padrao): 
        # Imagem nova
        if nova_imagem and nova_imagem.filename:
            imagemTemp = secure_filename(nova_imagem.filename)
            extensao = os.path.splitext(imagemTemp)[1]
                
            cls.imgem_extensao_valida(extensao) 
               
            #excluir a imagem anterior, desde que ela não seja a default
            if nome_imagem_anterior != EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                cls.removerImagem(nome_imagem_anterior, nome_pasta)

            return cls.salvarImagem(nova_imagem, nome_pasta)

        # manter a mesma imagem
        elif not nova_imagem and not imagem_padrao: 
            return nome_imagem_anterior
        
        # Deixar o produto sem imagem
        else:
            #preciso remover a imagem associada caso exista
            if nome_imagem_anterior != EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                cls.removerImagem(nome_imagem_anterior, nome_pasta)

            return EnumNomesPastaImagem.IMAGEM_PADRAO.value

    # Função remover imagem
    @classmethod
    def removerImagem(cls, nome_da_imagem, nome_pasta):
        try:
            if nome_da_imagem!=EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                caminho_imagem = os.path.join(
                    current_app.root_path,
                    current_app.config['UPLOAD_FILES'] ,
                    nome_pasta.value, nome_da_imagem)
            
                if os.path.exists(caminho_imagem):
                    os.remove(caminho_imagem)

        except Exception as error:
            print(f"erro ao delatar a imagem {error}")
            return False
       
           
        
