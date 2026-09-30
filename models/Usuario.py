from database import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from sqlalchemy.dialects.mysql import TINYINT

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    # 1. Mapeamento das Colunas no MySQL (Sem CPF)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(11), unique=True)
    cpf = db.Column(db.CHAR(11), unique=True, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    foto_nome = db.Column(db.String(255), nullable=True)
    ativo = db.Column(TINYINT(1), default=1, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Correto: apontando para id_endereco
    fk_id_endereco = db.Column(db.Integer, db.ForeignKey('enderecos.id'), nullable=True)

    # Relacionamento virtual apontando para a classe Endereco
    enderecos = db.relationship('Endereco', backref='usuarios', lazy=True)

    # 2. Construtor Ajustado para os dados do formulário (Sem CPF)
    def __init__(self, nome_completo, telefone, email, senha, foto, id_endereco, ativo, data_cadastro, data_atualizacao, cpf):
        self.nome_completo = nome_completo
        self.telefone = telefone
        self.cpf = cpf
        self.email = email
        self.senha_hash = senha
        self.endereco_id = id_endereco 
        self.foto_path = foto
        self.ativo = ativo
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    # 3. Serialização para a Sessão / Respostas JSON
    def to_dict(self):
        return {
            'id': self.id, 
            'nome_completo': self.nome_completo,
            'telefone': self.telefone,
            'email': self.email,
            'senha': self.senha_hash,  
        }
        
    def getDict(user):
        return {
                'id': user.id, 
                'nome_completo': user.nome_completo,
                'telefone': user.telefone,
                'email': user.email,
                'senha': user.senha_hash,  
        }

    # ============================================================
    # MÉTODOS CRUD OFICIAIS (CORRIGIDOS)
    # ============================================================

    # CREATE - Salva o usuário e retorna o ID auto-incremental gerado pelo MySQL
    def salvar(self):
        result = db.session.execute(
                        db.text("""
                              insert into usuarios 
                              (nome_completo,telefone,cpf,email,senha_hash,foto_nome,ativo, data_cadastro, data_atualizacao, fk_id_endereco)
                                values (:nome_completo, :telefone, :cpf, :email, :senha_hash, :foto_nome, :ativo, :data_cadastro, :data_atualizacao, :fk_id_endereco)  
                        """),
                        {
                            "nome_completo": self.nome_completo,
                            "telefone": self.telefone,
                            "cpf": self.cpf,
                            "email": self.email,
                            "senha_hash": generate_password_hash(self.senha_hash),
                            "foto_nome": self.foto_nome,
                            "ativo": self.ativo,
                            "data_cadastro": self.data_cadastro,
                            "data_atualizacao": self.data_atualizacao,
                            "fk_id_endereco": self.fk_id_endereco
    
                         }
        
                    )

        return result.lastrowid

    # READ - Busca o usuário diretamente pela Chave Primária (id)
    @classmethod
    def buscar_por_id(cls, id):
        return db.session.get(cls, id)

    # READ - 🔥 CORRIGIDO: Atualizado para a sintaxe moderna db.select
  
        
        
    # READ - 🔥 CORRIGIDO: Atualizado para a sintaxe moderna db.select e scalars().all()

    def listar_todos(cls):
        stmt = db.select(cls).order_by(cls.nome_completo.asc())
        return db.session.scalars(stmt).all()

    # UPDATE - Confirma as alterações feitas no objeto
    def atualizar(self):
        db.session.commit()
        return True

    # DELETE - 🔥 CORRIGIDO: Mantém a segurança do cascade deletando o objeto da sessão
    @classmethod
    def excluir_por_id(cls, id):
        usuario = cls.buscar_por_id(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False

    def consultarUsuario():
        return db.session.execute(
            db.text("""
                   select * from usuarios limit 1 
            """)
        ).fetchall()
    
    # chamar o método pela própria classe
    # cls é uma convenção do Python que representa a própria classe
    @classmethod
    def inserirUsuarioGestor(cls, id_endereco_gestor:int):
        
        usuario_gestor = cls.consultarUsuario()
        
        if not usuario_gestor:
            
            cls.fk_id_endereco = id_endereco_gestor
            cls.nome_completo = "Samuel Maicon da Silva"
            cls.telefone="84999999999"
            cls.cpf="12345678901"
            cls.email="samuelmaicon.gestor@gmail.com"
            cls.senha_hash="1234"
            cls.foto_nome="samuel.jpg"
            cls.ativo=1
            cls.data_cadastro=datetime.now(timezone.utc)
            cls.data_atualizacao=datetime.now(timezone.utc)                                    
               
            return cls.salvar(cls)
        
        return -1