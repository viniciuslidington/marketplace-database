# 🏪 Marketplace Database

## 📋 Descrição do Projeto

Este é um **sistema completo de banco de dados para marketplace** desenvolvido com PostgreSQL, FastAPI e Docker. O projeto implementa um modelo de dados robusto para e-commerce, incluindo gerenciamento de usuários, produtos, pedidos, pagamentos e muito mais.

### 🎯 Objetivos do Projeto

- **Implementação completa de banco de dados** em SQL com PostgreSQL
- **Criação de relações complexas** com restrições de integridade referencial
- **Inserção de volume significativo de dados** para teste e demonstração
- **Conjunto abrangente de consultas** para análise de dados
- **Integração com linguagem de programação** através de FastAPI
- **Containerização completa** com Docker para facilitar execução

## 🏗️ Arquitetura do Sistema

### 📊 Modelo de Dados

O banco de dados contém **13 tabelas principais** organizadas em módulos:

#### 👥 **Gestão de Usuários**
- `Usuario` - Dados base dos usuários
- `Comprador` - Extensão para compradores com endereços
- `Vendedor` - Extensão para vendedores com dados comerciais
- `Endereco` - Endereços de entrega dos compradores

#### 🛍️ **Catálogo de Produtos**
- `Categoria` - Categorização dos produtos
- `Produto` - Produtos disponíveis no marketplace
- `Estoque` - Controle de inventário

#### 🛒 **Gestão de Pedidos**
- `Pedido` - Pedidos realizados
- `ItemPedido` - Itens individuais de cada pedido
- `StatusPedido` - Histórico de status dos pedidos

#### 💳 **Sistema de Pagamento**
- `Pagamento` - Transações financeiras
- `Cartao` - Cartões cadastrados pelos compradores

#### ⭐ **Avaliação e Feedback**
- `Avaliacao` - Avaliações dos produtos pelos compradores

### 🔗 Relacionamentos Principais

- **Usuários** podem ser **Compradores** e/ou **Vendedores**
- **Compradores** têm múltiplos **Endereços** e **Cartões**
- **Vendedores** gerenciam **Produtos** e **Estoque**
- **Pedidos** contêm múltiplos **ItemPedido**
- **Pagamentos** são vinculados a **Pedidos** específicos
- **Avaliações** são feitas por **Compradores** em **Pedidos**

## 🚀 Como Executar o Projeto

### ⚡ Execução Rápida (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/viniciuslidington/marketplace-database.git
cd marketplace-database

# 2. Execute com Docker Compose
docker-compose up -d

# 3. Aguarde alguns segundos para inicialização completa
```

**Pronto!** Os serviços estarão disponíveis em:
- 🌐 **API**: http://localhost:8000
- 📚 **Documentação**: http://localhost:8000/docs  
- 🗃️ **Adminer**: http://localhost:8080

### 📋 Pré-requisitos

- **Docker** instalado
- **Docker Compose** instalado
- **Portas disponíveis**: 8000, 5432, 8080

### 🔧 Execução Detalhada

#### 1️⃣ **Preparação do Ambiente**
```bash
# Verificar se Docker está rodando
docker --version
docker-compose --version

# Verificar portas disponíveis
lsof -i :8000  # Deve estar livre
lsof -i :5432  # Deve estar livre
lsof -i :8080  # Deve estar livre
```

#### 2️⃣ **Inicialização dos Containers**
```bash
# Opção A: Comando direto
docker-compose up -d

# Opção B: Script de gerenciamento
chmod +x docker-manager.sh
./docker-manager.sh start
```

#### 3️⃣ **Verificação dos Serviços**
```bash
# Verificar status dos containers
docker-compose ps

# Verificar logs (se necessário)
docker-compose logs -f api
```

#### 4️⃣ **Teste da API**
```bash
# Health check
curl http://localhost:8000/health

# Endpoint principal
curl http://localhost:8000/

