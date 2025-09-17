from linkedin_api import Linkedin
from fastmcp import FastMCP
import os
import logging
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import List

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP("mcp-linkedin")
logger = logging.getLogger(__name__)

def get_client():
    return Linkedin(os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"), debug=True)

@mcp.tool()
def get_feed_posts(limit: int = 10, offset: int = 0) -> str:
    """
    Retrieve LinkedIn feed posts.

    :return: List of feed post details
    """
    client = get_client()
    try:
        post_urns = client.get_feed_posts(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {e}"
    
    posts = ""
    for urn in post_urns:
        posts += f"Post by {urn['author_name']}: {urn['content']}\n"

    return posts

@mcp.tool()
def search_jobs(keywords: str, limit: int = 3, offset: int = 0, location: str = '') -> str:
    """
    Search for jobs on LinkedIn.
    
    :param keywords: Job search keywords
    :param limit: Maximum number of job results
    :param location: Optional location filter
    :return: List of job details
    """
    client = get_client()
    jobs = client.search_jobs(
        keywords=keywords,
        location_name=location,
        limit=limit,
        offset=offset,
    )
    job_results = ""
    for job in jobs:
        job_id = job["entityUrn"].split(":")[-1]
        job_data = client.get_job(job_id=job_id)

        job_title = job_data["title"]
        company_name = job_data["companyDetails"]["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]["name"]
        job_description = job_data["description"]["text"]
        job_location = job_data["formattedLocation"]

        job_results += f"Job by {job_title} at {company_name} in {job_location}: {job_description}\n\n"

    return job_results

def get_location_id(location_name: str) -> str:
    """
    Obtient l'ID de géolocalisation LinkedIn pour un nom de lieu.
    
    :param location_name: Nom du lieu (ex: "Amsterdam", "Madrid")
    :return: ID de géolocalisation LinkedIn
    """
    import requests
    
    try:
        # Utilise l'API de géolocalisation LinkedIn
        url = "https://www.linkedin.com/jobs-guest/api/typeaheadHits"
        params = {
            "origin": "jserp",
            "typeaheadType": "GEO", 
            "geoTypes": "POPULATED_PLACE",
            "query": location_name
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            # Chercher le bon résultat selon le pays
            for location in data:
                display_name = location.get("displayName", "").lower()
                
                # Logique de priorité pour choisir la bonne ville
                if location_name.lower() == "amsterdam":
                    # Préférer les Pays-Bas
                    if "netherlands" in display_name:
                        return location["id"]
                elif location_name.lower() == "madrid":
                    # Préférer l'Espagne  
                    if "spain" in display_name or "madrid" in display_name.split(",")[0].strip():
                        return location["id"]
                elif location_name.lower() == "rome":
                    # Préférer l'Italie
                    if "italy" in display_name:
                        return location["id"]
                elif location_name.lower() == "london":
                    # Préférer le Royaume-Uni
                    if "united kingdom" in display_name or "england" in display_name:
                        return location["id"]
                        
            # Si aucune correspondance spécifique, prendre le premier
            return data[0]["id"]
        
        return ""
        
    except Exception as e:
        print(f"Erreur lors de la récupération de l'ID de localisation: {e}")
        return ""

def search_jobs_direct(keywords: str, limit: int = 3, offset: int = 0, location: str = '') -> str:
    """
    Direct version of search_jobs function that can be called without MCP decorator.
    Récupère 100% des données disponibles dans l'API LinkedIn.
    
    :param keywords: Job search keywords
    :param limit: Maximum number of job results
    :param location: Optional location filter
    :return: List of job details
    """
    client = get_client()
    jobs = client.search_jobs(
        keywords=keywords,
        location_name=location,
        limit=limit,
        offset=offset,
    )
    
    # Store structured data for JSON export
    jobs_structured = []
    
    job_results = ""
    for job in jobs:
        job_id = job["entityUrn"].split(":")[-1]
        job_data = client.get_job(job_id=job_id)

        # Extract basic info
        job_title = job_data.get("title", "")
        company_name = ""
        company_details_full = {}
        
        # Extract complete company information
        if "companyDetails" in job_data:
            company_details_full = job_data["companyDetails"]
            if "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany" in company_details_full:
                company_details = company_details_full["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]
                if "companyResolutionResult" in company_details:
                    company_name = company_details["companyResolutionResult"].get("name", "")
                    
                    # Extract logo information and build custom logo URL
                    logo_info = company_details["companyResolutionResult"].get("logo", {})
                    custom_logo_url = ""
                    
                    if logo_info and "image" in logo_info:
                        image_data = logo_info["image"].get("com.linkedin.common.VectorImage", {})
                        root_url = image_data.get("rootUrl", "")
                        artifacts = image_data.get("artifacts", [])
                        
                        # Find the 400x400 size artifact
                        for artifact in artifacts:
                            if artifact.get("width") == 400 and artifact.get("height") == 400:
                                path_segment = artifact.get("fileIdentifyingUrlPathSegment", "")
                                if root_url and path_segment:
                                    custom_logo_url = root_url + path_segment
                                break
        else:
            company_details_full = {}
            custom_logo_url = ""
        
        job_description = job_data.get("description", {}).get("text", "")
        job_location = job_data.get("formattedLocation", "")
        
        # Extract ALL available fields with deep nesting
        job_structured = {
            # Basic identification
            "id": job_id,
            "job_posting_id": job_data.get("jobPostingId", ""),
            "custom_jobPost_url": f"https://www.linkedin.com/jobs/view/{job_data.get('jobPostingId', '')}/",
            
            # Basic job info
            "title": job_title,
            "company": company_name,
            "location": job_location,
            "description": job_description,
            
            # Company details (complete)
            "company_details": company_details_full,
            
            # Job state and status
            "job_state": job_data.get("jobState", ""),
            "talent_hub_job": job_data.get("talentHubJob", ""),
            
            # Workplace information
            "work_remote_allowed": job_data.get("workRemoteAllowed", ""),
            "workplace_types": job_data.get("workplaceTypes", ""),
            "workplace_types_resolution_results": job_data.get("workplaceTypesResolutionResults", ""),
            
            # Employment details
            "seniority_level": job_data.get("seniorityLevel", ""),
            "employment_status": job_data.get("employmentStatus", {}),
            "employment_type": job_data.get("employmentType", ""),
            "industry_name": job_data.get("industryName", ""),
            
            # Skills and requirements
            "skills": job_data.get("skills", []),
            "benefits": job_data.get("benefits", []),
            "requirements": job_data.get("requirements", {}),
            
            # Dates and timing
            "listed_at": job_data.get("listedAt", ""),
            "posting_timestamp": job_data.get("postingTimestamp", ""),
            "created_at": job_data.get("createdAt", ""),
            "updated_at": job_data.get("updatedAt", ""),
            
            # Application information
            "apply_method": job_data.get("applyMethod", {}),
            "application_url": job_data.get("applyMethod", {}).get("applyUrl", ""),
            "application_type": job_data.get("applyMethod", {}).get("type", ""),
            
            # Salary and compensation
            "salary_insights": job_data.get("salaryInsights", {}),
            "compensation": job_data.get("compensation", {}),
            
            # Additional metadata
            "recipe_type": job_data.get("$recipeType", ""),
            "tracking_id": job_data.get("trackingId", ""),
            "job_posting_status": job_data.get("jobPostingStatus", ""),
            
            # Experience and education
            "experience_level": job_data.get("experienceLevel", ""),
            "education_level": job_data.get("educationLevel", ""),
            
            # Location details
            "location_details": job_data.get("locationDetails", {}),
            "country": job_data.get("country", ""),
            "city": job_data.get("city", ""),
            "postal_code": job_data.get("postalCode", ""),
            
            # Company size and type
            "company_size": job_data.get("companySize", ""),
            "company_type": job_data.get("companyType", ""),
            
            # Job functions and categories
            "job_functions": job_data.get("jobFunctions", []),
            "job_categories": job_data.get("jobCategories", []),
            
            # Additional fields that might exist
            "certifications": job_data.get("certifications", []),
            "languages": job_data.get("languages", []),
            "travel_requirements": job_data.get("travelRequirements", ""),
            "relocation_assistance": job_data.get("relocationAssistance", ""),
            
            # Internal LinkedIn fields
            "internal_job": job_data.get("internalJob", ""),
            "sponsored_job": job_data.get("sponsoredJob", ""),
            "premium_job": job_data.get("premiumJob", ""),
            
            # Complete raw data for maximum coverage
            "raw_data_complete": job_data,
            
            # List of all available keys for reference
            "all_available_keys": list(job_data.keys())
        }
        
        jobs_structured.append(job_structured)
        
        # Format for console output
        job_results += f"Job by {job_title} at {company_name} in {job_location}: {job_description}\n\n"

    # Save structured data to JSON
    save_jobs_incremental_to_json(jobs_structured, keywords, location, limit)
    
    return job_results

def search_jobs_with_proper_location(keywords: str, location: str, limit: int = 3, offset: int = 0) -> str:
    """
    Recherche de jobs avec géolocalisation correcte utilisant locationUnion:(geoId:ID).
    
    :param keywords: Mots-clés de recherche
    :param location: Nom de la localisation
    :param limit: Nombre de résultats
    :param offset: Offset pour pagination
    :return: Résultats formatés
    """
    from urllib.parse import urlencode
    import requests
    
    # Obtenir l'ID de géolocalisation
    location_id = get_location_id(location)
    if not location_id:
        print(f"❌ Impossible de trouver l'ID de géolocalisation pour: {location}")
        return search_jobs_direct(keywords, limit, offset, location)  # Fallback
    
    print(f"📍 ID de géolocalisation trouvé pour {location}: {location_id}")
    
    # Construire la requête avec la syntaxe correcte
    client = get_client()
    
    # Construction de la query avec la bonne syntaxe
    query = {
        "origin": "JOB_SEARCH_PAGE_QUERY_EXPANSION",
        "keywords": keywords,
        "locationUnion": f"(geoId:{location_id})",
        "selectedFilters": {
            "timePostedRange": "List(r604800)"  # 7 jours
        },
        "spellCorrectionEnabled": "true"
    }
    
    query_string = (
        str(query)
        .replace(" ", "")
        .replace("'", "")
        .replace("{", "(")
        .replace("}", ")")
    )
    
    # Paramètres de requête
    params = {
        "decorationId": "com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-174",
        "count": limit,
        "q": "jobSearch", 
        "query": query_string,
        "start": offset
    }
    
    try:
        # Faire la requête directement
        res = client._fetch(
            f"/voyagerJobsDashJobCards?{urlencode(params, safe='(),:')}",
            headers={"accept": "application/vnd.linkedin.normalized+json+2.1"},
        )
        data = res.json()
        
        elements = data.get("included", [])
        jobs = [
            i for i in elements
            if i["$type"] == "com.linkedin.voyager.dash.jobs.JobPosting"
        ]
        
        # Traiter les résultats
        job_results = ""
        jobs_structured = []
        
        for job in jobs:
            job_id = job["entityUrn"].split(":")[-1] 
            job_data = client.get_job(job_id=job_id)
            
            job_title = job_data.get("title", "")
            job_location = job_data.get("formattedLocation", "")
            job_description = job_data.get("description", {}).get("text", "")
            
            # Extraire le nom de l'entreprise
            company_name = ""
            if "companyDetails" in job_data:
                company_details = job_data["companyDetails"]
                if "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany" in company_details:
                    company_data = company_details["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]
                    if "companyResolutionResult" in company_data:
                        company_name = company_data["companyResolutionResult"].get("name", "")
            
            job_results += f"Job: \"{job_title}\" chez {company_name} - 📍 {job_location}\n"
            
            # Extraire company_name, company_url et custom_logo_url depuis company_details
            company_url = ""
            custom_logo_url = ""
            if "companyDetails" in job_data:
                company_details = job_data["companyDetails"]
                if "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany" in company_details:
                    company_data = company_details["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]
                    if "companyResolutionResult" in company_data:
                        company_url = company_data["companyResolutionResult"].get("url", "")
                        # Générer custom_logo_url
                        logo_info = company_data["companyResolutionResult"].get("logo", {})
                        if logo_info and "image" in logo_info:
                            image_data = logo_info["image"].get("com.linkedin.common.VectorImage", {})
                            root_url = image_data.get("rootUrl", "")
                            artifacts = image_data.get("artifacts", [])
                            # Find the 400x400 size artifact
                            for artifact in artifacts:
                                if artifact.get("width") == 400 and artifact.get("height") == 400:
                                    path_segment = artifact.get("fileIdentifyingUrlPathSegment", "")
                                    if root_url and path_segment:
                                        custom_logo_url = root_url + path_segment
                                    break
            
            # Convertir listed_at en format lisible
            from datetime import datetime
            listed_at_raw = job_data.get("listedAt", 0)
            if listed_at_raw:
                listed_at_readable = datetime.fromtimestamp(listed_at_raw / 1000).strftime("%Y-%m-%d %H:%M:%S")
            else:
                listed_at_readable = ""
            
            # Extraire workplace_type depuis workplace_types_resolution_results
            workplace_type = ""
            workplace_results = job_data.get("workplaceTypesResolutionResults", {})
            for key, value in workplace_results.items():
                if isinstance(value, dict) and "localizedName" in value:
                    workplace_type = value["localizedName"]
                    break
            
            # Extraire apply_url depuis apply_method
            apply_url = ""
            apply_method = job_data.get("applyMethod", {})
            if "com.linkedin.voyager.jobs.OffsiteApply" in apply_method:
                apply_data = apply_method["com.linkedin.voyager.jobs.OffsiteApply"]
                apply_url = apply_data.get("companyApplyUrl", "")
            
            # Structure optimisée pour JSON - seulement les champs utiles
            job_structured = {
                # Champs critiques
                "id": job_id,
                "linkedin_postJob_url": f"https://www.linkedin.com/jobs/view/{job_id}/",
                "title": job_title,
                "company": company_name,
                "company_url": company_url,
                "location": job_location,
                "description": job_description,
                "listed_at": listed_at_readable,
                "apply_url": apply_url,
                "workplace_type": workplace_type,
                "custom_logo_url": custom_logo_url,
                "job_state": job_data.get("jobState", ""),
                "work_remote_allowed": job_data.get("workRemoteAllowed", False),
                "job_nature": ""  # Sera rempli dans la fonction de sauvegarde
            }
            jobs_structured.append(job_structured)
        
        # Sauvegarder les résultats  
        save_jobs_incremental_to_json(jobs_structured, keywords, location, limit, 
                                      None, None, None, None, None)
        
        return job_results
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche avec géolocalisation: {e}")
        return search_jobs_direct(keywords, limit, offset, location)  # Fallback

def linkedin_job_search_advanced(
    keywords: str, 
    location: str = '',
    limit: int = 10,
    experience: List[str] = None,
    job_type: List[str] = None,
    remote: List[str] = None,
    listed_at: int = 604800,
    distance: int = None,
    use_enhanced_location: bool = True
) -> str:
    """
    Fonction avancée pour la recherche d'emplois LinkedIn avec tous les filtres.
    
    :param keywords: Mots-clés de recherche (ex: "SEO", "developer", "marketing manager")
    :param location: Nom de la ville ou région (ex: "Amsterdam", "Tokyo", "Berlin")
    :param limit: Nombre de résultats souhaités (défaut: 10)
    :param experience: Niveaux d'expérience ["1"=Stage, "2"=Débutant, "3"=Associé, "4"=Intermédiaire, "5"=Directeur, "6"=Cadre]
    :param job_type: Types de contrat ["F"=CDI, "C"=Contrat, "P"=Temps partiel, "T"=Temporaire, "I"=Stage, "V"=Bénévolat, "O"=Autre]
    :param remote: Mode de travail ["1"=Présentiel, "2"=Télétravail, "3"=Hybride]
    :param listed_at: Limite de temps en secondes (604800=7j, 86400=24h, 2592000=30j)
    :param distance: Distance maximum en miles depuis la location
    :param use_enhanced_location: Utiliser la géolocalisation améliorée (recommandé: True)
    :return: Résultats formatés des offres d'emploi
    """
    print(f"🔍 Recherche avancée avec filtres multiples activée...")
    
    if location and use_enhanced_location:
        # Utiliser la géolocalisation améliorée avec filtres
        location_id = get_location_id(location)
        if not location_id:
            print(f"❌ Impossible de trouver l'ID de géolocalisation pour: {location}")
            location_id = None
        else:
            print(f"📍 ID de géolocalisation trouvé pour {location}: {location_id}")
    
    client = get_client()
    
    # Appel avec tous les paramètres disponibles
    if location and use_enhanced_location and location_id:
        # Version avec géolocalisation corrigée - on doit construire manuellement la requête
        from urllib.parse import urlencode
        
        query_parts = ["origin:JOB_SEARCH_PAGE_QUERY_EXPANSION"]
        
        if keywords:
            query_parts.append(f"keywords:{keywords}")
            
        if location_id:
            query_parts.append(f"locationUnion:(geoId:{location_id})")
        
        selected_filters = []
        if experience:
            selected_filters.append(f"experience:List({','.join(experience)})")
        if job_type:
            selected_filters.append(f"jobType:List({','.join(job_type)})")
        if remote:
            selected_filters.append(f"workplaceType:List({','.join(remote)})")
        if distance:
            selected_filters.append(f"distance:List({distance})")
        if listed_at:
            selected_filters.append(f"timePostedRange:List(r{listed_at})")
            
        if selected_filters:
            query_parts.append(f"selectedFilters:({','.join(selected_filters)})")
        
        query_parts.append("spellCorrectionEnabled:true")
        query_string = f"({','.join(query_parts)})"
        
        params = {
            "decorationId": "com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-174",
            "count": limit,
            "q": "jobSearch",
            "query": query_string,
            "start": 0
        }
        
        try:
            res = client._fetch(
                f"/voyagerJobsDashJobCards?{urlencode(params, safe='(),:')}",
                headers={"accept": "application/vnd.linkedin.normalized+json+2.1"},
            )
            data = res.json()
            
            elements = data.get("included", [])
            jobs = [i for i in elements if i["$type"] == "com.linkedin.voyager.dash.jobs.JobPosting"]
            
            # Traiter les résultats
            job_results = ""
            jobs_structured = []
            
            for job in jobs:
                job_id = job["entityUrn"].split(":")[-1] 
                job_data = client.get_job(job_id=job_id)
                
                job_title = job_data.get("title", "")
                job_location = job_data.get("formattedLocation", "")
                job_description = job_data.get("description", {}).get("text", "")
                
                # Extraire le nom de l'entreprise
                company_name = ""
                if "companyDetails" in job_data:
                    company_details = job_data["companyDetails"]
                    if "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany" in company_details:
                        company_data = company_details["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]
                        if "companyResolutionResult" in company_data:
                            company_name = company_data["companyResolutionResult"].get("name", "")
                
                job_results += f"Job: \"{job_title}\" chez {company_name} - 📍 {job_location}\n"
                
                # Extraire company_name, company_url et custom_logo_url depuis company_details
                company_url = ""
                custom_logo_url = ""
                if "companyDetails" in job_data:
                    company_details = job_data["companyDetails"]
                    if "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany" in company_details:
                        company_data = company_details["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]
                        if "companyResolutionResult" in company_data:
                            company_url = company_data["companyResolutionResult"].get("url", "")
                            # Générer custom_logo_url
                            logo_info = company_data["companyResolutionResult"].get("logo", {})
                            if logo_info and "image" in logo_info:
                                image_data = logo_info["image"].get("com.linkedin.common.VectorImage", {})
                                root_url = image_data.get("rootUrl", "")
                                artifacts = image_data.get("artifacts", [])
                                # Find the 400x400 size artifact
                                for artifact in artifacts:
                                    if artifact.get("width") == 400 and artifact.get("height") == 400:
                                        path_segment = artifact.get("fileIdentifyingUrlPathSegment", "")
                                        if root_url and path_segment:
                                            custom_logo_url = root_url + path_segment
                                        break
                
                # Convertir listed_at en format lisible
                from datetime import datetime
                listed_at_raw = job_data.get("listedAt", 0)
                if listed_at_raw:
                    listed_at_readable = datetime.fromtimestamp(listed_at_raw / 1000).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    listed_at_readable = ""
                
                # Extraire workplace_type depuis workplace_types_resolution_results
                workplace_type = ""
                workplace_results = job_data.get("workplaceTypesResolutionResults", {})
                for key, value in workplace_results.items():
                    if isinstance(value, dict) and "localizedName" in value:
                        workplace_type = value["localizedName"]
                        break
                
                # Extraire apply_url depuis apply_method
                apply_url = ""
                apply_method = job_data.get("applyMethod", {})
                if "com.linkedin.voyager.jobs.OffsiteApply" in apply_method:
                    apply_data = apply_method["com.linkedin.voyager.jobs.OffsiteApply"]
                    apply_url = apply_data.get("companyApplyUrl", "")
                
                # Structure optimisée pour JSON - seulement les champs utiles
                job_structured = {
                    # Champs critiques
                    "id": job_id,
                    "linkedin_postJob_url": f"https://www.linkedin.com/jobs/view/{job_id}/",
                    "title": job_title,
                    "company": company_name,
                    "company_url": company_url,
                    "location": job_location,
                    "description": job_description,
                    "listed_at": listed_at_readable,
                    "apply_url": apply_url,
                    "workplace_type": workplace_type,
                    "custom_logo_url": custom_logo_url,
                    "job_state": job_data.get("jobState", ""),
                    "work_remote_allowed": job_data.get("workRemoteAllowed", False),
                    "job_nature": ""  # Sera rempli dans la fonction de sauvegarde
                }
                jobs_structured.append(job_structured)
            
            # Sauvegarder les résultats
            save_jobs_incremental_to_json(jobs_structured, keywords, location, limit, 
                                          experience, job_type, remote, listed_at, distance)
            return job_results
            
        except Exception as e:
            print(f"❌ Erreur recherche avec géolocalisation avancée: {e}")
            # Fallback vers méthode standard
            
    # Méthode standard avec filtres
    jobs = client.search_jobs(
        keywords=keywords,
        location_name=location if location else None,
        experience=experience,
        job_type=job_type,
        remote=remote,
        listed_at=listed_at,
        distance=distance,
        limit=limit
    )
    
    # Traitement standard des résultats
    job_results = ""
    jobs_structured = []
    
    for job in jobs:
        job_id = job["entityUrn"].split(":")[-1]
        job_data = client.get_job(job_id=job_id)
        
        job_title = job_data.get("title", "")
        job_location = job_data.get("formattedLocation", "")
        job_description = job_data.get("description", {}).get("text", "")
        
        # Extraire le nom de l'entreprise
        company_name = ""
        if "companyDetails" in job_data:
            company_details = job_data["companyDetails"]
            if "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany" in company_details:
                company_data = company_details["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]
                if "companyResolutionResult" in company_data:
                    company_name = company_data["companyResolutionResult"].get("name", "")
        
        job_results += f"Job: \"{job_title}\" chez {company_name} - 📍 {job_location}\n"
        
        # Extraire company_name, company_url et custom_logo_url depuis company_details
        company_url = ""
        custom_logo_url = ""
        if "companyDetails" in job_data:
            company_details = job_data["companyDetails"]
            if "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany" in company_details:
                company_data = company_details["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]
                if "companyResolutionResult" in company_data:
                    company_url = company_data["companyResolutionResult"].get("url", "")
                    # Générer custom_logo_url
                    logo_info = company_data["companyResolutionResult"].get("logo", {})
                    if logo_info and "image" in logo_info:
                        image_data = logo_info["image"].get("com.linkedin.common.VectorImage", {})
                        root_url = image_data.get("rootUrl", "")
                        artifacts = image_data.get("artifacts", [])
                        # Find the 400x400 size artifact
                        for artifact in artifacts:
                            if artifact.get("width") == 400 and artifact.get("height") == 400:
                                path_segment = artifact.get("fileIdentifyingUrlPathSegment", "")
                                if root_url and path_segment:
                                    custom_logo_url = root_url + path_segment
                                break
        
        # Convertir listed_at en format lisible
        from datetime import datetime
        listed_at_raw = job_data.get("listedAt", 0)
        if listed_at_raw:
            listed_at_readable = datetime.fromtimestamp(listed_at_raw / 1000).strftime("%Y-%m-%d %H:%M:%S")
        else:
            listed_at_readable = ""
        
        # Extraire workplace_type depuis workplace_types_resolution_results
        workplace_type = ""
        workplace_results = job_data.get("workplaceTypesResolutionResults", {})
        for key, value in workplace_results.items():
            if isinstance(value, dict) and "localizedName" in value:
                workplace_type = value["localizedName"]
                break
        
        # Extraire apply_url depuis apply_method
        apply_url = ""
        apply_method = job_data.get("applyMethod", {})
        if "com.linkedin.voyager.jobs.OffsiteApply" in apply_method:
            apply_data = apply_method["com.linkedin.voyager.jobs.OffsiteApply"]
            apply_url = apply_data.get("companyApplyUrl", "")
        
        # Structure optimisée pour JSON - seulement les champs utiles
        job_structured = {
            # Champs critiques
            "id": job_id,
            "linkedin_postJob_url": f"https://www.linkedin.com/jobs/view/{job_id}/",
            "title": job_title,
            "company": company_name,
            "company_url": company_url,
            "location": job_location,
            "description": job_description,
            "listed_at": listed_at_readable,
            "apply_url": apply_url,
            "workplace_type": workplace_type,
            "custom_logo_url": custom_logo_url,
            "job_state": job_data.get("jobState", ""),
            "work_remote_allowed": job_data.get("workRemoteAllowed", False),
            "job_nature": ""  # Sera rempli dans la fonction de sauvegarde
        }
        jobs_structured.append(job_structured)
    
    # Sauvegarder les résultats
    save_jobs_incremental_to_json(jobs_structured, keywords, location, limit, 
                                  experience, job_type, remote, listed_at, distance)
    return job_results

def linkedin_job_search(keywords: str, location: str = '', limit: int = 10, use_enhanced_location: bool = True) -> str:
    """
    Fonction principale unifiée pour la recherche d'emplois LinkedIn.
    
    :param keywords: Mots-clés de recherche (ex: "SEO", "developer", "marketing manager")
    :param location: Nom de la ville ou région (ex: "Amsterdam", "Tokyo", "Berlin")
    :param limit: Nombre de résultats souhaités (défaut: 10)
    :param use_enhanced_location: Utiliser la géolocalisation améliorée (recommandé: True)
    :return: Résultats formatés des offres d'emploi
    """
    if location and use_enhanced_location:
        print(f"🔍 Recherche avec géolocalisation améliorée activée...")
        return search_jobs_with_proper_location(keywords, location, limit)
    else:
        print(f"🔍 Recherche avec méthode standard...")
        return search_jobs_direct(keywords, limit, 0, location)

def save_jobs_incremental_to_json(jobs_structured: list, keywords: str, location: str, limit: int,
                                     experience: list = None, job_type: list = None, remote: list = None, 
                                     listed_at: int = None, distance: int = None):
    """
    Save jobs data incrementally to a single consolidated JSON file.
    New searches are added to existing data, avoiding duplicates by job ID.
    
    :param jobs_structured: List of job data from current search
    :param keywords: Search keywords used
    :param location: Location searched
    :param limit: Number of jobs requested
    :param experience: Experience levels filter applied
    :param job_type: Job types filter applied
    :param remote: Remote work filter applied
    :param listed_at: Time filter applied (in seconds)
    :param distance: Distance filter applied (in miles)
    """
    # Create Exports directory if it doesn't exist
    exports_dir = "exports/Exports"
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
        print(f"📁 Dossier '{exports_dir}' créé")
    
    # Single consolidated filename
    consolidated_filename = "linkedin_job_searches_consolidated.json"
    filepath = os.path.join(exports_dir, consolidated_filename)
    
    # Load existing data if file exists
    existing_data = None
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            print(f"📄 Fichier existant trouvé: {len(existing_data.get('jobs', []))} offres")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️  Erreur lecture fichier existant: {e}. Création d'un nouveau fichier.")
            existing_data = None

    # Helper functions for filter descriptions
    def get_experience_description(codes):
        if not codes:
            return None
        exp_map = {"1": "Internship", "2": "Entry level", "3": "Associate", 
                   "4": "Mid-Senior level", "5": "Director", "6": "Executive"}
        return [exp_map.get(exp, exp) for exp in codes]
    
    def get_job_type_description(codes):
        if not codes:
            return None
        type_map = {"F": "Full-time", "C": "Contract", "P": "Part-time", 
                   "T": "Temporary", "I": "Internship", "V": "Volunteer", "O": "Other"}
        return [type_map.get(jt, jt) for jt in codes]
    
    def get_remote_description(codes):
        if not codes:
            return None
        remote_map = {"1": "On-site", "2": "Remote", "3": "Hybrid"}
        return [remote_map.get(r, r) for r in codes]
    
    def get_time_description(seconds):
        if not seconds:
            return None
        if seconds == 86400:
            return "Last 24 hours"
        elif seconds == 604800:
            return "Last week"
        elif seconds == 2592000:
            return "Last month"
        elif seconds == 7776000:
            return "Last 3 months"
        else:
            return f"Last {seconds} seconds"
    
    # Add job_nature to each job from search filters
    job_nature_description = ""
    if job_type:
        job_nature_description = ", ".join(get_job_type_description(job_type) or [])
    
    for job in jobs_structured:
        job["job_nature"] = job_nature_description

    # Create current search metadata
    current_search = {
        'keywords': keywords,
        'location': location,
        'limit_requested': limit,
        'jobs_found': len(jobs_structured),
        'search_timestamp': datetime.now().isoformat(),
        'search_filters': {
            'experience_levels': {
                'codes': experience,
                'description': get_experience_description(experience)
            },
            'job_types': {
                'codes': job_type,
                'description': get_job_type_description(job_type)
            },
            'remote_work': {
                'codes': remote,
                'description': get_remote_description(remote)
            },
            'time_posted': {
                'seconds': listed_at,
                'description': get_time_description(listed_at)
            },
            'distance_miles': distance
        }
    }
    
    # Initialize or update consolidated data structure
    if existing_data:
        # Merge with existing data
        consolidated_data = existing_data
        
        # Update global metadata
        consolidated_data['metadata']['last_updated'] = datetime.now().isoformat()
        consolidated_data['metadata']['total_searches'] += 1
        
        # Add current search to history
        consolidated_data['search_history'].append(current_search)
        
        # Get existing job IDs to avoid duplicates
        existing_job_ids = {job['id'] for job in consolidated_data['jobs']}
        
        # Add only new jobs (not duplicates)
        new_jobs = [job for job in jobs_structured if job['id'] not in existing_job_ids]
        consolidated_data['jobs'].extend(new_jobs)
        
        # Update total counts
        consolidated_data['metadata']['total_jobs'] = len(consolidated_data['jobs'])
        
        print(f"🔄 Ajout de {len(new_jobs)} nouvelles offres ({len(jobs_structured) - len(new_jobs)} doublons évités)")
        
    else:
        # Create new consolidated structure
        consolidated_data = {
            'metadata': {
                'creation_date': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_searches': 1,
                'total_jobs': len(jobs_structured),
                'data_coverage': 'Minimal - No duplicate fields',
                'export_version': 'incremental_v8.0'
            },
            'search_history': [current_search],
            'jobs': jobs_structured
        }
        print(f"📝 Création nouveau fichier consolidé avec {len(jobs_structured)} offres")

    # Save consolidated data to JSON file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(consolidated_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Fichier consolidé sauvegardé : {consolidated_filename}")
    print(f"📊 Total recherches : {consolidated_data['metadata']['total_searches']}")
    print(f"💼 Total offres uniques : {consolidated_data['metadata']['total_jobs']}")
    print(f"📁 Fichier : {filepath}")
    return filepath

if __name__ == "__main__":
    print("🔍 LINKEDIN JOB SEARCH - Version avec géolocalisation corrigée")
    print("="*60)
    
    # Exemple d'utilisation avec la nouvelle fonction de géolocalisation
    print("\n📍 TEST 1 - Recherche SEO à Amsterdam (Pays-Bas)")
    results_amsterdam = search_jobs_with_proper_location(
        keywords="SEO", 
        location="Amsterdam", 
        limit=5
    )
    print(f"✅ Résultats Amsterdam:\n{results_amsterdam}")
    
    print("\n📍 TEST 2 - Recherche Developer à Tokyo (Japon)")  
    results_tokyo = search_jobs_with_proper_location(
        keywords="developer",
        location="Tokyo",
        limit=5
    )
    print(f"✅ Résultats Tokyo:\n{results_tokyo}")
    
    print("\n📍 TEST 3 - Recherche Marketing à Berlin (Allemagne)")
    results_berlin = search_jobs_with_proper_location(
        keywords="marketing",
        location="Berlin", 
        limit=3
    )
    print(f"✅ Résultats Berlin:\n{results_berlin}")
    
    print("\n🎯 UTILISATION RECOMMANDÉE:")
    print("   search_jobs_with_proper_location(keywords='votre_recherche', location='votre_ville', limit=10)")
    print("\n📁 Les résultats sont automatiquement sauvegardés dans le dossier 'exports/Exports' au format JSON.")
    print("\n🌍 Villes testées avec succès : Amsterdam, Tokyo, Berlin, Los Angeles, Lisbonne, Madrid, Rome, Londres")