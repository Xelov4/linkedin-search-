#!/usr/bin/env python3
"""
Script de test simple pour vérifier la connexion LinkedIn.
"""

import sys

# Ajouter le chemin vers le module
sys.path.append('/root/project-jobsearch/linkedin-search-')

try:
    from src.mcp_linkedin.client import linkedin_job_search_advanced
    print("✅ Module LinkedIn importé avec succès")
    
    # Test simple avec un seul mot-clé
    print("🧪 Test avec 'SEO' à Paris, limite 3...")
    result = linkedin_job_search_advanced(
        keywords="SEO",
        location="Paris",
        limit=3,
        job_type=["F"],  # Full-time seulement
        listed_at=604800,  # Dernière semaine
        use_enhanced_location=True
    )
    print("✅ Test réussi !")
    print("🎯 Le système est prêt pour lancer le script complet.")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("🔧 Installez les dépendances manquantes:")
    print("   pip install linkedin-api python-dotenv fastmcp")
    sys.exit(1)
    
except Exception as e:
    print(f"⚠️  Erreur lors du test: {e}")
    print("📋 Vérifiez vos identifiants LinkedIn dans le fichier .env")
    sys.exit(1)