# Listar produtos
curl http://localhost:8000/produtos
```

## 🌐 Serviços Disponíveis

| Serviço | URL | Descrição | Credenciais |
|---------|-----|-----------|-------------|
| **API REST** | http://localhost:8000 | FastAPI com 13 endpoints | - |
| **Documentação** | http://localhost:8000/docs | Swagger UI interativo | - |
| **Adminer** | http://localhost:8080 | Interface web do banco | Ver abaixo |
| **PostgreSQL** | localhost:5432 | Banco de dados | Ver abaixo |

### 🔐 Credenciais de Acesso

**PostgreSQL & Adminer:**
- **Servidor**: `db` (interno) ou `localhost` (externo)
- **Banco**: `marketplace`
- **Usuário**: `admin`
- **Senha**: `admin123`
- **Porta**: `5432`

## 📊 Dados de Exemplo

O banco é automaticamente populado com:
- **15 usuários** (compradores e vendedores)
- **20 produtos** em 5 categorias diferentes
- **15 pedidos** com status variados
- **25+ itens de pedido**
- **10+ pagamentos** processados
- **Histórico completo** de status e avaliações

## 🔍 Principais Endpoints da API

### 📦 **Produtos**
- `GET /produtos` - Listar todos os produtos
- `GET /produtos/{id}` - Detalhes de um produto
- `GET /produtos/mais-vendidos` - Top produtos por vendas

### 🛒 **Pedidos**  
- `POST /pedidos` - Criar novo pedido
- `GET /pedidos/comprador/{id}` - Pedidos de um comprador

### 📊 **Analytics**
- `GET /dashboard` - Métricas gerais do marketplace
- `GET /clientes/vip` - Clientes com maior valor
- `GET /estoque/critico` - Produtos com estoque baixo

### 👥 **Usuários**
- `GET /comprador/email/{email}` - Buscar comprador por email
- `GET /comprador/{id}/enderecos` - Endereços de um comprador

### ❤️ **Sistema**
- `GET /health` - Status da API e banco
- `GET /` - Informações da API

## 🗃️ Estrutura do Projeto

```
marketplace-database/
├── 📄 docker-compose.yml      # Orquestração dos containers
├── 🐳 Dockerfile              # Container PostgreSQL
├── 🐳 Dockerfile.api          # Container FastAPI
├── ⚙️ docker-manager.sh       # Script de gerenciamento
├── 🔧 .env                    # Variáveis de ambiente
├── 📊 init.sql               # Schema do banco de dados
├── 📊 sample_data.sql        # Dados de exemplo
├── 📊 queries.sql            # Consultas de exemplo
├── 📋 pyproject.toml         # Dependências Python (UV)
└── app/
    ├── 🚀 api.py             # Aplicação FastAPI
    └── 🗄️ database.py        # Conexão com banco
```

## 🛠️ Comandos Úteis

### 🔄 **Gerenciamento de Containers**
```bash
# Parar todos os serviços
docker-compose down

# Reiniciar apenas a API
docker-compose restart api

# Ver logs em tempo real
docker-compose logs -f

# Reconstruir containers
docker-compose build
```

### 🧹 **Limpeza e Reset**
```bash
# Parar e remover tudo (CUIDADO!)
docker-compose down -v

# Limpar sistema Docker
docker system prune -f

# Rebuild completo
docker-compose build --no-cache
docker-compose up -d
```

## 🚨 Troubleshooting

### ❌ **Problemas Comuns**

**1. Porta já em uso**
```bash
# Verificar que processo está usando a porta
lsof -i :8000
kill -9 <PID>  # Se necessário
```

**2. Container da API não inicia**
```bash
# Ver logs detalhados
docker-compose logs api

# Rebuild da imagem
docker-compose build api
```

**3. Banco de dados não conecta**
```bash
# Verificar se container está saudável
docker-compose ps

# Logs do PostgreSQL
docker-compose logs db
```

### ✅ **Verificação de Saúde**
```bash
# Status de todos os containers
docker-compose ps

# Health check da API
curl http://localhost:8000/health

# Conectar diretamente ao banco
docker exec -it marketplace_postgres psql -U admin -d marketplace
```

## 🎯 Funcionalidades Implementadas

- ✅ **Schema completo** com 13 tabelas e relacionamentos
- ✅ **Dados de exemplo** realistas para desenvolvimento
- ✅ **API REST** com 13 endpoints documentados
- ✅ **Documentação interativa** com Swagger UI
- ✅ **Containerização** completa com Docker
- ✅ **Interface de administração** com Adminer
- ✅ **Consultas analíticas** para insights de negócio
- ✅ **Sistema de saúde** e monitoramento
- ✅ **Logs estruturados** para debugging

## 📈 Métricas e Analytics

A API fornece endpoints para análise de:
- **Volume de vendas** por período
- **Produtos mais vendidos**
- **Clientes VIP** por valor gasto
- **Estoque crítico** por categoria
- **Performance de vendedores**
- **Status de pedidos** em tempo real

## 🤝 Contribuições

Este projeto foi desenvolvido como demonstração de conhecimentos em:
- **Modelagem de banco de dados**
- **SQL avançado** e **PostgreSQL**
- **API Development** com **FastAPI**
- **Containerização** com **Docker**
- **Documentação técnica**

---

**🚀 Projeto pronto para execução! Execute `docker-compose up -d` e explore a API em http://localhost:8000/docs**