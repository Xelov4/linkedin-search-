#!/usr/bin/env python3
"""
Script d'analyse du fichier JSON consolidé.
Fournit des statistiques détaillées sur les recherches et offres d'emploi.
"""

import json
import os
from datetime import datetime
from collections import Counter
import sys

def analyze_consolidated_file():
    """Analyse le fichier JSON consolidé et affiche les statistiques."""
    
    consolidated_file = "Exports/linkedin_job_searches_consolidated.json"
    
    if not os.path.exists(consolidated_file):
        print("❌ Fichier consolidé non trouvé.")
        print(f"📁 Recherche dans : {os.path.abspath(consolidated_file)}")
        print("💡 Effectuez d'abord quelques recherches LinkedIn !")
        return False
    
    try:
        with open(consolidated_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Erreur : Fichier JSON corrompu")
        return False
    
    # Affichage des informations principales
    print("📊 ANALYSE DU FICHIER CONSOLIDÉ LinkedIn Job Search")
    print("=" * 60)
    
    metadata = data.get('metadata', {})
    search_history = data.get('search_history', [])
    jobs = data.get('jobs', [])
    
    # Métadonnées générales
    print(f"📅 Créé le : {metadata.get('creation_date', 'N/A')}")
    print(f"🔄 Dernière mise à jour : {metadata.get('last_updated', 'N/A')}")
    print(f"📈 Version d'export : {metadata.get('export_version', 'N/A')}")
    print(f"🔍 Total recherches : {metadata.get('total_searches', 0)}")
    print(f"💼 Total offres uniques : {metadata.get('total_jobs', 0)}")
    
    if not search_history:
        print("\n⚠️ Aucun historique de recherche trouvé")
        return True
    
    # Analyse des recherches
    print(f"\n📋 HISTORIQUE DES RECHERCHES ({len(search_history)})")
    print("-" * 40)
    
    total_jobs_found = 0
    keywords_counter = Counter()
    locations_counter = Counter()
    
    for i, search in enumerate(search_history, 1):
        keywords = search.get('keywords', 'N/A')
        location = search.get('location', 'N/A')
        jobs_found = search.get('jobs_found', 0)
        timestamp = search.get('search_timestamp', 'N/A')
        
        print(f"{i:2}. {keywords} @ {location}")
        print(f"    📊 {jobs_found} offres trouvées - {timestamp[:19]}")
        
        # Filtres appliqués
        filters = search.get('search_filters', {})
        filter_info = []
        
        if filters.get('job_types', {}).get('description'):
            filter_info.append(f"Type: {', '.join(filters['job_types']['description'])}")
        if filters.get('remote_work', {}).get('description'):
            filter_info.append(f"Mode: {', '.join(filters['remote_work']['description'])}")
        if filters.get('experience_levels', {}).get('description'):
            filter_info.append(f"Exp: {', '.join(filters['experience_levels']['description'])}")
        
        if filter_info:
            print(f"    🔧 Filtres: {' | '.join(filter_info)}")
        
        print()
        
        total_jobs_found += jobs_found
        keywords_counter[keywords] += 1
        locations_counter[location] += 1
    
    # Statistiques des offres
    if jobs:
        print(f"💼 ANALYSE DES OFFRES D'EMPLOI ({len(jobs)})")
        print("-" * 40)
        
        # Analyse par entreprise
        companies = [job.get('company', 'N/A') for job in jobs]
        company_counter = Counter(companies)
        
        print("🏢 Top 5 entreprises :")
        for company, count in company_counter.most_common(5):
            print(f"   {company}: {count} offres")
        
        # Analyse par lieu
        job_locations = [job.get('location', 'N/A') for job in jobs]
        job_location_counter = Counter(job_locations)
        
        print("\n📍 Top 5 localisations :")
        for location, count in job_location_counter.most_common(5):
            print(f"   {location}: {count} offres")
        
        # Types de travail
        workplace_types = [job.get('workplace_type', 'N/A') for job in jobs if job.get('workplace_type')]
        if workplace_types:
            workplace_counter = Counter(workplace_types)
            print("\n🏠 Types de télétravail :")
            for wtype, count in workplace_counter.most_common():
                print(f"   {wtype}: {count} offres")
        
        # Job nature
        job_natures = [job.get('job_nature', 'N/A') for job in jobs if job.get('job_nature')]
        if job_natures:
            nature_counter = Counter(job_natures)
            print("\n💼 Types de contrat :")
            for nature, count in nature_counter.most_common():
                print(f"   {nature}: {count} offres")
    
    # Statistiques des recherches
    print(f"\n🔍 STATISTIQUES DES RECHERCHES")
    print("-" * 40)
    
    print("🎯 Mots-clés les plus recherchés :")
    for keyword, count in keywords_counter.most_common(5):
        print(f"   {keyword}: {count} fois")
    
    print(f"\n📍 Localisations les plus recherchées :")
    for location, count in locations_counter.most_common(5):
        print(f"   {location}: {count} fois")
    
    # Efficacité des recherches
    if total_jobs_found > 0:
        avg_jobs_per_search = total_jobs_found / len(search_history)
        unique_rate = (len(jobs) / total_jobs_found) * 100 if total_jobs_found > 0 else 0
        
        print(f"\n📈 MÉTRIQUES D'EFFICACITÉ")
        print("-" * 40)
        print(f"📊 Moyenne offres/recherche : {avg_jobs_per_search:.1f}")
        print(f"🎯 Taux d'unicité : {unique_rate:.1f}% ({len(jobs)}/{total_jobs_found})")
        print(f"🔄 Doublons évités : {total_jobs_found - len(jobs)}")
    
    print(f"\n📁 Fichier analysé : {os.path.abspath(consolidated_file)}")
    
    return True

if __name__ == "__main__":
    if not analyze_consolidated_file():
        sys.exit(1)