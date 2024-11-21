# Custom NVFlare Provision Documentation

## Overview
Questo progetto implementa un sistema di federated learning utilizzando NVIDIA FLARE. La struttura è organizzata per guidare lo sviluppo dal test locale fino all'implementazione federata, seguendo un approccio step-by-step.

## Adattabilità del Sistema
Gli script e i componenti presenti nel progetto sono configurati come esempio per un dataset di immagini specifico presente nella cartella 'images'. Tuttavia, la struttura è progettata per essere facilmente adattabile a diversi tipi di dati e problemi. 

## Workflow

### 1. Setup Iniziale
Il primo passo prevede la creazione della struttura del progetto e la distribuzione del dataset tra i vari server/client (nvflare) e notebooks. Il dataset di partenza deve essere organizzato nella cartella 'images' seguendo una struttura predefinita.

### 2. Fase di Sviluppo
Utilizzo dei notebook di training per lo sviluppo e il test locale. In questa fase si definisce l'architettura del modello, si configurano le trasformazioni del dataset e si verifica il corretto funzionamento del training.

### 3. Implementazione Federata
Una volta validato il modello localmente, il codice viene adattato alla struttura richiesta da NVFlare utilizzando i template presenti nella cartella pt/. Questa fase richiede particolare attenzione nell'allineamento dei nomi delle classi e dei percorsi.

### 4. Training Distribuito
Il training federato viene gestito attraverso l'admin console di NVFlare, che permette di monitorare e controllare l'intero processo di training distribuito.

### 5. Validazione
La fase finale prevede la validazione del modello federato utilizzando i notebook di inferenza, disponibili sia per il training standard che per quello con crittografia omomorfica.

## Note Importanti
- È fondamentale seguire l'ordine sequenziale delle operazioni
- Il codice presente in pt/ serve come riferimento da adattare
- Si consiglia di testare approfonditamente ogni componente in locale
- La struttura dei nomi e dei percorsi deve essere mantenuta coerente

## Setup NVFlare 

## Descrizione
Script di automazione per la creazione e configurazione di nuovi progetti NVFlare. Lo script gestisce automaticamente il processo di provisioning e la configurazione iniziale del progetto, **inclusa la gestione della distribuzione dei dataset di immagini**.

## Prerequisiti
- Python 3.x
- Install dependencies: 
```bash
   pip install -r requirements.txt
   ```
- File richiesti nella stessa cartella:
  - `project_builder.py`
  - `preconfig_project_folders.py`
  - `prebuild_images_split.py`
  - Directory `images` contenente le immagini da distribuire (train, val, test), le immagini devono essere divise in cartelle con il nome della label come nell'esempio

## Come Utilizzare lo Script

### Sintassi Base
```bash
./launch_provision.sh <nome_progetto>
```

### Esempio Pratico
```bash
./launch_provision.sh progetto_ml
```

### Passaggi Eseguiti dallo Script
1. Crea un nuovo progetto con il nome specificato
2. Genera il file di configurazione `nvflare_project_config_<nome_progetto>.yml`
3. Esegue il provisioning NVFlare
4. Configura la struttura delle cartelle del progetto
5. Esegue la distribuzione delle immagini tra i siti

### Output Atteso
Lo script creerà:
- Una nuova directory del progetto
- File di configurazione necessari
- Struttura base delle cartelle per NVFlare
- Directory di immagini suddivise per ogni client

### Struttura delle Directory per le Immagini
```
workspace/
└── nome_progetto/
    └── prod_XX/
        ├── localhost/
        │   └── local/
        │       └── images/
        │           └── split_images/
        ├── site-1/
        │   └── local/
        │       └── images/
        │           └── split_images/
        └── site-2/
            └── local/
                └── images/
                    └── split_images/
```

## Gestione delle Risorse
Lo script configura automaticamente le risorse per ogni client:
- Aggiorna i file `resources.json` per ogni client
- Configura l'utilizzo della GPU (1 GPU per client)
- Gestisce l'allocazione della memoria GPU

## Note Importanti
- Eseguire lo script dalla directory dove sono presenti i file di supporto
- Il nome del progetto non deve contenere spazi
- Attendere il completamento di tutti i passaggi prima di utilizzare il progetto
- Verificare che la directory `images` sia presente prima dell'esecuzione

## Struttura Moduli PyTorch (pt/)

### Descrizione
La directory `pt` contiene i componenti per l'implementazione del federated learning con PyTorch da utilizzare con NVFlare. La struttura presente è un esempio di riferimento che mostra come organizzare il codice dopo averlo testato nei notebook.

