#!/usr/bin/env python3
"""
Script complet pour relancer toutes les recherches avec mots-clés uniques.
Version autonome qui inclut l'extraction ET le relancement des recherches.
"""

import json
import os
import re
import sys
import time
from datetime import datetime

# Ajouter les chemins nécessaires
sys.path.insert(0, '/root/project-jobsearch/linkedin-search-')
sys.path.insert(0, '/root/project-jobsearch/linkedin-search-/src')

def extract_unique_keywords_from_file(consolidated_file_path):
    """
    Extrait tous les mots-clés uniques du fichier consolidé.
    """
    try:
        with open(consolidated_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire tous les mots-clés avec une regex
        keyword_pattern = r'"keywords":\s*"([^"]*)"'
        matches = re.findall(keyword_pattern, content)
        
        # Créer un set pour éliminer les doublons et nettoyer
        keywords_set = set()
        for match in matches:
            if match.strip():  # Ignorer les chaînes vides
                keywords_set.add(match.strip())
        
        # Convertir en liste triée
        unique_keywords = sorted(list(keywords_set))
        
        return unique_keywords
        
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction des mots-clés: {e}")
        return []

def run_searches_with_unique_keywords():
    """
    Version complète avec import dynamique et gestion d'erreurs robuste.
    """
    # Chemin du fichier consolidé
    consolidated_file = "/root/project-jobsearch/linkedin-search-/search-system/exports/Exports/linkedin_job_searches_consolidated.json"
    
    if not os.path.exists(consolidated_file):
        print(f"❌ Fichier consolidé non trouvé: {consolidated_file}")
        return
    
    # Extraire les mots-clés uniques
    unique_keywords = extract_unique_keywords_from_file(consolidated_file)
    
    if not unique_keywords:
        print("❌ Aucun mot-clé trouvé.")
        return
    
    print(f"🔍 MOTS-CLÉS UNIQUES EXTRAITS ({len(unique_keywords)} trouvés)")
    print("=" * 60)
    for i, keyword in enumerate(unique_keywords, 1):
        print(f"  {i:2d}. {keyword}")
    
    # Tenter l'import du client LinkedIn
    try:
        from src.mcp_linkedin.client import linkedin_job_search_advanced
        print(f"\n✅ Module LinkedIn importé avec succès")
    except ImportError as e:
        print(f"\n❌ Erreur d'import LinkedIn: {e}")
        print("📋 SOLUTION: Voici le script prêt à exécuter avec les bons imports:")
        print_ready_to_run_script(unique_keywords)
        return
    
    # Paramètres de recherche
    location = "Paris"
    time_filter = 604800  # 7 jours en secondes (dernière semaine)
    limit = 50
    job_types = ["F", "C", "T"]  # Full-time, Contract, Temporary
    
    print(f"\n🚀 PARAMÈTRES DE RECHERCHE")
    print(f"=" * 40)
    print(f"📍 Localisation: {location}")
    print(f"⏰ Filtre temporel: Dernière semaine ({time_filter} secondes)")
    print(f"📊 Limite par recherche: {limit} jobs")
    print(f"💼 Types de contrat: Full-time, Contract, Temporary")
    print(f"🔄 Nombre total de recherches: {len(unique_keywords)}")
    
    # Demander confirmation
    try:
        input("\n⏸️  Appuyez sur Entrée pour commencer les recherches (ou Ctrl+C pour annuler)...")
    except KeyboardInterrupt:
        print("\n⏹️  Opération annulée par l'utilisateur")
        return
    
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
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche '{keywords}': {e}")
            failed_searches += 1
        
        # Pause entre les recherches pour éviter le rate limiting
        if i < total_searches:
            pause_duration = 8  # 8 secondes entre chaque recherche
            print(f"⏳ Pause de {pause_duration} secondes...")
            time.sleep(pause_duration)
    
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

def print_ready_to_run_script(unique_keywords):
    """
    Génère un script prêt à exécuter avec tous les mots-clés.
    """
    script_content = f'''#!/usr/bin/env python3
"""
Script généré automatiquement pour relancer toutes les recherches LinkedIn.
Contient {len(unique_keywords)} mots-clés uniques extraits du fichier consolidé.
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
    print(f"❌ Erreur d'import: {{e}}")
    print("🔧 Vérifiez que le module linkedin-api est installé:")
    print("   pip install linkedin-api python-dotenv fastmcp")
    sys.exit(1)

def main():
    # Liste des mots-clés uniques extraits
    unique_keywords = [
{chr(10).join([f'        "{keyword}",' for keyword in unique_keywords])}
    ]
    
    # Paramètres de recherche
    location = "Paris"
    time_filter = 604800  # 7 jours (dernière semaine)
    limit = 50
    job_types = ["F", "C", "T"]  # Full-time, Contract, Temporary
    
    print(f"🚀 LANCEMENT DES RECHERCHES LINKEDIN")
    print(f"=" * 50)
    print(f"📍 Localisation: {{location}}")
    print(f"⏰ Filtre: Dernière semaine")
    print(f"📊 Limite: {{limit}} jobs par recherche")
    print(f"💼 Types: Full-time, Contract, Temporary")
    print(f"🔄 Total recherches: {{len(unique_keywords)}}")
    
    # Demander confirmation
    try:
        input("\\n⏸️  Appuyez sur Entrée pour commencer...")
    except KeyboardInterrupt:
        print("\\n⏹️  Annulé")
        return
    
    # Exécuter les recherches
    successful = 0
    failed = 0
    start_time = datetime.now()
    
    for i, keywords in enumerate(unique_keywords, 1):
        print(f"\\n🔄 {{i}}/{{len(unique_keywords)}}: '{{keywords}}'")
        
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
            print(f"❌ Erreur: {{e}}")
            failed += 1
        
        # Pause pour éviter rate limiting
        if i < len(unique_keywords):
            time.sleep(8)
    
    # Résultats finaux
    duration = datetime.now() - start_time
    print(f"\\n🎉 TERMINÉ!")
    print(f"✅ Succès: {{successful}}")
    print(f"❌ Échecs: {{failed}}")
    print(f"⏱️  Durée: {{duration}}")
    print(f"📁 Données consolidées automatiquement dans exports/Exports/")

if __name__ == "__main__":
    main()
'''

    # Sauvegarder le script
    script_path = "/root/project-jobsearch/linkedin-search-/search-system/scripts/generated_relaunch_script.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\n📝 SCRIPT GÉNÉRÉ: {script_path}")
    print(f"🚀 POUR EXÉCUTER:")
    print(f"   cd /root/project-jobsearch/linkedin-search-/search-system")
    print(f"   python scripts/generated_relaunch_script.py")
    
    return script_path

if __name__ == "__main__":
    print("🔍 EXTRACTEUR ET RELANCEUR COMPLET - MOTS-CLÉS LINKEDIN")
    print("=" * 65)
    
    try:
        run_searches_with_unique_keywords()
    except KeyboardInterrupt:
        print("\n\n⏹️  Opération interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)