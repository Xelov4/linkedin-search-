#!/usr/bin/env python3
"""
Script pour fusionner les deux fichiers consolidés LinkedIn.
Fusionne le fichier récent (Exports/) avec l'ancien (exports/Exports/).
"""

import json
import os
from datetime import datetime

def merge_consolidated_files():
    """Fusionne les deux fichiers consolidés LinkedIn."""
    
    # Chemins des fichiers
    old_file = "exports/Exports/linkedin_job_searches_consolidated.json"
    new_file = "Exports/linkedin_job_searches_consolidated.json"
    
    print("🔄 FUSION DES FICHIERS CONSOLIDÉS LinkedIn")
    print("=" * 50)
    
    # Vérifier l'existence des fichiers
    if not os.path.exists(old_file):
        print(f"❌ Fichier ancien non trouvé: {old_file}")
        return False
    
    if not os.path.exists(new_file):
        print(f"❌ Fichier nouveau non trouvé: {new_file}")
        return False
    
    # Charger les deux fichiers
    print(f"📖 Lecture de l'ancien fichier: {old_file}")
    with open(old_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    print(f"📖 Lecture du nouveau fichier: {new_file}")
    with open(new_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    # Afficher les statistiques des fichiers
    print(f"\n📊 STATISTIQUES AVANT FUSION")
    print(f"Ancien fichier:")
    print(f"  - Recherches: {old_data['metadata']['total_searches']}")
    print(f"  - Offres: {old_data['metadata']['total_jobs']}")
    print(f"  - Dernière MAJ: {old_data['metadata']['last_updated']}")
    
    print(f"\nNouveau fichier:")
    print(f"  - Recherches: {new_data['metadata']['total_searches']}")
    print(f"  - Offres: {new_data['metadata']['total_jobs']}")
    print(f"  - Dernière MAJ: {new_data['metadata']['last_updated']}")
    
    # Fusionner les données
    print(f"\n🔄 Fusion en cours...")
    
    # Combiner les historiques de recherche
    combined_search_history = old_data['search_history'] + new_data['search_history']
    
    # Combiner les offres avec déduplication par ID
    old_jobs = {job['id']: job for job in old_data['jobs']}
    new_jobs = {job['id']: job for job in new_data['jobs']}
    
    # Fusionner en gardant les nouvelles versions en cas de doublon
    combined_jobs = {**old_jobs, **new_jobs}
    
    # Créer le fichier fusionné
    merged_data = {
        "metadata": {
            "creation_date": old_data['metadata']['creation_date'],
            "last_updated": datetime.now().isoformat(),
            "total_searches": len(combined_search_history),
            "total_jobs": len(combined_jobs),
            "data_coverage": "Minimal - No duplicate fields",
            "export_version": "incremental_v8.0",
            "merge_info": {
                "merged_at": datetime.now().isoformat(),
                "old_file_searches": old_data['metadata']['total_searches'],
                "old_file_jobs": old_data['metadata']['total_jobs'],
                "new_file_searches": new_data['metadata']['total_searches'],
                "new_file_jobs": new_data['metadata']['total_jobs']
            }
        },
        "search_history": combined_search_history,
        "jobs": list(combined_jobs.values())
    }
    
    # Sauvegarder dans l'ancien fichier (destination finale)
    print(f"💾 Sauvegarde du fichier fusionné dans: {old_file}")
    with open(old_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)
    
    # Statistiques finales
    print(f"\n✅ FUSION TERMINÉE")
    print(f"📊 Statistiques finales:")
    print(f"  - Total recherches: {len(combined_search_history)}")
    print(f"  - Total offres uniques: {len(combined_jobs)}")
    print(f"  - Doublons évités: {(old_data['metadata']['total_jobs'] + new_data['metadata']['total_jobs']) - len(combined_jobs)}")
    print(f"📁 Fichier consolidé final: {os.path.abspath(old_file)}")
    
    # Supprimer le fichier temporaire
    print(f"\n🗑️  Suppression du fichier temporaire: {new_file}")
    os.remove(new_file)
    
    # Supprimer le dossier Exports s'il est vide
    exports_dir = "Exports"
    if os.path.exists(exports_dir) and not os.listdir(exports_dir):
        print(f"🗑️  Suppression du dossier vide: {exports_dir}")
        os.rmdir(exports_dir)
    
    return True

if __name__ == "__main__":
    try:
        success = merge_consolidated_files()
        if not success:
            print("\n⚠️ Fusion échouée")
            exit(1)
    except Exception as e:
        print(f"\n💥 Erreur lors de la fusion: {e}")
        import traceback
        traceback.print_exc()
        exit(1)