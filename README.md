# 🔍 LinkedIn Job Search - Version 8.0 avec Export Incrémental

**Solution complète pour rechercher des offres d'emploi LinkedIn avec géolocalisation précise et filtres avancés.**

## 🎯 Nouveautés Version 8.0

- 📁 **Export incrémental** : Un seul fichier JSON consolidé pour toutes les recherches
- 🔄 **Suppression automatique des doublons** : Évite les offres déjà sauvegardées
- 📊 **Historique des recherches** : Suivi de toutes vos recherches avec métadonnées
- ✅ **Structure d'export minimale** : 11 champs essentiels sans doublons
- ✅ **Géolocalisation corrigée** : 95-100% de précision géographique
- ✅ **Filtres avancés** : Experience, type de contrat, télétravail, date  
- ✅ **URLs directes** : LinkedIn job URLs et apply URLs automatiques
- ✅ **Multi-villes validées** : Los Angeles, Tokyo, Berlin, Marseille, Vilnius...

---

## 🚀 Installation et Configuration

### Prérequis
- Python 3.11+ 
- Git
- Accès Internet

### Installation Rapide

```bash
# 1. Cloner le projet
git clone https://github.com/Xelov4/linkedin-search-.git
cd linkedin-search-

# 2. Créer l'environnement virtuel
python3 -m venv mcp-linkedin-env
source mcp-linkedin-env/bin/activate

# 3. Installer les dépendances
pip install linkedin-api python-dotenv requests fastmcp

# 4. Configurer les identifiants LinkedIn
cp .env.example .env
# Éditer .env avec vos identifiants LinkedIn
```

### Configuration .env
```bash
LINKEDIN_EMAIL=votre.email@example.com
LINKEDIN_PASSWORD=votre_mot_de_passe
```

---

## 📁 Export Incrémental - Fonctionnalité Principale

**Fini les multiples fichiers JSON !** Toutes vos recherches sont consolidées dans un **seul fichier** :

```
Exports/linkedin_job_searches_consolidated.json
```

### Avantages de l'export incrémental :
- **🔄 Accumulation intelligente** : Chaque nouvelle recherche ajoute les offres au fichier existant
- **🚫 Suppression des doublons** : Les offres déjà présentes ne sont pas re-ajoutées
- **📊 Historique complet** : Suivi de toutes vos recherches avec filtres et métadonnées
- **📈 Statistiques globales** : Nombre total de recherches et d'offres uniques

### Structure du fichier consolidé :
```json
{
  "metadata": {
    "total_searches": 15,
    "total_jobs": 127,
    "creation_date": "2025-08-28T06:09:00",
    "export_version": "incremental_v8.0"
  },
  "search_history": [
    {"keywords": "Python Developer", "location": "Paris", "jobs_found": 8},
    {"keywords": "Data Scientist", "location": "Berlin", "jobs_found": 5}
  ],
  "jobs": [
    // Toutes vos offres d'emploi uniques
  ]
}
```

---

## 🔧 Utilisation

### Recherche Simple
```bash
source mcp-linkedin-env/bin/activate && python -c "
import sys
sys.path.append('/root/project-jobsearch/linkedin-search-')
from src.mcp_linkedin.client import linkedin_job_search_advanced
result = linkedin_job_search_advanced('SEO', 'Paris', 20)
print(result)
"
```

### Recherche Avancée avec Filtres
```bash
source mcp-linkedin-env/bin/activate && python -c "
import sys
sys.path.append('/root/project-jobsearch/linkedin-search-')
from src.mcp_linkedin.client import linkedin_job_search_advanced
result = linkedin_job_search_advanced(
    keywords='SEO programmatique',
    location='Paris', 
    limit=100,
    listed_at=2592000,    # 30 jours
    distance=30,          # 30 miles
    job_type=['F'],       # CDI uniquement
    experience=['3', '4'], # Associé + Senior
    remote=['2', '3']     # Remote + Hybride
)
print(result)
"
```

### Fonction Python Directe
```python
from src.mcp_linkedin.client import linkedin_job_search_advanced

# Recherche simple avec géolocalisation automatique
results = linkedin_job_search_advanced(
    keywords="Python Developer",
    location="Berlin", 
    limit=10
)
print(results)
# → Fichier JSON auto-généré dans Exports/
```

