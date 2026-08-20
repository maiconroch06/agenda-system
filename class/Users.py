class Users:
    def __init__(self,cpf, nome, sobrenome, telefone,email, senha, fotoPerfil, ativo, endereco):
        self.nome = nome
        self.cpf = cpf
        self.sobrenome = sobrenome
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.foto_perfil = fotoPerfil
        self.ativo = ativo
        self.endereco = endereco


        #metodos privados self.__nome (utilizando __ deixa a variavel privada, mas posso acessar )
        # usuario  = Users(campospreenchidos)
        # print(usuario._Users.__nome)-> isso funciona
        # por isso não é um private absoluto, é considerado um private aproximadamente;
        #Essa regra se aplica ao protected.
        
    