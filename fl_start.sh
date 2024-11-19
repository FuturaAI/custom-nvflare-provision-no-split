#!/bin/bash

# Funzione per lanciare un server specifico
launch_server() {
    local startup_path="$1"
    local site_name="$2"
    
    if [ ! -f "${startup_path}/start.sh" ]; then
        echo "Errore: File 'start.sh' non trovato in '${startup_path}'"
        return 1
    fi
    
    echo "$(date '+%H:%M:%S') - Avvio del server NVFlare per ${site_name}..."
    cd "$startup_path" && ./start.sh &
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
PROJECT_DIR="./workspace/${PROJECT_NAME}"
PROD_DIR="${PROJECT_DIR}/${PROD_NAME}"

# Verifica se la directory del progetto esiste
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Errore: Directory del progetto '${PROJECT_DIR}' non trovata!"
    exit 1
fi

# Verifica se la directory prod esiste
if [ ! -d "$PROD_DIR" ]; then
    echo "Errore: Directory prod '${PROD_DIR}' non trovata!"
    exit 1
fi

# Array dei siti da lanciare
SITES=("server1" "site-1" "site-2")

# Lancia tutti i server con un ritardo di 7 secondi tra loro
for site in "${SITES[@]}"; do
    STARTUP_PATH="${PROD_DIR}/${site}/startup"
    
    if [ ! -d "$STARTUP_PATH" ]; then
        echo "Errore: Directory di startup per ${site} non trovata: '${STARTUP_PATH}'"
        continue
    fi
    
    launch_server "$STARTUP_PATH" "$site"
    
    # Se non è l'ultimo elemento dell'array, aspetta 7 secondi
    if [ "$site" != "${SITES[-1]}" ]; then
        echo "Attendo 10 secondi prima di avviare il prossimo server..."
        sleep 10
    fi
done

echo "Tutti i server sono stati avviati!"

# Attendi che tutti i processi in background terminino
wait