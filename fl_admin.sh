#!/bin/bash

# Funzione per lanciare l'admin console
launch_admin() {
    local startup_path="$1"
    local admin_script="${startup_path}/fl_admin.sh"
    
    if [ ! -f "$admin_script" ]; then
        echo "Errore: File 'fl_admin.sh' non trovato in '${startup_path}'"
        return 1
    fi
    
    echo "$(date '+%H:%M:%S') - Avvio della console admin NVFlare..."
    cd "$startup_path" && ./fl_admin.sh
}

# Verifica se sono stati forniti entrambi i parametri
if [ $# -ne 2 ]; then
    echo "Errore: Necessari sia il nome del progetto che la directory prod!"
    echo "Uso: $0 <nome_progetto> <prod_directory>"
    echo "Esempio: $0 test1 prod_00"
    exit 1
fi

PROJECT_NAME="$1"
PROD_NAME="$2"
BASE_DIR=$(pwd)
ADMIN_DIR="${BASE_DIR}/workspace/${PROJECT_NAME}/${PROD_NAME}/admin@nvidia.com/startup"

# Verifica se la directory admin esiste
if [ ! -d "$ADMIN_DIR" ]; then
    echo "Errore: Directory admin '${ADMIN_DIR}' non trovata!"
    exit 1
fi

# Lancia la console admin
launch_admin "$ADMIN_DIR"