### Workflow di Sviluppo
1. Il codice viene inizialmente sviluppato e testato nei notebook (`notebooks/`)
2. Una volta validata l'implementazione nei notebook standalone
3. Si crea la struttura appropriata in `pt/` per l'integrazione con NVFlare
4. I componenti in `pt/` vengono utilizzati esclusivamente per il training federato

### Struttura e Funzionalità

#### 1. Utils (utils/)
Contiene gli strumenti per la gestione dei dati:
- **Gestione Dataset**: Implementazione del dataset personalizzato in custom_data.py per il caricamento e la gestione delle immagini
- **Utility Generali**: Funzioni di supporto e costanti utilizzate nel progetto

#### 2. Networks (networks/)
Contiene le implementazioni delle reti neurali:
- Definizione dell'architettura della rete
- Configurazione dei layer
- Parametri del modello

#### 3. Learners (learners/)
Gestisce la logica di training:
- Implementazione del training loop
- Gestione della validazione
- Integrazione con NVFlare per il federated learning
- Configurazione dei parametri di training

### Note Importanti
- Il codice presente è un esempio di riferimento
- Lo sviluppo iniziale avviene nei notebook standalone
- I componenti in `pt/` sono specifici per NVFlare
- La struttura segue le convenzioni richieste da NVFlare

## Configurazione dei Job

### Job Builder Base

### Descrizione
Script Python per la configurazione automatica dei job di training federated. Gestisce la configurazione del server e dei client, impostando parametri di training e workflow di federated learning.

### Prerequisiti
- File di configurazione `config/job_builder_setup.json`
- Moduli personalizzati:
  - `pt.networks.nets`
  - `pt.learners.custom_learner`
  - `pt.utils.custom_data`

### Utilizzo
```bash
python job_builder.py
```
Lo script chiederà interattivamente:
1. Il nome del progetto
2. La sottodirectory del progetto (es. 'prod_00')

### Input Richiesti
```
Insert the project name, must be the same name of a folder in the workspace:
> test1

Insert the project sub dir (e.g. 'prod_00'):
> prod_00
```

### Componenti Configurati
1. **Server**:
   - Model persistor
   - Aggregator per i modelli
   - Model selector e locator
   - Workflow di Scatter and Gather
   - Cross-site model evaluation

2. **Client**:
   - Custom learner per training
   - Executor per task di training e validazione
   - Configurazione risorse GPU

### Output
- Genera i file di configurazione dei job nella directory:
  ```
  workspace/<nome_progetto>/<project_sub_dir>/admin@nvidia.com/transfer/jobs
  ```

### Parametri Principali
- `NUM_ROUNDS`: Numero di round di training
- `AGGREGATION_EPOCHS`: Epoche per aggregazione
- `min_clients`: Numero minimo di client richiesti
- Configurazione GPU per ogni client (1 GPU, 1GB memoria)

### Note sulla Configurazione
- I parametri di training sono configurabili nel file `job_builder_setup.json`
- La configurazione include setup per training distribuito e validazione cross-site
- Risorse GPU vengono allocate automaticamente per ogni client
- Il percorso di output dipende dalla sottodirectory specificata

### Job Builder con Crittografia Omomorfica (HE)
È disponibile una versione alternativa del job builder che implementa la crittografia omomorfica per una maggiore sicurezza durante il training federato.

```bash
python job_builder_HE.py
```

#### Caratteristiche HE
- Utilizza `HEModelShareableGenerator` per la generazione sicura dei modelli condivisi
- Implementa filtri di serializzazione specifici per HE
- Aggiunge componenti di crittografia/decrittografia per client e server
- Configura aggregatori specifici per HE (`HEInTimeAccumulateWeightedAggregator`)

### ⚠️ Punti di Attenzione

#### 1. Configurazione dei Job
Quando si configurano i job (in `job_builder.py` o `job_builder_HE.py`), i nomi delle classi e i percorsi devono corrispondere esattamente alla struttura presente in `pt/`:

```python
# Questi import devono corrispondere alla struttura attuale
from pt.networks.nets import CustomModel
from pt.learners.custom_learner import CustomLearner
from pt.utils.custom_data import CustomDataset
```

#### 2. Trasformazioni Dataset
Le trasformazioni attuali nel codice sono specifiche per il dataset di esempio (immagini in scala di grigi):
```python
transforms_train = [
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((224, 224)),
    # altre trasformazioni specifiche per immagini in scala di grigi
]
```

⚠️ Queste trasformazioni **devono essere modificate** in base al proprio dataset:
- Adattare le dimensioni di resize
- Modificare il numero di canali (es. 3 per RGB)
- Aggiustare la normalizzazione in base alle statistiche del dataset
- Personalizzare le augmentation in base al tipo di dati
- Rimuovere trasformazioni non pertinenti

[Il resto della documentazione su Admin Console e Notebooks avanzati rimane invariato...]