#!/usr/bin/env python3
"""
Script pour extraire et relancer toutes les recherches avec mots-clés uniques.
Extrait tous les mots-clés du fichier consolidé et relance des recherches 
avec les paramètres spécifiés: Paris, dernière semaine, 50 jobs par recherche.
"""

import sys
import os
import json
import time
from datetime import datetime

# Ajouter le chemin vers le module
sys.path.append('/root/project-jobsearch/linkedin-search-')

try:
    from src.mcp_linkedin.client import linkedin_job_search_advanced
    print("✅ Module LinkedIn importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

def extract_unique_keywords(consolidated_file_path):
    """
    Extrait tous les mots-clés uniques du fichier consolidé.
    
    :param consolidated_file_path: Chemin vers le fichier consolidé
    :return: Liste des mots-clés uniques
    """
    try:
        with open(consolidated_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        keywords_set = set()
        
        # Extraire depuis search_history
        if 'search_history' in data:
            for search in data['search_history']:
                if 'keywords' in search and search['keywords']:
                    keywords_set.add(search['keywords'].strip())
        
        # Convertir en liste triée
        unique_keywords = sorted(list(keywords_set))
        
        print(f"🔍 {len(unique_keywords)} mots-clés uniques extraits:")
        for i, keyword in enumerate(unique_keywords, 1):
            print(f"  {i:2d}. {keyword}")
        
        return unique_keywords
        
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction des mots-clés: {e}")
        return []

def relaunch_all_searches():
    """
    Relance toutes les recherches avec les mots-clés uniques trouvés.
    Paramètres fixés: Paris, dernière semaine, 50 jobs par recherche.
    """
    # Chemin du fichier consolidé
    consolidated_file = "/root/project-jobsearch/linkedin-search-/search-system/exports/Exports/linkedin_job_searches_consolidated.json"
    
    if not os.path.exists(consolidated_file):
        print(f"❌ Fichier consolidé non trouvé: {consolidated_file}")
        return
    
    # Extraire les mots-clés uniques
    unique_keywords = extract_unique_keywords(consolidated_file)
    
    if not unique_keywords:
        print("❌ Aucun mot-clé trouvé.")
        return
    
    # Paramètres de recherche
    location = "Paris"
    time_filter = 604800  # 7 jours en secondes (dernière semaine)
    limit = 50
    job_types = ["F", "C", "T"]  # Full-time, Contract, Temporary
    
    print(f"\n🚀 LANCEMENT DES RECHERCHES")
    print(f"=" * 50)
    print(f"📍 Localisation: {location}")
    print(f"⏰ Filtre temporel: Dernière semaine ({time_filter} secondes)")
    print(f"📊 Limite par recherche: {limit} jobs")
    print(f"💼 Types de contrat: Full-time, Contract, Temporary")
    print(f"🔄 Nombre total de recherches: {len(unique_keywords)}")
    
    # Demander confirmation
    input("\n⏸️  Appuyez sur Entrée pour commencer les recherches (ou Ctrl+C pour annuler)...")
    
    # Statistiques
    total_searches = len(unique_keywords)
    successful_searches = 0
    failed_searches = 0
    start_time = datetime.now()
    
    for i, keywords in enumerate(unique_keywords, 1):
        print(f"\n🔄 Recherche {i}/{total_searches}: '{keywords}'")
        print("-" * 60)
        
        try:
            result = linkedin_job_search_advanced(
                keywords=keywords,
                location=location,
                limit=limit,
                job_type=job_types,
                listed_at=time_filter,
                use_enhanced_location=True
            )
            
            print(f"✅ Recherche '{keywords}' terminée avec succès")
            successful_searches += 1
            
            # Pause entre les recherches pour éviter le rate limiting
            if i < total_searches:
                pause_duration = 8  # 8 secondes entre chaque recherche
                print(f"⏳ Pause de {pause_duration} secondes...")
                time.sleep(pause_duration)
                
        except Exception as e:
            print(f"❌ Erreur lors de la recherche '{keywords}': {e}")
            failed_searches += 1
            # Pause même en cas d'erreur
            if i < total_searches:
                time.sleep(5)
    
    # Statistiques finales
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n🎉 TOUTES LES RECHERCHES TERMINÉES!")
    print(f"=" * 50)
    print(f"✅ Recherches réussies: {successful_searches}")
    print(f"❌ Recherches échouées: {failed_searches}")
    print(f"📊 Total: {total_searches}")
    print(f"⏱️  Durée totale: {duration}")
    print(f"📄 Fichier consolidé mis à jour:")
    print(f"   {consolidated_file}")
    print(f"\n💡 Toutes les nouvelles données ont été consolidées automatiquement")
    print(f"   avec suppression des doublons par ID d'offre!")

def show_unique_keywords_list():
    """
    Affiche uniquement la liste des mots-clés uniques sans lancer les recherches.
    """
    consolidated_file = "/root/project-jobsearch/linkedin-search-/search-system/exports/Exports/linkedin_job_searches_consolidated.json"
    
    if not os.path.exists(consolidated_file):
        print(f"❌ Fichier consolidé non trouvé: {consolidated_file}")
        return
    
    unique_keywords = extract_unique_keywords(consolidated_file)
    
    if unique_keywords:
        print(f"\n📋 LISTE COMPLÈTE DES MOTS-CLÉS UNIQUES:")
        print(f"=" * 50)
        for keyword in unique_keywords:
            print(f"• {keyword}")
        print(f"\n📊 Total: {len(unique_keywords)} mots-clés uniques")
        return unique_keywords
    else:
        print("❌ Aucun mot-clé trouvé.")
        return []

if __name__ == "__main__":
    print("🔍 EXTRACTEUR ET RELANCEUR DE RECHERCHES LINKEDIN")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--list-only":
        # Mode affichage uniquement
        show_unique_keywords_list()
    else:
        # Mode complet avec recherches
        try:
            relaunch_all_searches()
        except KeyboardInterrupt:
            print("\n\n⏹️  Opération interrompue par l'utilisateur")
        except Exception as e:
            print(f"\n💥 Erreur inattendue: {e}")
            sys.exit(1)