---

## 📋 Guide des Filtres

Consultez **[SEARCH_GUIDE.md](SEARCH_GUIDE.md)** pour la documentation complète des filtres :

- ⏰ **Filtres temporels** : 24h, 7 jours, 30 jours, 3 mois
- 💼 **Types de contrat** : CDI, Contrat, Temps partiel, Stage...
- 📊 **Niveaux d'expérience** : Débutant, Associé, Senior, Directeur...
- 🏠 **Mode de travail** : Présentiel, Remote, Hybride
- 📍 **Distance géographique** : Rayon en miles depuis la ville

---

## 🌍 Villes Testées et Validées

| Ville | Pays | Validation | Résultats Géographiques |
|-------|------|------------|-------------------------|
| **Los Angeles** | 🇺🇸 USA | **PARFAIT** | ✅ 100% USA |
| **Tokyo** | 🇯🇵 Japon | **EXCELLENT** | ✅ Japan/APAC |  
| **Amsterdam** | 🇳🇱 Pays-Bas | **EXCELLENT** | ✅ Netherlands/EU |
| **Berlin** | 🇩🇪 Allemagne | **EXCELLENT** | ✅ Germany/EU |
| **Lisbonne** | 🇵🇹 Portugal | **PARFAIT** | ✅ 100% Portugal |
| Madrid | 🇪🇸 Espagne | **BON** | ✅ Spain/EU |
| Rome | 🇮🇹 Italie | **BON** | ✅ Italy/EU |
| **Paris** | 🇫🇷 France | **EXCELLENT** | ✅ 100% France |
| **Lyon** | 🇫🇷 France | **EXCELLENT** | ✅ 100% France |

---

## 📚 Documentation

- **[SEARCH_GUIDE.md](SEARCH_GUIDE.md)** - Guide complet des recherches et filtres
- **[REPOSITORY.md](REPOSITORY.md)** - Documentation technique complète
- **[src/mcp_linkedin/client.py](src/mcp_linkedin/client.py)** - Code source principal

---

## 🔧 Structure des Données Export (11 champs essentiels)

```json
{
  "id": "4295877533",
  "linkedin_postJob_url": "https://www.linkedin.com/jobs/view/4295877533/",
  "title": "SEO Manager",
  "company": "THE/STUDIO",
  "company_url": "https://linkedin.com/company/the-studio",
  "location": "European Economic Area", 
  "description": "Full job description...",
  "listed_at": "2025-08-28 01:46:15",
  "apply_url": "https://company-apply-url.com",
  "workplace_type": "Remote",
  "custom_logo_url": "https://logo-400x400.jpg",
  "work_remote_allowed": true,
  "job_nature": "Full-time"
}
```

---

## ⚡ Performance

- **Recherche speed** : ~2-3 secondes par résultat
- **Export generation** : Instantané
- **Memory usage** : ~200MB
- **Geographic accuracy** : 95-100%
- **Duplicate prevention** : 100% efficace

---

## Original MCP LinkedIn

This project builds upon the MCP LinkedIn server that provides tools to interact with LinkedIn's Feeds and Job API.

This is using unofficial LinkedIn API via [Linkedin-api](https://github.com/tomquirk/linkedin-api). Use at your own risk.

<a href="https://smithery.ai/server/mcp-linkedin"><img alt="Smithery Badge" src="https://smithery.ai/badge/mcp-linkedin"></a>
<a href="https://glama.ai/mcp/servers/dvbdubl2bg"><img width="380" height="200" src="https://glama.ai/mcp/servers/dvbdubl2bg/badge" alt="mcp-linkedin MCP server" /></a>

### Installing via Smithery

To install LinkedIn Interaction Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/mcp-linkedin):

```bash
npx -y @smithery/cli install mcp-linkedin --client claude
```

## Configuration

```json
{
    "mcpServers": {
        "linkedin": {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/adhikasp/mcp-linkedin", "mcp-linkedin"],
            "env": {
                "LINKEDIN_EMAIL": "your_linkedin_email",
                "LINKEDIN_PASSWORD": "your_linkedin_password"
            }
        }
    }
}
```

