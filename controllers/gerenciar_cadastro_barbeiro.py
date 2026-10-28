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


class ValidarBarbeiro:

    @staticmethod
    def validarFormularioCriarEditarBarbeiro(request, rota_erro: str, rota_certa: str, id_barbeiro:int):

        try:
            # ==========================================================
            # 1. COLETA DOS DADOS
            # ==========================================================

            foto = request.files.get("foto")

            cpf = request.form.get("cpf", "").strip()
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip()
            senha = request.form.get("senha", "")
            confirmaSenha = request.form.get("confirmar-senha", "")
            telefone = request.form.get("telefone", "").strip()
            descricao = request.form.get("descricao", "").strip()

            cep = request.form.get("cep", "").strip()
            cidade = request.form.get("cidade", "").strip()
            uf = request.form.get("unidade-federativa", "").strip().upper()
            bairro = request.form.get("bairro", "").strip()
            logradouro = request.form.get("logradouro", "").strip()
            numero = request.form.get("numero", "").strip()
            complemento = request.form.get("complemento", "").strip()

            sequencia = request.form.get("sequencia", "").strip()

            erros = {}

            # ==========================================================
            # 2. CAMPOS OBRIGATÓRIOS
            # ==========================================================

            campos_obrigatorios = {
                "cpf": cpf,
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "senha": senha,
                "confirmaSenha": confirmaSenha,
                "cep": cep,
                "cidade": cidade,
                "uf": uf,
                "bairro": bairro,
                "logradouro": logradouro,
                "numero": numero
            }

            for campo, valor in campos_obrigatorios.items():

                if not valor or str(valor).strip() == "":
                    erros[campo] = "Este campo é obrigatório."

            # ==========================================================
            # 3. LIMPEZA DOS CAMPOS NUMÉRICOS
            # ==========================================================

            cpf_limpo = re.sub(r"\D", "", cpf)
            telefone_limpo = re.sub(r"\D", "", telefone)
            cep_limpo = re.sub(r"\D", "", cep)

            # ==========================================================
            # 4. VALIDAÇÃO DO CPF
            # ==========================================================

            if cpf:

                if len(cpf_limpo) != 11:
                    erros["cpf"] = "O CPF deve conter exatamente 11 dígitos."

                elif cpf_limpo == cpf_limpo[0] * 11:
                    erros["cpf"] = "Informe um CPF válido."

                else:

                    # Primeiro dígito verificador
                    soma = sum(
                        int(cpf_limpo[i]) * (10 - i)
                        for i in range(9)
                    )

                    resto = soma % 11

                    digito1 = 0 if resto < 2 else 11 - resto

                    # Segundo dígito verificador
                    soma = sum(
                        int(cpf_limpo[i]) * (11 - i)
                        for i in range(10)
                    )

                    resto = soma % 11

                    digito2 = 0 if resto < 2 else 11 - resto

                    if (
                        int(cpf_limpo[9]) != digito1
                        or int(cpf_limpo[10]) != digito2
                    ):
                        erros["cpf"] = "Informe um CPF válido."

            # ==========================================================
            # 5. VALIDAÇÃO DO NOME
            # ==========================================================

            if nome:

                if len(nome) < 3:
                    erros["nome"] = "O nome deve ter pelo menos 3 caracteres."

                elif not re.match(
                    r"^[A-Za-zÀ-ÿ\s]+$",
                    nome
                ):
                    erros["nome"] = (
                        "O nome deve conter apenas letras e espaços."
                    )

            # ==========================================================
            # 6. VALIDAÇÃO DO E-MAIL
            # ==========================================================

            if email:

                regex_email = (
                    r"^[A-Za-z0-9._%+-]+"
                    r"@[A-Za-z0-9.-]+"
                    r"\.[A-Za-z]{2,}$"
                )

                if not re.match(regex_email, email):
                    erros["email"] = "Insira um endereço de e-mail válido."

            # ==========================================================
            # 7. VALIDAÇÃO DO TELEFONE
            # ==========================================================

            if telefone:

                if len(telefone_limpo) not in (10, 11):
                    erros["telefone"] = (
                        "O telefone deve conter DDD e possuir "
                        "10 ou 11 dígitos."
                    )

            # ==========================================================
            # 8. VALIDAÇÃO DA SENHA
            # ==========================================================

            if senha:

                if len(senha) < 6:
                    erros["senha"] = (
                        "A senha deve ter no mínimo 6 caracteres."
                    )

                elif len(senha) > 50:
                    erros["senha"] = (
                        "A senha deve ter no máximo 50 caracteres."
                    )

            # ==========================================================
            # 9. CONFIRMAÇÃO DA SENHA
            # ==========================================================

            if confirmaSenha:

                if senha != confirmaSenha:
                    erros["confirmaSenha"] = (
                        "A senha e a confirmação de senha não coincidem."
                    )

            # ==========================================================
            # 10. VALIDAÇÃO DO CEP
            # ==========================================================

            if cep:

                if len(cep_limpo) != 8:
                    erros["cep"] = (
                        "O CEP deve conter exatamente 8 dígitos."
                    )

            # ==========================================================
            # 11. VALIDAÇÃO DA UF
            # ==========================================================

            estados_brasileiros = {
                "AC", "AL", "AP", "AM", "BA", "CE", "DF",
                "ES", "GO", "MA", "MT", "MS", "MG", "PA",
                "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
                "RO", "RR", "SC", "SP", "SE", "TO"
            }

            if uf:

                if len(uf) != 2 or not uf.isalpha():
                    erros["uf"] = (
                        "A UF deve conter exatamente 2 letras."
                    )

                elif uf not in estados_brasileiros:
                    erros["uf"] = (
                        "Informe uma UF válida do Brasil."
                    )

            # ==========================================================
            # 12. VALIDAÇÃO DA CIDADE
            # ==========================================================

            if cidade:

                if len(cidade) < 2:
                    erros["cidade"] = (
                        "Informe uma cidade válida."
                    )

            # ==========================================================
            # 13. VALIDAÇÃO DO BAIRRO
            # ==========================================================

            if bairro:

                if len(bairro) < 2:
                    erros["bairro"] = (
                        "Informe um bairro válido."
                    )

            # ==========================================================
            # 14. VALIDAÇÃO DO LOGRADOURO
            # ==========================================================

            if logradouro:

                if len(logradouro) < 3:
                    erros["logradouro"] = (
                        "Informe um logradouro válido."
                    )

            # ==========================================================
            # 15. VALIDAÇÃO DO NÚMERO
            # ==========================================================

            if numero:

                if not re.match(r"^[0-9]+$", numero):
                    erros["numero"] = (
                        "O número deve conter apenas números."
                    )

            # ==========================================================
            # 16. VALIDAÇÃO DA DESCRIÇÃO
            # ==========================================================

            if descricao:

                if len(descricao) > 500:
                    erros["descricao"] = (
                        "A descrição deve ter no máximo 500 caracteres."
                    )

            # ==========================================================
            # 17. VALIDAÇÃO DA FOTO
            # ==========================================================

            if foto and foto.filename:

                extensoes_permitidas = {
                    "png",
                    "jpg",
                    "jpeg",
                    "webp"
                }

                extensao = foto.filename.rsplit(".", 1)[-1].lower()

                if extensao not in extensoes_permitidas:
                    erros["foto"] = (
                        "Formato de imagem inválido. "
                        "Use PNG, JPG, JPEG ou WEBP."
                    )

            # ==========================================================
            # 18. MOSTRAR OS ERROS NO FLASH
            # ==========================================================

            if erros:

                nomes_amigaveis = {
                    "cpf": "CPF",
                    "nome": "Nome",
                    "email": "E-mail",
                    "telefone": "Telefone",
                    "senha": "Senha",
                    "confirmaSenha": "Confirmar Senha",
                    "cep": "CEP",
                    "cidade": "Cidade",
                    "uf": "UF",
                    "bairro": "Bairro",
                    "logradouro": "Logradouro",
                    "numero": "Número",
                    "complemento": "Complemento",
                    "descricao": "Descrição",
                    "foto": "Foto do Barbeiro"
                }

                campos_com_falha = []

                for campo, mensagem in erros.items():

                    nome_campo = nomes_amigaveis.get(
                        campo,
                        campo
                    )

                    campos_com_falha.append(
                        f"{nome_campo}: {mensagem}"
                    )

                texto_campos = " | ".join(campos_com_falha)

                flash(
                    f"Atenção! Corrija os seguintes campos: {texto_campos}",
                    EnumStatusMensagens.AVISO.value
                )

                return render_template(
                    rota_erro,
                    erros=erros,
                    mensagens_status=EnumStatusMensagens,
                    dados_preenchidos=request.form
                )

            erros_unicidade = ValidarBarbeiro.verificarDadosUnicos(
                cpf=cpf,
                email=email,
                telefone=telefone,
                id_barbeiro=id_barbeiro
            )

            if erros_unicidade:
                erros.update(erros_unicidade)

                nomes_amigaveis = {
                    "cpf": "CPF",
                    "email": "E-mail",
                    "telefone": "Telefone"
                }

                mensagens = [
                    f"{nomes_amigaveis.get(campo, campo)}: {mensagem}"
                    for campo, mensagem in erros_unicidade.items()
                ]

                flash(
                    "Atenção! " + " | ".join(mensagens),
                    EnumStatusMensagens.AVISO.value
                )

                return render_template(
                    rota_erro,
                    erros=erros,
                    mensagens_status=EnumStatusMensagens,
                    dados_preenchidos=request.form
                )

            # ==========================================================
            # 19. SE NÃO EXISTEM ERROS, SALVAR O BARBEIRO
            # ==========================================================

            nome_foto = None

            if foto and foto.filename:
                nome_foto = secure_filename(foto.filename)

            if id_barbeiro is None:
                print("Passei aqui!!!")
                # CADASTRO: insere novos registros
                resultado = ValidarBarbeiro.criarBarbeiro(
                    cpf=cpf,
                    nome=nome,
                    email=email,
                    senha=senha,
                    telefone=telefone,
                    foto=nome_foto,
                    descricao=descricao,
                    cep=cep_limpo,
                    cidade=cidade,
                    uf=uf,
                    bairro=bairro,
                    logradouro=logradouro,
                    numero=numero,
                    complemento=complemento,
                    sequencia=sequencia
                )

                mensagem = "Barbeiro cadastrado com sucesso!"

            else:
                # EDIÇÃO: atualiza os registros existentes
                resultado = ValidarBarbeiro.editarBarbeiro(
                    id_barbeiro=id_barbeiro,
                    cpf=cpf,
                    nome=nome,
                    email=email,
                    senha=senha,
                    telefone=telefone,
                    foto=nome_foto,
                    descricao=descricao,
                    cep=cep_limpo,
                    cidade=cidade,
                    uf=uf,
                    bairro=bairro,
                    logradouro=logradouro,
                    numero=numero,
                    complemento=complemento,
                    sequencia=sequencia
                )

                mensagem = "Barbeiro atualizado com sucesso!"

            # 20. VERIFICAR O RESULTADO
            if not resultado:
                flash(
                    "Não foi possível salvar o barbeiro.",
                    EnumStatusMensagens.ERRO.value
                )

                return render_template(
                    rota_erro,
                    mensagens_status=EnumStatusMensagens,
                    dados_preenchidos=request.form
                )

            # 21. SUCESSO
            flash(mensagem, EnumStatusMensagens.SUCESSO.value)

            return redirect(url_for(rota_certa))

        except Exception as erro:

            print(f"Erro na validação/cadastro: {erro}")

            flash(
                "Ocorreu um erro ao realizar o cadastro.",
                EnumStatusMensagens.ERRO.value
            )

            return render_template(
                rota_erro,
                mensagens_status= EnumStatusMensagens,
                dados_preenchidos=request.form
            )

    @staticmethod
    def criarBarbeiro(
        cpf,
        nome,
        email,
        senha,
        telefone,
        foto,
        descricao,
        cep,
        cidade,
        uf,
        bairro,
        logradouro,
        numero,
        complemento,
        sequencia
    ):

        try:

            print("======================================")
            print("INICIANDO CADASTRO DO BARBEIRO")
            print("======================================")


            # ==========================================================
            # 1. BUSCAR O ESTADO
            # ==========================================================

            estado = db.session.execute(
                db.text("""
                    SELECT id
                    FROM estados
                    WHERE sigla_estado = :uf
                """),
                {
                    "uf": uf
                }
            ).scalar()

            print("ID DO ESTADO:", estado)

            if not estado:
                raise Exception(
                    f"Estado não encontrado para a UF: {uf}"
                )


            # ==========================================================
            # 2. CRIAR ENDEREÇO
            # ==========================================================

            endereco = Endereco(
                cep=cep,
                cidade=cidade,
                numero=int(numero),
                bairro=bairro,
                estado=estado,
                sequencia=sequencia if sequencia else None,
                complemento=complemento if complemento else None
            )
            print("OBJETO ENDEREÇO CRIADO")

            id_endereco = endereco.inserirEndereco()

            print("ID DO ENDEREÇO:", id_endereco)

            if not id_endereco:
                raise Exception(
                    "O endereço não retornou um ID."
                )


            # ==========================================================
            # 3. CRIAR USUÁRIO
            # ==========================================================

            agora = datetime.now(timezone.utc)

            usuario = Usuario(
                nome_completo=nome,
                telefone=re.sub(r"\D", "", telefone),
                email=email,
                senha=senha,
                foto=foto,
                id_endereco=id_endereco,
                ativo=1,
                data_cadastro=agora,
                data_atualizacao=agora,
                cpf=re.sub(r"\D", "", cpf)
            )

            print("OBJETO USUÁRIO CRIADO")

            id_usuario = usuario.salvar()

            print("ID DO USUÁRIO:", id_usuario)

            if not id_usuario:
                raise Exception(
                    "O usuário não retornou um ID."
                )


            # ==========================================================
            # 4. CRIAR BARBEIRO
            # ==========================================================

            barbeiro = Barbeiro()

            barbeiro.id = id_usuario
            barbeiro.data_liberacao = None
            barbeiro.ativo = 1
            barbeiro.descricao = descricao

            print("OBJETO BARBEIRO CRIADO")

            barbeiro.salvar()

            print("BARBEIRO INSERIDO")


            # ==========================================================
            # 5. COMMIT
            # ==========================================================

            db.session.commit()

            print("======================================")
            print("CADASTRO CONCLUÍDO COM SUCESSO")
            print("======================================")

            return id_usuario


        except Exception as erro:

            db.session.rollback()

            import traceback

            print("======================================")
            print("ERRO AO SALVAR BARBEIRO")
            print("======================================")
            print(f"ERRO: {erro}")

            traceback.print_exc()

            print("======================================")

            return None

    @staticmethod
    def editarBarbeiro(
        id_barbeiro,
        cpf,
        nome,
        email,
        senha,
        telefone,
        foto,
        descricao,
        cep,
        cidade,
        uf,
        bairro,
        logradouro,
        numero,
        complemento,
        sequencia
    ):
        try:
            print("======================================")
            print("INICIANDO EDIÇÃO DO BARBEIRO")
            print("ID:", id_barbeiro)
            print("======================================")

            # ==========================================================
            # 1. BUSCAR O BARBEIRO EXISTENTE
            # ==========================================================

            barbeiro = db.session.get(Barbeiro, id_barbeiro)

            if barbeiro is None:
                raise Exception("Barbeiro não encontrado.")

            # ==========================================================
            # 2. BUSCAR O USUÁRIO ASSOCIADO
            # ==========================================================

            usuario = db.session.get(Usuario, id_barbeiro)

            if usuario is None:
                raise Exception("Usuário do barbeiro não encontrado.")

            # ==========================================================
            # 3. BUSCAR O ENDEREÇO ASSOCIADO
            # ==========================================================

            endereco = db.session.get(
                Endereco,
                usuario.fk_id_endereco
            )

            if endereco is None:
                raise Exception("Endereço do barbeiro não encontrado.")

            # ==========================================================
            # 4. BUSCAR O ESTADO PELA UF
            # ==========================================================

            estado = db.session.execute(
                db.text("""
                    SELECT id
                    FROM estados
                    WHERE sigla_estado = :uf
                """),
                {"uf": uf}
            ).scalar()

            if estado is None:
                raise Exception(f"Estado não encontrado para a UF: {uf}")

            # ==========================================================
            # 5. ATUALIZAR O ENDEREÇO EXISTENTE
            # ==========================================================

            endereco.cep = cep
            endereco.cidade = cidade
            endereco.numero = int(numero)
            endereco.bairro = bairro
            endereco.fk_estado = estado
            endereco.sequencia = sequencia if sequencia else None
            endereco.complemento = complemento if complemento else None

            # ==========================================================
            # 6. ATUALIZAR OS DADOS DO USUÁRIO
            # ==========================================================

            usuario.cpf = re.sub(r"\D", "", cpf)
            usuario.nome_completo = nome
            usuario.email = email
            usuario.telefone = re.sub(r"\D", "", telefone)
            usuario.data_atualizacao = datetime.now(timezone.utc)

            # Só altera a senha se o usuário informou uma nova.
            if senha and senha.strip():
                from werkzeug.security import generate_password_hash

                usuario.senha_hash = generate_password_hash(senha)

            # Só substitui a foto se uma nova foto foi enviada.
            if foto:
                usuario.foto_nome = foto

            # ==========================================================
            # 7. ATUALIZAR OS DADOS DO BARBEIRO
            # ==========================================================

            barbeiro.descricao = descricao

            # ==========================================================
            # 8. SALVAR TODAS AS ALTERAÇÕES
            # ==========================================================

            db.session.commit()

            print("======================================")
            print("BARBEIRO ATUALIZADO COM SUCESSO")
            print("======================================")

            return id_barbeiro

        except Exception as erro:
            db.session.rollback()

            import traceback

            print("======================================")
            print("ERRO AO EDITAR BARBEIRO")
            print("======================================")
            print(f"ERRO: {erro}")

            traceback.print_exc()

            print("======================================")

            return None

    @staticmethod
    def verificarDadosUnicos(cpf, email, telefone, id_barbeiro=None):
        cpf = re.sub(r"\D", "", cpf)
        telefone = re.sub(r"\D", "", telefone)
        email = email.strip()

        sql = db.text("""
            SELECT id, cpf, email, telefone
            FROM usuarios
            WHERE cpf = :cpf
            OR LOWER(email) = LOWER(:email)
            OR telefone = :telefone
        """)

        registros = db.session.execute(
            sql,
            {
                "cpf": cpf,
                "email": email,
                "telefone": telefone
            }
        ).mappings().all()

        erros = {}

        for usuario in registros:
            # Na edição, não considerar o próprio usuário como duplicado.
            if (
                id_barbeiro is not None
                and usuario["id"] == id_barbeiro
            ):
                continue

            if usuario["cpf"] == cpf:
                erros["cpf"] = "Este CPF já está cadastrado."

            if (
                usuario["email"]
                and usuario["email"].lower() == email.lower()
            ):
                erros["email"] = "Este e-mail já está cadastrado."

            telefone_existente = re.sub(
                r"\D", "", usuario["telefone"] or ""
            )

            if telefone_existente == telefone:
                erros["telefone"] = "Este telefone já está cadastrado."

        return erros
            
