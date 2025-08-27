# Workflow - Lancement du Script LinkedIn

## Prérequis
• Installer Python 3.7+ sur votre système
• Avoir un compte LinkedIn avec email et mot de passe
• Cloner le repository du projet

## Configuration
• Créer un fichier `.env` à la racine du projet
• Ajouter vos credentials LinkedIn : `LINKEDIN_EMAIL=jihad.ejjilali@gmail.com` et `LINKEDIN_PASSWORD=bikini23`
• Installer les dépendances : `pip install -r requirements.txt` ou `pip install linkedin-api fastmcp python-dotenv`

## Lancement du Script
• Ouvrir un terminal dans le dossier `linkedin-search-`
• Activer l'environnement virtuel : `source venv/bin/activate`
• Lancer le script : `python src/mcp_linkedin/client.py`

## Résultats
• Le script recherche automatiquement 50 offres d'emploi à Saint-Denis (France)
• Les résultats s'affichent dans la console
• Un fichier JSON complet est créé dans le dossier `Exports/`
• Le fichier contient toutes les données disponibles de l'API LinkedIn

## Personnalisation
• Modifier les paramètres dans la fonction `search_jobs_direct()` du script
• Changer les mots-clés, la localisation ou le nombre d'offres selon vos besoins
• Les variables sont dans la dernière ligne du script principal

## Dépannage
• Vérifier que le fichier `.env` est bien créé et contient vos credentials
• S'assurer que l'environnement virtuel est activé
• Contrôler que toutes les dépendances sont installées
• Vérifier votre connexion internet et l'accès à LinkedIn
