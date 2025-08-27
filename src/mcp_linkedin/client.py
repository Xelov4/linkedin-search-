from linkedin_api import Linkedin
from fastmcp import FastMCP
import os
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

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
        posts += f"Post by {urn["author_name"]}: {urn["content"]}\n"

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
            "entity_urn": job_data.get("entityUrn", ""),
            "dash_entity_urn": job_data.get("dashEntityUrn", ""),
            "job_posting_id": job_data.get("jobPostingId", ""),
            
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
    save_jobs_ultra_complete_to_json(jobs_structured, keywords, location, limit)
    
    return job_results

def save_jobs_ultra_complete_to_json(jobs_structured: list, keywords: str, location: str, limit: int):
    """
    Save ultra-complete jobs data to JSON file with 100% data coverage.
    
    :param keywords: Search keywords used
    :param location: Location searched
    :param limit: Number of jobs requested
    """
    # Create Exports directory if it doesn't exist
    exports_dir = "Exports"
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
        print(f"📁 Dossier '{exports_dir}' créé")
    
    # Process jobs to add custom_logo_url
    for job in jobs_structured:
        # Extract logo information and build custom logo URL
        company_details = job.get("company_details", {})
        custom_logo_url = ""
        
        if company_details and "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany" in company_details:
            company_data = company_details["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]
            if "companyResolutionResult" in company_data:
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
        
        # Add custom_logo_url to the job data
        job["custom_logo_url"] = custom_logo_url
    
    # Format date in French style
    current_date = datetime.now()
    date_str = current_date.strftime("%d-%B-%Y").lower()
    time_str = current_date.strftime("%Hh-%M")
    
    # Format keywords and location for filename
    keywords_clean = keywords.lower().replace(' ', '_').replace('&', 'et').replace('/', '_')
    location_clean = location.lower().replace(' ', '_').replace('&', 'et').replace('/', '_')
    
    # Create filename in the requested format
    filename = f"{keywords_clean}_{location_clean}_{limit}_{date_str}_{time_str}.json"
    filepath = os.path.join(exports_dir, filename)
    
    # Create the data structure to save
    data_to_save = {
        'search_info': {
            'keywords': keywords,
            'location': location,
            'limit_requested': limit,
            'jobs_found': len(jobs_structured),
            'search_timestamp': datetime.now().isoformat(),
            'data_coverage': '100% - All available fields extracted',
            'export_version': 'ultra_complete_v1.0'
        },
        'jobs': jobs_structured
    }
    
    # Save to JSON file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Données ultra-complètes sauvegardées dans le fichier : {filepath}")
    print(f"📊 Couverture des données : 100% - Tous les champs disponibles extraits")
    print(f"📁 Fichier placé dans le dossier : {exports_dir}")
    return filepath

if __name__ == "__main__":
    print("🔍 Recherche de jobs à Saint-Denis (France)...")
    results = search_jobs_direct(keywords="", location="Saint-Denis", limit=50)
    print("\n📋 Résultats de la recherche :")
    print(results)