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
    cpf = db.Column(db.CHAR(11), unique=True, nullable=False)
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
    def __init__(self, nome_completo, telefone, email, senha, foto, id_endereco):
        self.nome_completo = nome_completo
        self.telefone = telefone
        self.email = email
        self.senha_hash = generate_password_hash(senha)
        self.endereco_id = id_endereco 
        self.foto_path = foto

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
        db.session.add(self)
        db.session.commit()
        return self.id 

    # READ - Busca o usuário diretamente pela Chave Primária (id)
    @classmethod
    def buscar_por_id(cls, id):
        return db.session.get(cls, id)

    # READ - 🔥 CORRIGIDO: Atualizado para a sintaxe moderna db.select
    @classmethod
    def buscar_por_email(cls, email):
        return db.session.execute(
            db.text(
        """
            select *
            from clientes c join usuarios u 
            on c.cliente_id = u.id where u.email = :email
        """
            ),
            {"email":email}
        ).first()
        
        
    @classmethod
    def buscar_por_email_gestor(cls, email):
        return db.session.execute(
                    db.text(
                """
                   select * from barbearias b join usuarios u  on u.id = b.gestor_id where u.email =:email
                """
                    ),
                    {"email":email}
        ).first()

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

            db.session.execute(
                db.text("""
                      insert into usuarios 
                      (nome_completo,telefone,cpf,email,senha_hash,foto_nome,ativo, data_cadastro, data_atualizacao, fk_id_endereco)
                        values (:nome_completo, :telefone, :cpf, :email, :senha_hash, :foto_nome, :ativo, :data_cadastro, :data_atualizacao, :fk_id_endereco)  
                """),
                {
                    "nome_completo": "Samuel Maicon da Silva",
                    "telefone": "84999999999",
                    "cpf": "12345678901",
                    "email": "gestorbb@gmail.com",
                    "senha_hash": generate_password_hash("1234"),
                    "foto_nome": "samuel.jpg",
                    "ativo": 1,
                    "data_cadastro": "2026-09-29 20:00:00",
                    "data_atualizacao": "2026-09-29 20:00:00",
                    "fk_id_endereco": 1

                 }

            )

            db.session.commit()
                
            return 1

        return -1