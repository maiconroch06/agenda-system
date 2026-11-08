import re
import os

from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

from database import db
from datetime import datetime, timezone

from models.usuarios import Usuario
from models.endereco import Endereco
from models.barbeiros import Barbeiro
from enums import EnumStatusMensagens
from services_mvc import BarbeiroService


class ControladorBarbeiro:

    __barbeiroService = BarbeiroService()

    @classmethod
    def consultar_todos_barbeiros(cls):
        return render_template('pages/gestor/gestor-painel-barbeiros-rp.html', barbeiros = cls.__barbeiroService.consultar_barbeiros(), mensagens_status=EnumStatusMensagens)

    @classmethod
    def atualizar_endereco_barbeiro(cls, endereco):
        try:
            cls.__barbeiroService.atualizar_endereco(endereco)
            flash("Endereço alterado com sucesso", EnumStatusMensagens.SUCESSO.value)
        except Exception:
            flash("Não foi possivel alterar o endeceço, contate o suporte", EnumStatusMensagens.AVISO.value)
        
        return redirect(url_for('gestor.gestorAbaBarbeiros'))    
    