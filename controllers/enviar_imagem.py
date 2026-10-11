from flask import current_app, flash, redirect, url_for
from enums import EnumStatusMensagens, EnumNomesPastaImagem
import time
import os
from werkzeug.utils import secure_filename

class EnviarImagem:
    
    @staticmethod
    def enviarImagem(imagem, nomePasta:EnumNomesPastaImagem):
        
        foto_nome = 'default.png'
            
        if imagem and imagem.filename:
            # pega a extensao
            imagemTemp = secure_filename(imagem.filename)
            extensao = os.path.splitext(imagemTemp)[1]
        
            # valida a imagem
            if (extensao != '.png' and extensao!='.jpg' and extensao!='.jpeg'):
                flash("O sistema só aceita imagens em formato png ou jpg", EnumStatusMensagens.AVISO.value)
                foto_nome=None
                return foto_nome
             
            # O nome pode ser criptografado, mas deixei assim para acompanhar as imagems enviadas
            # nesse caso ele esta pegando o tempo em millisegundos;
            foto_nome = f"{int(time.time() * 1000 )}{extensao}"
        
            # crio o caminho da pasta
            pasta = os.path.join(
                current_app.root_path,
                current_app.config['UPLOAD_FILES'] ,
                nomePasta.value) 
        
            # crio a pasta e caso não exista eu crio automaticamente
            os.makedirs(pasta,exist_ok=True)
        
            #crio o caminho da pasta com o nome
            caminho = os.path.join(pasta, foto_nome)
        
            #salvo a imagem no caminho
            imagem.save(caminho)

        return foto_nome