#!/bin/bash

# Diretório onde os arquivos JSON estão localizados
DIR="resources"

# Função para lidar com erros
handle_error() {
    echo "Erro: $1" >&2
    exit 1
}

# Verifica se o diretório existe
if [ ! -d "$DIR" ]; then
    handle_error "O diretório $DIR não existe."
fi

# Verifica se jq está instalado
if ! command -v jq &> /dev/null; then
    handle_error "jq não está instalado. Por favor, instale-o com: sudo apt-get install jq"
fi

# Função para enviar um recurso
send_resource() {
    local file=$1
    local resource=$(basename "$file" | cut -d'-' -f1)
    local id=$(jq -r '.id' "$file")

    if [ -z "$id" ] || [ "$id" == "null" ]; then
        echo "Aviso: ID não encontrado no arquivo $file, pulando..."
        return
    fi

    echo "Enviando $file para localhost:8080/fhir/$resource/$id"

    response=$(curl -X PUT "http://localhost:8080/fhir/$resource/$id" \
         -H "Content-Type: application/json" \
         -d @"$file" \
         -w "\n%{http_code}")

    http_status=$(echo "$response" | tail -n1)

    if [ "$http_status" -ge 200 ] && [ "$http_status" -lt 300 ]; then
        echo "Sucesso! Código de status: $http_status"
    else
        echo "Falha ao enviar $file. Código de status: $http_status"
        echo "Resposta:"
        echo "$response" | sed '$d'
    fi

    echo "----------------------------------------"
}

# Ordem de inserção dos recursos
resources_order=(
    "Organization"
    "Location"
    "Patient"
    "Practitioner"
    "PractitionerRole"
    "Encounter"
    "Observation"
    "AllergyIntolerance"
    "Condition"
    "Procedure"
    "Medication"
    "MedicationStatement"
)

# Itera sobre a ordem dos recursos
for resource in "${resources_order[@]}"; do
    for file in "$DIR"/$resource-*.json; do
        if [ -f "$file" ]; then
            send_resource "$file"
        fi
    done
done

echo "Todos os arquivos foram processados."