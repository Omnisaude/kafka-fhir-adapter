#!/bin/bash

# Função para lidar com erros e sair do script
handle_error() {
    echo "Erro: $1" >&2
    exit 1
}

# Função para criar diretório com tratamento de erro
create_directory() {
    if ! mkdir -p "$1"; then
        handle_error "Não foi possível criar o diretório $1"
    fi
}

# Função para clonar o repositório com tratamento de erro
clone_repository() {
    if ! git clone "$1" "$2"; then
        handle_error "Falha ao clonar o repositório $1"
    fi
}

# Verifica se o diretório output existe, se não, cria
if [ ! -d "output" ]; then
    create_directory "output"
    echo "Diretório 'output' criado com sucesso."
else
    echo "Diretório 'output' já existe."
fi

# Verifica se o diretório do servidor já existe, se não, clona o repositório
if [ ! -d "output/hapi-fhir-jpaserver-starter" ]; then
    echo "Clonando repositório hapi-fhir-jpaserver-starter..."
    clone_repository "https://github.com/hapifhir/hapi-fhir-jpaserver-starter" "output/hapi-fhir-jpaserver-starter"
    echo "Repositório clonado com sucesso."
else
    echo "Diretório hapi-fhir-jpaserver-starter já existe."
fi

# Verifica se o arquivo ROOT.war existe, se não, compila o projeto
if [ ! -f "output/hapi-fhir-jpaserver-starter/target/ROOT.war" ]; then
    echo "Compilando o projeto..."
    cd output/hapi-fhir-jpaserver-starter || handle_error "Não foi possível acessar o diretório do projeto"
    if ! mvn clean package -DskipTests; then
        handle_error "Falha ao compilar o projeto. Verifique se o Maven está instalado corretamente."
    fi
    echo "Projeto compilado com sucesso."
    cd ../.. || handle_error "Não foi possível retornar ao diretório original"
else
    echo "Arquivo ROOT.war já existe."
fi

# Executa o servidor
echo "Iniciando o servidor..."
if ! java -jar output/hapi-fhir-jpaserver-starter/target/ROOT.war; then
    handle_error "Falha ao iniciar o servidor. Verifique se o Java está instalado corretamente."
fi

echo "Servidor iniciado!"
