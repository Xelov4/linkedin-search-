#!/usr/bin/env python3
"""
Script de démonstration de la nouvelle logique incrémentale.
Simule plusieurs recherches LinkedIn avec l'API réelle.
"""

import sys
import os
import time

# Ajouter le chemin vers le module
sys.path.append('/root/project-jobsearch/linkedin-search-')

try:
    from src.mcp_linkedin.client import linkedin_job_search
    print("✅ Module LinkedIn importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("🐳 Utilisation recommandée : ./run-docker.sh")
    sys.exit(1)

def demo_incremental_searches():
    """Démonstration de recherches incrémentales."""
    print("🔍 DÉMONSTRATION - Export JSON Incrémentale")
    print("=" * 55)
    print("Cette démonstration effectue plusieurs recherches LinkedIn")
    print("et montre comment elles sont consolidées dans un seul fichier JSON.")
    print()
    
    # Recherches de démonstration
    searches = [
        {
            "keywords": "Python Developer", 
            "location": "Paris", 
            "limit": 3,
            "desc": "Développeurs Python à Paris"
        },
        {
            "keywords": "Data Scientist", 
            "location": "Berlin", 
            "limit": 2,
            "desc": "Data Scientists à Berlin"
        },
        {
            "keywords": "SEO Manager", 
            "location": "Amsterdam", 
            "limit": 2,
            "desc": "SEO Managers à Amsterdam"
        }
    ]
    
    print(f"📋 Recherches programmées : {len(searches)}")
    for i, search in enumerate(searches, 1):
        print(f"  {i}. {search['desc']} (max {search['limit']} offres)")
    
    input("\n⏸️  Appuyez sur Entrée pour commencer les recherches...")
    
    for i, search in enumerate(searches, 1):
        print(f"\n🔄 Recherche {i}/{len(searches)}: {search['desc']}")
        print("-" * 40)
        
        try:
            result = linkedin_job_search(
                keywords=search['keywords'],
                location=search['location'], 
                limit=search['limit']
            )
            print(f"✅ Recherche terminée")
            
            # Pause entre les recherches pour éviter le rate limiting
            if i < len(searches):
                print("⏳ Pause de 5 secondes...")
                time.sleep(5)
                
        except Exception as e:
            print(f"❌ Erreur lors de la recherche: {e}")
            continue
    
    print(f"\n🎉 Démonstration terminée !")
    print("📄 Vérifiez le fichier consolidé :")
    print("   exports/Exports/linkedin_job_searches_consolidated.json")
    print("\n💡 Ce fichier contient maintenant toutes vos recherches")
    print("   avec suppression automatique des doublons !")

if __name__ == "__main__":
    try:
        demo_incremental_searches()
    except KeyboardInterrupt:
        print("\n\n⏹️  Démonstration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        sys.exit(1)