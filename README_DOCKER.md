# Marketplace Database - Docker

## 🐳 Containers Criados

O projeto agora está totalmente containerizado com Docker Compose, incluindo:

- **PostgreSQL Database** (marketplace_postgres) - Porta 5432
- **FastAPI API** (marketplace_api) - Porta 8000  
- **Adminer** (marketplace_adminer) - Porta 8080

## 🚀 Como Executar

### Opção 1: Docker Compose Simples
```bash
# Iniciar todos os containers
docker-compose up -d

# Parar todos os containers
docker-compose down

# Ver status dos containers
docker-compose ps

# Ver logs
docker-compose logs -f
```

### Opção 2: Script de Gerenciamento
```bash
# Tornar o script executável (primeira vez)
chmod +x docker-manager.sh

# Iniciar containers
./docker-manager.sh start

# Parar containers
./docker-manager.sh stop

# Ver logs da API
./docker-manager.sh logs-api

# Ver status
./docker-manager.sh status
```

## 🌐 Serviços Disponíveis

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **API** | http://localhost:8000 | API REST do Marketplace |
| **Documentação** | http://localhost:8000/docs | Swagger UI da API |
| **Adminer** | http://localhost:8080 | Interface web do banco |
| **PostgreSQL** | localhost:5432 | Banco de dados |

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```bash
# Banco de dados
DB_HOST=db  # 'db' para containers, 'localhost' para local
DB_PORT=5432
DB_NAME=marketplace
DB_USER=admin
DB_PASSWORD=admin123

# API
API_HOST=0.0.0.0
API_PORT=8000
```

### Credenciais do Banco
- **Host:** localhost (ou `db` dentro dos containers)
- **Porta:** 5432
- **Database:** marketplace
- **Usuário:** admin
- **Senha:** admin123

## 📊 Testando a API

```bash
# Health check
curl http://localhost:8000/health

# Listar produtos
curl http://localhost:8000/produtos

# Ver documentação completa
open http://localhost:8000/docs
```

## 🛠️ Desenvolvimento

### Rebuild dos Containers
```bash
# Rebuild completo
docker-compose build

# Rebuild apenas da API
docker-compose build api

# Restart apenas da API
docker-compose restart api
```

### Logs Específicos
```bash
# Logs da API
docker-compose logs -f api

# Logs do banco
docker-compose logs -f db

# Logs do Adminer
docker-compose logs -f adminer
```

## 📁 Estrutura de Arquivos Docker

```
├── docker-compose.yml      # Orquestração dos containers
├── Dockerfile             # PostgreSQL container
├── Dockerfile.api         # FastAPI container  
├── docker-manager.sh      # Script de gerenciamento
├── .env                   # Variáveis de ambiente
├── init.sql              # Schema do banco
├── sample_data.sql       # Dados de exemplo
└── app/
    ├── api.py           # FastAPI application
    └── database.py      # Database connection
```

## 🚨 Troubleshooting

### Container da API não inicia
```bash
# Ver logs detalhados
docker-compose logs api

# Rebuild da imagem
docker-compose build api
docker-compose up api
```

### Banco não conecta
```bash
# Verificar se o container está saudável
docker-compose ps

# Verificar logs do PostgreSQL
docker-compose logs db
```

### Portas em uso
```bash
# Verificar quem está usando as portas
lsof -i :8000  # API
lsof -i :5432  # PostgreSQL
lsof -i :8080  # Adminer
```

## 🎯 Próximos Passos

1. ✅ Containers criados e funcionais
2. ✅ API documentada e testável  
3. ✅ Banco populado com dados de exemplo
4. ✅ Interface de administração (Adminer)

O marketplace está pronto para uso!
