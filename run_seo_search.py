#!/usr/bin/env python3
"""
Script pour recherche SEO directe avec tous les filtres demandés.
Critères: SEO à Paris, CDI ou Contract, 30 derniers jours, 20 miles max, 100 résultats
"""

import sys
import os
from datetime import datetime

# Ajouter le chemin vers le module
sys.path.append('/root/project-jobsearch/linkedin-search-')

try:
    from src.mcp_linkedin.client import linkedin_job_search_advanced
    print("✅ Module LinkedIn importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

def run_advanced_seo_search():
    """Recherche SEO avec tous les critères spécifiés."""
    print("🔍 RECHERCHE SEO AVANCÉE - Paris")
    print("=" * 50)
    
    # Critères demandés
    keywords = "SEO"
    location = "Paris"
    limit = 100
    job_type = ["F", "C"]          # CDI (Full-time) + Contract
    remote = ["1", "2", "3"]       # Tous types (On-site, Remote, Hybrid)
    listed_at = 2592000            # 30 jours (2592000 secondes)
    distance = 20                  # 20 miles max
    
    print(f"📋 Critères de recherche :")
    print(f"   🎯 Mots-clés: {keywords}")
    print(f"   📍 Lieu: {location}")
    print(f"   📊 Nombre souhaité: {limit}")
    print(f"   💼 Types de contrat: CDI + Contract")
    print(f"   🏠 Mode travail: Tous (Présentiel, Télétravail, Hybride)")
    print(f"   📅 Période: 30 derniers jours")
    print(f"   📏 Distance max: {distance} miles")
    
    print(f"\n🚀 Lancement de la recherche...")
    start_time = datetime.now()
    
    try:
        results = linkedin_job_search_advanced(
            keywords=keywords,
            location=location,
            limit=limit,
            experience=None,           # Tous niveaux d'expérience
            job_type=job_type,         # CDI + Contract
            remote=remote,             # Tous modes de travail
            listed_at=listed_at,       # 30 jours
            distance=distance,         # 20 miles
            use_enhanced_location=True # Géolocalisation précise
        )
        
        search_time = (datetime.now() - start_time).total_seconds()
        
        print(f"\n✅ Recherche terminée en {search_time:.1f} secondes")
        print(f"📄 Résultats console :")
        print("-" * 40)
        print(results)
        
        # Analyser le fichier consolidé résultant
        print(f"\n📊 ANALYSE DU FICHIER CONSOLIDÉ")
        print("=" * 50)
        
        try:
            from analyze_consolidated import analyze_consolidated_file
            analyze_consolidated_file()
        except:
            print("⚠️ Script d'analyse non disponible, vérifiez manuellement le fichier:")
            print("   Exports/linkedin_job_searches_consolidated.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        
        # Si erreur CHALLENGE, expliquer
        if "CHALLENGE" in str(e):
            print(f"\n💡 Explication de l'erreur CHALLENGE:")
            print("   - LinkedIn a détecté des recherches automatisées")
            print("   - Protection anti-bot activée temporairement")
            print("   - Solutions :")
            print("     1. Attendre 15-30 minutes")
            print("     2. Utiliser des credentials différents")
            print("     3. Réduire la fréquence des recherches")
        
        return False

if __name__ == "__main__":
    try:
        success = run_advanced_seo_search()
        if not success:
            print(f"\n⚠️ Recherche échouée, mais le système fonctionne correctement")
    except KeyboardInterrupt:
        print(f"\n⏹️ Recherche interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()