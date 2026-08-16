-- drop schema if exists agenda_system;
-- create schema if not exists  agenda_system;

USE agenda_system;
-- SE seguido diretamente do nome do banco;

create table usuario(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome varchar(150) not null,
    sobrenome varchar(150) not null,
    telefone varchar(20) not null,
    email varchar(150) not null,
    senha varchar(255) not null,
    cpf varchar(14) not null unique,
	foto_perfil Text,
    ativo tinyint(1) not null,
    data_criacao timestamp not null,
    data_atualizacao timestamp not null,
    endereco_id int not null,
    
    constraint fk_usuario_endereco foreign key (endereco_id) references enderecos(id)
    
);

create table if not exists empresa(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome varchar(255) not null,
    decricao text,
    cnpj varchar(20),
    telefone varchar(20) not null,
    email_empresa varchar(150) not null,
    logo_image text,
    data_cadastro timestamp not null,
    categoria_empresa_id int not null,
    endereco_id int not null,
   
   constraint fk_empresa_endereco foreign key (endereco_id) references enderecos(id),
   constraint fk_empresa_categoria foreign key (categoria_empresa_id) references categoria_empresa(id)
      
);

CREATE	TABLE IF NOT EXISTS empresa_usuario(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    empresa_id int not null,
    usuario_id int not null,
  
    constraint fk_usuario foreign key (usuario_id) references usuario(id),
    constraint fk_empresa foreign key (empresa_id) references empresa(id)
);

CREATE TABLE IF NOT EXISTS categoria_empresa(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    descricao varchar(50)
);

create table if not exists dias_da_semana(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	nome_do_dia varchar(15) not null
);

create table if not exists empresa_dias_da_semana(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	empresa_id int not null,
    dia_semana_id int not null,
    horario_abertura time not null,
    horario_fechamento time not null,
    
    CONSTRAINT fk_empresa_dia_semana FOREIGN KEY (empresa_id) references empresa(id),
    constraint fk_dia_da_semana foreign key (dias_semana_id) references dias_da_semana(id)
);

create table if not exists endereco(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	cep varchar(10) not null,
	cidade varchar(40) not null,
    numeto int not null,
    bairro varchar(150) not null,
    estado varchar(2),
    sequencia int not null,
    complemento varchar(100)
);

create table if not exists funcionarios_empresa(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    empresa_id int not null,
    usuario_id int not null,
    data_cadastro timestamp not null,
    data_liberacao timestamp not null,
    ativo tinyint(1) not null,
    
    constraint fk_funcionario_empresa foreign key (empresa_id) references empresa(id),
    constraint fk_funcionario_usuario foreign key (usuario_id) references usuario(id)
    
    );
    
    -- PENDENTE AS DEMAIS TABELAS A DE SERVIÇOS, AGENDAMENTO, SERVIÇOS DA EMPRESA, SERVIÇOS QUE O FUNCIONARIO DA EMPRESA REALIZA


