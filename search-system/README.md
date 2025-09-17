# 🔍 LinkedIn Job Search System

## 📋 Vue d'Ensemble

Module autonome pour effectuer des recherches d'emploi sur LinkedIn avec géolocalisation précise et filtres avancés. Ce système génère des fichiers JSON consolidés avec suppression automatique des doublons.

## 🚀 Installation

```bash
# 1. Aller dans le module search-system
cd search-system

# 2. Activer l'environnement virtuel
source venv/bin/activate

# 3. Configurer les identifiants LinkedIn
cp .env.example .env
# Éditer .env avec vos identifiants LinkedIn
```

## 🔧 Utilisation

### Recherche Simple
```bash
source venv/bin/activate && python -c "
import sys
sys.path.append('src')
from mcp_linkedin.client import linkedin_job_search_advanced
result = linkedin_job_search_advanced('SEO', 'Paris', 20)
print(result)
"
```

### Recherche Avancée
```bash
source venv/bin/activate && python -c "
import sys
sys.path.append('src')
from mcp_linkedin.client import linkedin_job_search_advanced
result = linkedin_job_search_advanced(
    keywords='SEO Manager',
    location='Paris', 
    limit=50,
    listed_at=86400,      # 24h
    distance=20,          # 20 miles
    job_type=['F', 'C'],  # CDI + Contrat
    use_enhanced_location=True
)
print(result)
"
```

### Scripts Disponibles

```bash
# Script de recherche SEO automatisé
python scripts/run_seo_search.py

# Analyse des données consolidées
python scripts/analyze_consolidated.py

# Démonstration du système incrémental
python scripts/demo_incremental.py
```

## 📁 Structure

```
search-system/
├── src/
│   └── mcp_linkedin/          # API LinkedIn
│       ├── __init__.py
│       └── client.py          # Fonctions de recherche
├── scripts/
│   ├── run_seo_search.py      # Script de recherche SEO
│   ├── analyze_consolidated.py # Analyse des données
│   └── demo_incremental.py    # Démo système incrémental
├── exports/
│   └── linkedin_job_searches_consolidated.json # Données consolidées
├── venv/                      # Environnement virtuel Python
├── docs/                      # Documentation complète
│   ├── README.md             # Documentation principale
│   ├── SEARCH_GUIDE.md       # Guide des recherches
│   └── REPOSITORY.md         # Documentation technique
├── .env                      # Variables d'environnement
└── .env.example             # Exemple de configuration
```

## 📊 Export des Données

Les résultats sont automatiquement sauvegardés dans :
```
exports/linkedin_job_searches_consolidated.json
```

Format JSON avec :
- **Métadonnées** : Statistiques globales
- **Historique** : Toutes les recherches effectuées  
- **Jobs** : Offres d'emploi uniques (sans doublons)

## 🔗 Intégration avec Job Tracker

Ce module génère des données JSON qui peuvent être importées dans l'application job-tracker via :

```bash
# Depuis le module job-tracker
npm run import -- ../search-system/exports/linkedin_job_searches_consolidated.json
```

## 📚 Documentation

- **[SEARCH_GUIDE.md](docs/SEARCH_GUIDE.md)** - Guide complet des recherches
- **[REPOSITORY.md](docs/REPOSITORY.md)** - Documentation technique détaillée
- **[client.py](src/mcp_linkedin/client.py)** - Code source principal

---

*Module de recherche LinkedIn pour le projet Job Tracker*