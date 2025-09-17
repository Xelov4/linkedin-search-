# Structure des Dossiers - LinkedIn Search System

## 📁 Structure Correcte

```
search-system/
├── exports/
│   └── Exports/                           # ✅ DOSSIER PRINCIPAL D'EXPORT
│       ├── linkedin_job_searches_consolidated.json  # Fichier consolidé principal
│       └── *.json                         # Autres exports individuels
├── src/
│   └── mcp_linkedin/
│       └── client.py                      # Script principal (configuré pour exports/Exports)
├── scripts/
│   ├── generated_relaunch_script.py       # ✅ Corrigé
│   ├── complete_keyword_relaunch.py       # ✅ Corrigé
│   ├── analyze_consolidated.py            # ✅ Corrigé
│   ├── run_seo_search.py                  # ✅ Corrigé
│   └── demo_incremental.py                # ✅ Corrigé
└── docs/
```

## 🎯 Destination Unique des Exports

**TOUS les scripts utilisent maintenant le chemin unifié :**
```
exports/Exports/linkedin_job_searches_consolidated.json
```

## ✅ Scripts Corrigés

1. **src/mcp_linkedin/client.py** - Script principal
   - `exports_dir = "exports/Exports"`

2. **scripts/generated_relaunch_script.py** - Script de refresh automatique
   - Messages d'output corrigés

3. **scripts/analyze_consolidated.py** - Script d'analyse  
   - `consolidated_file = "exports/Exports/linkedin_job_searches_consolidated.json"`

4. **scripts/complete_keyword_relaunch.py** - Script générateur
   - Messages d'output corrigés

5. **scripts/run_seo_search.py** - Script de recherche SEO
   - Messages d'output corrigés

6. **scripts/demo_incremental.py** - Script de démonstration
   - Messages d'output corrigés

## 🚫 Problèmes Résolus

- ❌ Duplication dans `Exports/` (supprimé)
- ❌ Chemins incohérents entre scripts
- ❌ Confusion sur le dossier de destination

## 💡 Utilisation

Tous les scripts sauvegardent maintenant dans le même fichier :
```bash
exports/Exports/linkedin_job_searches_consolidated.json
```

Ce fichier unique contient toutes les recherches avec déduplication automatique.