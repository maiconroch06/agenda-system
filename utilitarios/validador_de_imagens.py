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
        if (extensao.lower() != 'png' and extensao.lower()!='jpg' and extensao.lower()!='jpeg' and extensao != EnumNomesPastaImagem.IMAGEM_PADRAO.value):
            raise ImagemErrorExcecao("O sistema só aceita imagens em formato png ou jpg")
    
     
    @classmethod
    def extensao_foto_servico(cls, nome_imagem:str):
                                               
        if nome_imagem and nome_imagem.strip():
            # pega a extensao
            extensao = nome_imagem.split(".")
                      
            if len(extensao) == 2:
                return extensao[1]
                
        return EnumNomesPastaImagem.IMAGEM_PADRAO.value       
    
    @classmethod
    def nomeImagem(cls, nome_imagem, prefixo_nome_imagem):
       
        extensao_ou_default_imagem = cls.extensao_foto_servico(nome_imagem)  
        cls.imgem_extensao_valida(extensao_ou_default_imagem)
                        
        if extensao_ou_default_imagem != EnumNomesPastaImagem.IMAGEM_PADRAO.value:
            foto_nome = f"{prefixo_nome_imagem}_{int(time.time_ns())}.{extensao_ou_default_imagem}" 
            return foto_nome
        
        return extensao_ou_default_imagem
    
    # Função para salvar a imagem
    @classmethod
    def salvarImagem(cls, imagem, nomePasta, nome_imagem):
        # O nome pode ser criptografado, mas deixei assim para acompanhar as imagems enviadas
        # nesse caso ele esta pegando o tempo em nanoSegundos;
        
        extensao_ou_default_imagem = nome_imagem
        print(" DEFAULT IMGEM: " + imagem.filename + " - " + nomePasta.value + " - "+ extensao_ou_default_imagem) 
        try:
            if extensao_ou_default_imagem != EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                  
                # crio o caminho da pasta
                pasta = os.path.join(
                    current_app.root_path,
                    current_app.config['UPLOAD_FILES'] ,
                    nomePasta.value) 
                        
                # crio automaticamente a pasta caso não exista!
                os.makedirs(pasta,exist_ok=True)
                        
                #crio o caminho da pasta com o nome
                caminho = os.path.join(pasta, extensao_ou_default_imagem)
                        
                #salvo a imagem no caminho
                imagem.save(caminho)
                
                #se ocorrrer algum erro, dispara uma excecão
                
            return True 
            
        except (OSError, FileNotFoundError, IsADirectoryError):
            raise Exception("Error ao tentar salvar a imagem no servidor")


    # Função para editar uma imagem
    @classmethod
    def editarImagem(cls, nome_imagem_anterior: str, nova_imagem, nome_pasta:EnumNomesPastaImagem, imagem_padrao, prefixo_nome_imagem):    
        # Imagem nova
        if nova_imagem and nova_imagem.filename:
            # devolvo o nome, e valido extensão
            foto_nome =  cls.nomeImagem(secure_filename(nova_imagem.filename), prefixo_nome_imagem)
            
            #excluir a imagem anterior, desde que ela não seja a default
            if nome_imagem_anterior != EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                cls.excluir_imagem(nome_imagem_anterior, nome_pasta)

            cls.salvarImagem(nova_imagem, nome_pasta, foto_nome)
        
            return foto_nome
        
        # manter a mesma imagem
        elif not nova_imagem and not imagem_padrao: 
            return nome_imagem_anterior
        
        # Deixar o servico sem imagem
        else:
            #preciso remover a imagem associada caso exista
            if nome_imagem_anterior != EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                cls.excluir_imagem(nome_imagem_anterior, nome_pasta)

            return EnumNomesPastaImagem.IMAGEM_PADRAO.value

    # Função remover imagem
    @classmethod
    def excluir_imagem(cls, nome_da_imagem, nome_pasta):
        try:
            if nome_da_imagem!=EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                caminho_imagem = os.path.join(
                    current_app.root_path,
                    current_app.config['UPLOAD_FILES'] ,
                    nome_pasta.value, nome_da_imagem)
            
                if os.path.exists(caminho_imagem):
                    os.remove(caminho_imagem)

        except Exception as error:
            print(f"erro ao delatar a imagem{nome_da_imagem}, pois {error}")
            return False
       
           
        