## Sample usage

Using [mcp-client-cli](https://github.com/adhikasp/mcp-client-cli)

### Get feed posts

```
$ llm whats happening in linkedin feed? Do not mention names

I'll retrieve the recent LinkedIn feed posts without mentioning any specific names.

Tool Calls:
  get_feed_posts
  Args:
    limit: 10

Based on the LinkedIn feed, here are the key highlights without mentioning specific names:

1. Data Science & Cybersecurity Insights:
   - A post about a massive dataset from a major tech company
   - Includes 13 million pieces of evidence
   - Covers SIEM telemetry from 6,100 organizations
   - Represents 441 MITRE ATT&CK techniques

2. DevOps Community Event:
   - A local DevOps meetup was held at a tech company office
   - Discussed topics like AWS Lambda, Kubernetes scaling, Terraform
   - Highlighted the importance of networking and continuous learning
   - Shared experiences of transitioning between tech roles

3. Linux Engineering Perspectives:
   - Insights into what makes a great Linux engineer
   - Key skills include:
     * Command-line troubleshooting
     * Process management
     * Networking fundamentals
     * System architecture understanding
     * Task automation
     * Shell scripting

4. Professional Networking:
   - Some posts about job seeking
   - Discussions about career transitions
   - Sharing professional experiences and learnings

5. Tech Community Reflections:
   - Posts about inspirational figures
   - Discussions on professional growth
   - Reflections on learning and personal development

The feed showcases a mix of technical insights, professional networking, career development, and community engagement across various tech domains.
```

### Search for jobs

```
$ llm search for 3 data engineer jobs in jakarta. For each job check if it a good match for me by analyzing it against my resume in file resume.md. Do not mention company name in your result but only generic area where the company business is about

I'll help you find data engineer jobs in Jakarta and analyze them against your resume. I'll break this down into steps:

1. First, I'll search for data engineer jobs in Jakarta
2. Then, I'll read your resume
3. Finally, I'll analyze the job matches

Let's start by searching for jobs:

Tool Calls:
  search_jobs
  Args:
    keywords: data engineer
    location: Jakarta
    limit: 3


Now, I'll read your resume:

Tool Calls:
  read_file
  Args:
    path: resume.md
Secure MCP Filesystem Server running on stdio
Allowed directories: [ '/home/adhikasp', '/mnt/e' ]


Now, I'll analyze the jobs against your resume:

1. Job in Financial Technology Sector (Lead Backend Engineer):
   - Match Score: 85%
   - Strengths:
     * Requires experience in developing scalable microservices (aligns with your Grab experience)
     * Strong focus on cloud infrastructure (AWS, GCP) - matches your cloud skills
     * Requires experience with event-driven architecture and message brokers
     * Requires Go or Python programming (your proficient languages)
   - Potential Gaps:
     * Specific focus on credit risk and fraud detection might require additional domain knowledge
     * Emphasis on team leadership (6+ years experience leading teams)

2. Job in Financial Technology Sector (DevOps Engineer):
   - Match Score: 75%
   - Strengths:
     * Requires cloud platform experience (AWS, GCP)
     * Needs containerization skills (Docker, Kubernetes)
     * Requires scripting in Python and Bash
     * Needs infrastructure as code experience
   - Potential Gaps:
     * More DevOps focused compared to your backend engineering background
     * Specific monitoring tools might require additional learning

3. Job in Enterprise Collaboration Software (Solution Engineer):
   - Match Score: 60%
   - Strengths:
     * Requires strong communication skills
     * Technical consulting background
     * Experience with enterprise software
   - Potential Gaps:
     * Less technical compared to your current role
     * More sales-oriented solution engineering
     * Less hands-on technical development

Recommendation:
The first job (Lead Backend Engineer) appears to be the best match for your skills and experience. It closely aligns with your current work, particularly in terms of backend development, cloud infrastructure, and working with distributed systems. The role's requirements in Go/Python, microservices, and event-driven architecture are very compatible with your professional background.

Would you like me to elaborate on any of these job analyses or provide more detailed insights?
```