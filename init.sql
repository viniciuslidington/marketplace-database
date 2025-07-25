CREATE TABLE Usuario (
    ID_Usuario SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Senha VARCHAR(100) NOT NULL,
    Telefone VARCHAR(20),
    Tipo_Usuario VARCHAR(20) CHECK (Tipo_Usuario IN ('comprador', 'vendedor')) NOT NULL
);

CREATE TABLE Comprador (
    ID_Usuario INTEGER PRIMARY KEY REFERENCES Usuario(ID_Usuario),
    CPF VARCHAR(14) UNIQUE NOT NULL
);

CREATE TABLE Vendedor (
    ID_Usuario INTEGER PRIMARY KEY REFERENCES Usuario(ID_Usuario),
    Nome_Loja VARCHAR(100),
    CNPJ VARCHAR(18) UNIQUE NOT NULL
);

CREATE TABLE Categoria (
    ID_Categoria SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Descricao TEXT
);

CREATE TABLE Produto (
    ID_Produto SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Descricao TEXT,
    Preco NUMERIC(10, 2) NOT NULL,
    Estoque INTEGER NOT NULL,
    ID_Vendedor INTEGER NOT NULL REFERENCES Vendedor(ID_Usuario)
);

CREATE TABLE Produto_Categoria (
    ID_Produto INTEGER REFERENCES Produto(ID_Produto),
    ID_Categoria INTEGER REFERENCES Categoria(ID_Categoria),
    PRIMARY KEY(ID_Produto, ID_Categoria)
);

CREATE TABLE Endereco (
    ID_Endereco SERIAL PRIMARY KEY,
    Rua VARCHAR(100),
    Numero VARCHAR(10),
    CEP VARCHAR(10),
    Estado VARCHAR(50),
    Cidade VARCHAR(50),
    Complemento VARCHAR(100),
    ID_Comprador INTEGER REFERENCES Comprador(ID_Usuario)
);

CREATE TABLE Pagamento (
    ID_Pagamento SERIAL PRIMARY KEY,
    Metodo_Pagamento VARCHAR(20) CHECK (Metodo_Pagamento IN ('cartao', 'pix', 'boleto')),
    Data DATE NOT NULL,
    Valor NUMERIC(10, 2),
    Status VARCHAR(20)
);

CREATE TABLE Cartao (
    ID_Cartao SERIAL PRIMARY KEY,
    Nome VARCHAR(100),
    Numero VARCHAR(20),
    Bandeira VARCHAR(50),
    Validade DATE,
    ID_Comprador INTEGER REFERENCES Comprador(ID_Usuario)
);

CREATE TABLE PagamentoCartao (
    ID_Pagamento INTEGER PRIMARY KEY REFERENCES Pagamento(ID_Pagamento),
    ID_Cartao INTEGER REFERENCES Cartao(ID_Cartao)
);

CREATE TABLE PagamentoPix (
    ID_Pagamento INTEGER PRIMARY KEY REFERENCES Pagamento(ID_Pagamento),
    ChavePix VARCHAR(100),
    Instituicao VARCHAR(100)
);

CREATE TABLE PagamentoBoleto (
    ID_Pagamento INTEGER PRIMARY KEY REFERENCES Pagamento(ID_Pagamento),
    Codigo_Barras VARCHAR(100),
    Vencimento DATE
);

CREATE TABLE Pedido (
    ID_Pedido SERIAL PRIMARY KEY,
    Data DATE NOT NULL,
    Status VARCHAR(20),
    ID_Comprador INTEGER REFERENCES Comprador(ID_Usuario),
    ID_Endereco INTEGER REFERENCES Endereco(ID_Endereco),
    ID_Pagamento INTEGER REFERENCES Pagamento(ID_Pagamento)
);

CREATE TABLE ItemDoPedido (
    ID_Produto INTEGER REFERENCES Produto(ID_Produto),
    ID_Pedido INTEGER REFERENCES Pedido(ID_Pedido),
    Quantidade INTEGER NOT NULL,
    PrecoNaCompra NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (ID_Pedido, ID_Produto)
);

CREATE TABLE Avaliacao (
    ID_Avaliacao SERIAL PRIMARY KEY,
    Comentario TEXT,
    Nota INTEGER CHECK (Nota >= 0 AND Nota <= 5),
    Data DATE NOT NULL,
    ID_Pedido INTEGER REFERENCES Pedido(ID_Pedido)
);
