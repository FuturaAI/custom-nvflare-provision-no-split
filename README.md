# Guida Step-by-Step

**N.B.** 
Questa guida include una fase iniziale di sviluppo e test locale che può essere saltata se si desidera utilizzare direttamente la configurazione di esempio già presente nel progetto.

**Documentazione**
Per una spiegazione dettagliata di ogni componente e processo, consultare il file `DOCS.md`. Si consiglia di farvi riferimento in caso di dubbi o per approfondimenti su specifiche funzionalità.

## 1. Sviluppo e Test Locale
### A. Test nel Notebook
```
notebooks/local_training.ipynb
```
- Sviluppa e testa l'architettura del modello
- Configura le trasformazioni del dataset
- Verifica il pipeline di training
- Valida le performance del modello
- Testa l'inferenza locale

### B. Struttura del Progetto
Il codice testato va organizzato nella struttura `pt/`:
```
pt/
├── learners/      # Implementa la logica di training
├── networks/      # Porta l'architettura del modello
└── utils/         # Contiene custom_data.py per la gestione del dataset
```
- Assicurati che i nomi delle classi corrispondano a quelli usati nei job builder
- Verifica che i path siano corretti

## 2. Setup Iniziale del Progetto

- Creare l'environment di sviluppo e installare i moduli python necessari:
```bash
python3 -m venv .venv
pip install -r requirements.txt
```

```bash
# Eseguire il setup del progetto
./launch_provision.sh <nome_progetto>
```

- Verifica che la directory `images` sia presente con la struttura corretta
- Controlla il completamento di tutte le operazioni di setup
- Verifica la creazione delle directory in workspace

## 3. Verifica delle Directory Generate
```
workspace/
└── nome_progetto/
    └── prod_00/
        ├── localhost/
        ├── site-1/
        └── site-2/
```
- Controlla che le immagini siano state correttamente distribuite
- Verifica la presenza dei file di configurazione

## 4. Avvio dei Server
```bash
# Avviare i server in ordine
./fl_start.sh <nome_progetto> prod_00
```
- Attendi il completamento dell'avvio di ogni server
- Verifica che tutti i server siano attivi

## 5. Accesso Admin Console
```bash
# Avviare la console di amministrazione
./fl_admin.sh <nome_progetto> prod_00
```
- Inserire "admin@nvidia.com" come default username
- Verifica la connessione di tutti i client con `check all`

## 6. Configurazione e Sottomissione Job
```bash
# Generare la configurazione del job
python job_builder.py        # Per training standard
# oppure
python job_builder_HE.py     # Per training con crittografia omomorfica

# Nella console admin
submit_job job_name
```

## 7. Monitoraggio Training
Nella console admin:
- Usa `check_status job_id` per monitorare il progresso
- Controlla i log per eventuali errori
- Monitora le metriche di training

## 8. Download e Validazione Risultati
```bash
# Nella console admin
download_job job_id
```
- I risultati saranno in `workspace/<nome_progetto>/prod_00/admin@nvidia.com/transfer`
- Utilizza i notebook in `notebooks/advanced/` per la validazione:
  - `nvflare_inference.ipynb` per modelli standard
  - `nvflare_inference_HE.ipynb` per modelli con HE

## 9. Chiusura Corretta
Nella console admin:
```bash
# Chiusura in ordine
shutdown client site-1
shutdown client site-2
shutdown server
```

## Note Importanti
- Segui l'ordine esatto degli step
- Verifica il completamento di ogni fase prima di procedere
- Controlla i log in caso di errori
- Backup dei risultati importanti prima della chiusura

## Troubleshooting
- Controlla `/tmp/nvflare/` per log dettagliati
- Verifica lo stato dei server con `check all`
- In caso di errori, riavvia i server in ordine
- Verifica i path nei file di configurazione

## Inferenza con NVFlare
Per i dettagli completi sulla fase di inferenza e validazione dei modelli addestrati, fare riferimento al README.md nella cartella `notebooks/advanced_nvflare/`:
- Struttura e utilizzo delle cartelle `models/` e `tenseal_context/`
- Differenze tra inferenza standard e HE
- Gestione dei path e dei contesti di crittografia
- Note importanti sulla validazione dei modelli

Per maggiori dettagli consultare:
```
notebooks/advanced_nvflare/README.md
```