from flask import current_app, flash
from enums import EnumStatusMensagens, EnumNomesPastaImagem
import time
import os
from werkzeug.utils import secure_filename

class ControladorDeImagens:

    # Função verifica a extensão do arquivo
    def imgemGExtensaoValida(self, extensao:str):
        # valida a imagem
        if (extensao != '.png' and extensao!='.jpg' and extensao!='.jpeg'):
            flash("O sistema só aceita imagens em formato png ou jpg", EnumStatusMensagens.AVISO.value)
            return False
        
        return True
    # Função para salvar a imagem
    def salvarImagem(self, imagem, nomePasta, extensao):
        # O nome pode ser criptografado, mas deixei assim para acompanhar as imagems enviadas
        # nesse caso ele esta pegando o tempo em nanoSegundos;
        try:
            foto_nome = f"servicos_{int(time.time_ns())}{extensao}"
                    
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
        
        except (OSError, FileNotFoundError, IsADirectoryError) as error:
            print(f"Ocorreu o error: {error}")
            flash("Error ao tentar salvar a imagem no servidor")
            return  EnumNomesPastaImagem.IMAGEM_PADRAO.value

    
    # Função para validar a imagem e enviar
    def enviarImagem(self, imagem, nomePasta:EnumNomesPastaImagem):
        
        foto_nome = EnumNomesPastaImagem.IMAGEM_PADRAO.value
                    
        if imagem and imagem.filename:
            # pega a extensao
            imagemTemp = secure_filename(imagem.filename)
            extensao = os.path.splitext(imagemTemp)[1]

            if self.imgemGExtensaoValida(extensao) is False:
                return None

            foto_nome = self.salvarImagem(imagem, nomePasta, extensao)

        return foto_nome

    # Função para editar uma imagem
    def editarImagem(self, nome_imagem_anterior: str, nova_imagem, nome_pasta:EnumNomesPastaImagem, imagem_padrao): 
        # Imagem nova
        if nova_imagem and nova_imagem.filename:
            imagemTemp = secure_filename(nova_imagem.filename)
            extensao = os.path.splitext(imagemTemp)[1]
                
            if self.imgemGExtensaoValida(extensao) is None:
                return None 

            #excluir a imagem anterior, desde que ela não seja a default
            if nome_imagem_anterior != EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                self.removerImagem(nome_imagem_anterior, nome_pasta)

            return self.salvarImagem(nova_imagem, nome_pasta, extensao)

        # manter a mesma imagem
        elif not nova_imagem and not imagem_padrao: 
            return nome_imagem_anterior
        
        # Deixar o produto sem imagem
        else:
            #preciso remover a imagem associada caso exista
            if nome_imagem_anterior != EnumNomesPastaImagem.IMAGEM_PADRAO.value:
                self.removerImagem(nome_imagem_anterior, nome_pasta)

            return EnumNomesPastaImagem.IMAGEM_PADRAO.value

   # Função remover imagem
    def removerImagem(self, nome_da_imagem, nome_pasta):
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
       
           
        
