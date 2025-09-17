#!/usr/bin/env python3
"""
Script pour extraire uniquement les mots-clés uniques du fichier consolidé.
Ne nécessite pas d'imports LinkedIn - extraction pure.
"""

import json
import os
import re

def extract_unique_keywords_from_file(consolidated_file_path):
    """
    Extrait tous les mots-clés uniques du fichier consolidé.
    
    :param consolidated_file_path: Chemin vers le fichier consolidé
    :return: Liste des mots-clés uniques
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

def main():
    """
    Fonction principale pour extraire et afficher les mots-clés uniques.
    """
    # Chemin du fichier consolidé
    consolidated_file = "/root/project-jobsearch/linkedin-search-/search-system/exports/Exports/linkedin_job_searches_consolidated.json"
    
    if not os.path.exists(consolidated_file):
        print(f"❌ Fichier consolidé non trouvé: {consolidated_file}")
        return []
    
    print("🔍 EXTRACTION DES MOTS-CLÉS UNIQUES")
    print("=" * 50)
    print(f"📁 Source: {consolidated_file}")
    print()
    
    unique_keywords = extract_unique_keywords_from_file(consolidated_file)
    
    if unique_keywords:
        print(f"✅ {len(unique_keywords)} mots-clés uniques trouvés:")
        print("-" * 50)
        for i, keyword in enumerate(unique_keywords, 1):
            print(f"{i:2d}. {keyword}")
        
        print(f"\n📋 LISTE POUR COPIER-COLLER:")
        print("-" * 30)
        for keyword in unique_keywords:
            print(f'"{keyword}",')
        
        print(f"\n📊 RÉSUMÉ:")
        print(f"• Total mots-clés uniques: {len(unique_keywords)}")
        print(f"• Fichier source: {os.path.basename(consolidated_file)}")
        
        return unique_keywords
    else:
        print("❌ Aucun mot-clé trouvé.")
        return []

if __name__ == "__main__":
    keywords = main()