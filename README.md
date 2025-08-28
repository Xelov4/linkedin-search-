# 🔍 LinkedIn Job Search - Version 7.0 avec Docker

**Une solution complète pour rechercher des offres d'emploi LinkedIn avec géolocalisation précise et déploiement Docker simplifié.**

## 🎯 Nouveautés Version 7.0

- 🐳 **Docker natif** : Déploiement one-click sur n'importe quel système
- ✅ **Structure d'export minimale** : 11 champs essentiels sans doublons
- ✅ **Géolocalisation corrigée** : 95-100% de précision géographique
- ✅ **Filtres avancés** : Experience, type de contrat, télétravail, date  
- ✅ **URLs directes** : LinkedIn job URLs et apply URLs automatiques
- ✅ **Multi-villes validées** : Los Angeles, Tokyo, Berlin, Marseille, Vilnius...

---

## 🐳 Démarrage Docker (Recommandé)

### Installation Ultra-Rapide
```bash
# 1. Cloner le projet
git clone https://github.com/Xelov4/linkedin-search-.git
cd linkedin-search-

# 2. Configurer les identifiants LinkedIn
cp .env.example .env
# Éditer .env avec vos identifiants LinkedIn

# 3. Lancer l'application
./run-docker.sh
```

### Recherches One-Shot
```bash
# Exemples de recherche directe
./run-docker.sh search "product manager" "Paris" 10
./run-docker.sh search "SEO specialist" "Los Angeles" 15 "F,C"
./run-docker.sh search "data scientist" "Berlin" 5
```

## 🚀 Installation Traditionnelle

```bash
# 1. Cloner le projet
git clone [URL_DU_REPO]
cd linkedin-search-

# 2. Installer les dépendances  
pip install linkedin-api fastmcp python-dotenv requests

# 3. Configurer vos identifiants LinkedIn
echo "LINKEDIN_EMAIL=votre.email@example.com" > .env
echo "LINKEDIN_PASSWORD=votre_mot_de_passe" >> .env

# 4. Lancer une recherche
python -c "from src.mcp_linkedin.client import linkedin_job_search; print(linkedin_job_search('SEO', 'Amsterdam', 5))"
```

### Fonction Principale (Recommandée)

```python
from src.mcp_linkedin.client import linkedin_job_search

# Recherche simple avec géolocalisation automatique
results = linkedin_job_search(
    keywords="Python Developer",
    location="Berlin", 
    limit=10
)
print(results)
# → Fichier JSON auto-généré dans Exports/
```

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

---

## 📖 Documentation Complète

Consultez [workflow.md](workflow.md) pour :
- Guide d'installation détaillé
- Exemples d'utilisation avancés
- Structure des données JSON
- Résolution de problèmes
- Scripts de production

---

## 🐳 Docker Documentation

Pour des instructions Docker complètes, consultez **[DOCKER.md](DOCKER.md)** qui inclut :

- 🚀 Guide de démarrage rapide Docker
- 🔧 Configuration avancée et options
- 📝 Exemples d'utilisation interactifs et one-shot
- 🐚 Accès shell et commandes de gestion
- 🔍 Dépannage et optimisations
- 🏗️ Intégrations CI/CD et Kubernetes

### Commandes Essentielles
```bash
# Lancement interactif
./run-docker.sh

# Recherche directe  
./run-docker.sh search "DevOps engineer" "Amsterdam" 20 "F"

# Gestion du container
./run-docker.sh logs    # Voir les logs
./run-docker.sh shell   # Accès terminal
./run-docker.sh stop    # Arrêter
./run-docker.sh clean   # Nettoyer
```

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
