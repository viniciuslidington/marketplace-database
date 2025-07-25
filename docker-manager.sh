#!/bin/bash

# Script para gerenciar os containers do Marketplace

case "$1" in
    "start")
        echo "🚀 Iniciando containers do Marketplace..."
        docker-compose up -d
        echo "✅ Containers iniciados!"
        echo "📊 API disponível em: http://localhost:8000"
        echo "📊 Documentação da API: http://localhost:8000/docs"
        echo "🗃️  Adminer disponível em: http://localhost:8080"
        ;;
    "stop")
        echo "🛑 Parando containers do Marketplace..."
        docker-compose down
        echo "✅ Containers parados!"
        ;;
    "restart")
        echo "🔄 Reiniciando containers do Marketplace..."
        docker-compose down
        docker-compose up -d
        echo "✅ Containers reiniciados!"
        ;;
    "logs")
        echo "📋 Logs dos containers:"
        docker-compose logs -f
        ;;
    "logs-api")
        echo "📋 Logs da API:"
        docker-compose logs -f api
        ;;
    "logs-db")
        echo "📋 Logs do banco de dados:"
        docker-compose logs -f db
        ;;
    "build")
        echo "🔨 Construindo containers..."
        docker-compose build
        echo "✅ Containers construídos!"
        ;;
    "status")
        echo "📊 Status dos containers:"
        docker-compose ps
        ;;
    "clean")
        echo "🧹 Limpando containers e volumes..."
        docker-compose down -v
        docker system prune -f
        echo "✅ Limpeza concluída!"
        ;;
    *)
        echo "🏪 Marketplace Database - Gerenciador de Containers"
        echo ""
        echo "Uso: $0 {start|stop|restart|logs|logs-api|logs-db|build|status|clean}"
        echo ""
        echo "Comandos disponíveis:"
        echo "  start     - Inicia todos os containers"
        echo "  stop      - Para todos os containers"
        echo "  restart   - Reinicia todos os containers"
        echo "  logs      - Exibe logs de todos os containers"
        echo "  logs-api  - Exibe logs apenas da API"
        echo "  logs-db   - Exibe logs apenas do banco"
        echo "  build     - Reconstrói as imagens dos containers"
        echo "  status    - Mostra status dos containers"
        echo "  clean     - Remove containers e volumes (CUIDADO!)"
        echo ""
        echo "Serviços:"
        echo "  🌐 API: http://localhost:8000"
        echo "  📚 Docs: http://localhost:8000/docs"
        echo "  🗃️  Adminer: http://localhost:8080"
        ;;
esac
