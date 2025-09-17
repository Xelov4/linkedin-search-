# 🔍 Guide de Recherche LinkedIn Jobs

## 🚀 Commande de Base

```bash
# Avec environnement virtuel (recommandé)
source mcp-linkedin-env/bin/activate && python -c "
import sys
sys.path.append('/root/project-jobsearch/linkedin-search-')
from src.mcp_linkedin.client import linkedin_job_search_advanced
result = linkedin_job_search_advanced('mots-clés', 'ville', limite, parametres...)
print(result)
"
```

## 📋 Paramètres Disponibles

### ✅ Paramètres Obligatoires
- **`keywords`** : Mots-clés de recherche (ex: "SEO", "developer", "marketing manager")
- **`location`** : Ville ou région (ex: "Paris", "Lyon", "Amsterdam")
- **`limit`** : Nombre de résultats (1-100)

### ⚙️ Paramètres Optionnels

#### 📅 Filtres Temporels
- **`listed_at`** : Limite de temps en secondes
  - `86400` = Dernières 24h
  - `604800` = Dernière semaine (défaut)
  - `2592000` = Dernier mois
  - `7776000` = Derniers 3 mois

#### 💼 Types de Contrat
- **`job_type`** : Liste des types
  - `["F"]` = CDI (Full-time)
  - `["C"]` = Contrat
  - `["P"]` = Temps partiel
  - `["T"]` = Temporaire
  - `["I"]` = Stage
  - `["V"]` = Bénévolat
  - `["O"]` = Autre

#### 📊 Niveaux d'Expérience
- **`experience`** : Liste des niveaux
  - `["1"]` = Stage
  - `["2"]` = Débutant
  - `["3"]` = Associé
  - `["4"]` = Intermédiaire/Senior
  - `["5"]` = Directeur
  - `["6"]` = Cadre supérieur

#### 🏠 Mode de Travail
- **`remote`** : Liste des modes
  - `["1"]` = Présentiel
  - `["2"]` = Télétravail
  - `["3"]` = Hybride

#### 📍 Distance Géographique
- **`distance`** : Rayon en miles (ex: `30`)

#### 🔧 Options Techniques
- **`use_enhanced_location`** : `True` (recommandé) / `False`

## 📝 Exemples Concrets

### Recherche Simple
```python
linkedin_job_search_advanced('SEO', 'Lyon', 20)
```

### Recherche avec Filtres Temporels
```python
linkedin_job_search_advanced('developer', 'Paris', 50, listed_at=86400)  # 24h
```

### Recherche avec Types de Contrat
```python
linkedin_job_search_advanced('marketing', 'Amsterdam', 30, job_type=["F", "C"])  # CDI + Contrat
```

### Recherche avec Niveau d'Expérience
```python
linkedin_job_search_advanced('product manager', 'Berlin', 25, experience=["4", "5"])  # Senior + Directeur
```

### Recherche Remote/Hybride
```python
linkedin_job_search_advanced('data scientist', 'Londres', 40, remote=["2", "3"])  # Remote + Hybride
```

### Recherche Complète (Tous Filtres)
```python
linkedin_job_search_advanced(
    keywords='SEO programmatique',
    location='Paris', 
    limit=100,
    listed_at=2592000,    # 30 jours
    distance=30,          # 30 miles
    job_type=["F"],       # CDI uniquement
    experience=["3", "4"], # Associé + Senior
    remote=["2", "3"]     # Remote + Hybride
)
```

## 💾 Export des Résultats

- **Fichier automatique** : `Exports/linkedin_job_searches_consolidated.json`
- **Format** : Export incrémental (évite les doublons)
- **Métadonnées** : Historique complet des recherches
- **Structure** : 11 champs essentiels par offre

## 🌍 Villes Testées

- **Paris**, Lyon, Marseille (France)
- **Amsterdam**, Berlin, Madrid (Europe)
- **Londres**, Lisbonne, Rome (Europe)
- **Tokyo**, Los Angeles (International)

## ⚡ Commande Complète Exemple

```bash
source mcp-linkedin-env/bin/activate && python -c "
import sys
sys.path.append('/root/project-jobsearch/linkedin-search-')
from src.mcp_linkedin.client import linkedin_job_search_advanced
result = linkedin_job_search_advanced(
    'SEO programmatique', 
    'Paris', 
    100, 
    listed_at=2592000,
    distance=30,
    job_type=['F'],
    experience=['3', '4'],
    remote=['2', '3']
)
print(result)
"
```