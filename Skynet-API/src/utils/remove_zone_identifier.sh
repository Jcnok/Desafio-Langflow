#!/bin/bash

# Verifica se um diretório foi passado como argumento
if [ -z "$1" ]; then
    echo "Uso: $0 <diretório>"
    exit 1
fi

# Diretório a ser verificado
DIR=$1

# Verifica se o diretório existe
if [ ! -d "$DIR" ]; then
    echo "Diretório não encontrado: $DIR"
    exit 1
fi

# Encontra e remove arquivos com :Zone.Identifier
find "$DIR" -type f -name "*:Zone.Identifier" -exec rm -f {} \;

echo "Remoção dos arquivos ':Zone.Identifier' concluída em $DIR"

# comando para remover tudo ./src/utils/remove_zone_identifier.sh /home/jcnok/desafio_langflow/skynet/CRM-Skynet-Provider-SQLite_FastAPI/ 