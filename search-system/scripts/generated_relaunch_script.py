#!/usr/bin/env python3
"""
Script généré automatiquement pour relancer toutes les recherches LinkedIn.
Contient 35 mots-clés uniques extraits du fichier consolidé.
Paramètres: Paris, dernière semaine, 50 jobs par recherche, types Full-time/Contract/Temporary
"""

import sys
import time
from datetime import datetime

# Ajouter le chemin vers le module
sys.path.append('/root/project-jobsearch/linkedin-search-')

try:
    from src.mcp_linkedin.client import linkedin_job_search_advanced
    print("✅ Module LinkedIn importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("🔧 Vérifiez que le module linkedin-api est installé:")
    print("   pip install linkedin-api python-dotenv fastmcp")
    sys.exit(1)

def main():
    # Liste des mots-clés uniques extraits
    unique_keywords = [
        "Brand Manager",
        "CRM Manager",
        "Content Manager",
        "Content Strategist",
        "Conversion Manager",
        "Cursor AI SEO",
        "Digital Campaign Manager",
        "Digital Consultant",
        "Digital Marketing Manager",
        "Enterprise SEO",
        "Growth Manager",
        "Head of Growth",
        "IA Agent",
        "Inbound Marketing Manager",
        "Local SEO",
        "Marketing Digital",
        "Marketing Operations Manager",
        "Marketing Strategist",
        "PPC Specialist",
        "Performance Manager",
        "Product Marketing Manager",
        "Programmatic SEO",
        "SEO",
        "SEO Analyst",
        "SEO Consultant",
        "SEO Specialist",
        "SEO programmatique",
        "Screaming Frog",
        "Social Media Manager",
        "Technical Writer",
        "Traffic Manager",
        "UX Content Writer",
        "User Acquisition Manager",
        "Webmarketing Manager",
        "python developer",
    ]
    
    # Paramètres de recherche
    location = "Paris"
    time_filter = 604800  # 7 jours (dernière semaine)
    limit = 50
    job_types = ["F", "C", "T"]  # Full-time, Contract, Temporary
    
    print(f"🚀 LANCEMENT DES RECHERCHES LINKEDIN")
    print(f"=" * 50)
    print(f"📍 Localisation: {location}")
    print(f"⏰ Filtre: Dernière semaine")
    print(f"📊 Limite: {limit} jobs par recherche")
    print(f"💼 Types: Full-time, Contract, Temporary")
    print(f"🔄 Total recherches: {len(unique_keywords)}")
    
    # Lancement automatique
    print("\n🚀 Démarrage automatique...")
    
    # Exécuter les recherches
    successful = 0
    failed = 0
    start_time = datetime.now()
    
    for i, keywords in enumerate(unique_keywords, 1):
        print(f"\n🔄 {i}/{len(unique_keywords)}: '{keywords}'")
        
        try:
            result = linkedin_job_search_advanced(
                keywords=keywords,
                location=location,
                limit=limit,
                job_type=job_types,
                listed_at=time_filter,
                use_enhanced_location=True
            )
            print(f"✅ Succès")
            successful += 1
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            failed += 1
        
        # Pause pour éviter rate limiting
        if i < len(unique_keywords):
            time.sleep(8)
    
    # Résultats finaux
    duration = datetime.now() - start_time
    print(f"\n🎉 TERMINÉ!")
    print(f"✅ Succès: {successful}")
    print(f"❌ Échecs: {failed}")
    print(f"⏱️  Durée: {duration}")
    print(f"📁 Données consolidées automatiquement dans exports/Exports/")

if __name__ == "__main__":
    main()
