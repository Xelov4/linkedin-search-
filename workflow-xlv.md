# LinkedIn Job Search Process - Ultra Minimal

## 1. Search Initialization
- **Function**: `linkedin_job_search_advanced()` in `src/mcp_linkedin/client.py`
- **Input**: keywords, location, limit, job_type, experience, remote, listed_at, distance
- **Authentication**: Auto-loads `.env` credentials with `load_dotenv()`

## 2. Location Processing
- **Function**: `get_location_id()` in `src/mcp_linkedin/client.py`
- **API**: `https://www.linkedin.com/voyager/api/voyagerSearchDashClusters?decorationId=...&query=(typeaheadHitType:GEO,query:{location_name})`
- **Process**: City name → LinkedIn geoId (e.g., "Paris" → 101240143)

## 3. Search Query Construction
- **Function**: `search_jobs_with_proper_location()` in `src/mcp_linkedin/client.py`
- **API**: `voyagerJobsDashJobCards` with `locationUnion:(geoId:ID)` syntax
- **Filters**: jobType, workplaceType, experienceLevel, timePostedRange, distance

## 4. Job Data Retrieval
- **API**: `voyager/api/jobs/jobPostings/{job_id}?decorationId=WebLightJobPosting-23`
- **Process**: For each job ID from search results, fetch complete job details
- **Data**: Full LinkedIn job posting object with all available fields

## 5. Data Processing & Extraction
- **Location**: Within each search function loop
- **Extract**: 
  - Basic info: id, title, company, location, description
  - Company data: name, URL, logo from nested `companyDetails`
  - Application: URL from `apply_method.companyApplyUrl`
  - Workplace: type from `workplaceTypesResolutionResults.localizedName`
  - Timing: timestamp conversion from Unix to readable format
  - Custom: LinkedIn job URL generation

## 6. Structure Assembly
- **Format**: 11-field minimal structure (no duplicates)
- **Fields**: id, linkedin_postJob_url, title, company, company_url, location, description, listed_at, apply_url, workplace_type, custom_logo_url, job_state, work_remote_allowed, job_nature

## 7. Filter Integration
- **Function**: `get_job_type_description()` in save function
- **Process**: Convert filter codes to human descriptions for `job_nature` field
- **Example**: ['F', 'C'] → "Full-time, Contract"

## 8. Export Generation  
- **Function**: `save_jobs_ultra_complete_to_json()` in `src/mcp_linkedin/client.py`
- **Structure**: search_info + search_filters + jobs array
- **Format**: JSON with UTF-8 encoding, 2-space indentation
- **Version**: minimal_v7.0

## 9. File Output
- **Directory**: `Exports/`
- **Naming**: `{keywords}_{location}_{limit}_{date}_{time}.json`
- **Example**: `sea_project_manager_marseille_5_27-august-2025_22h-29.json`

## Core Files
- `src/mcp_linkedin/client.py`: All search and processing functions
- `.env`: LinkedIn credentials (LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
- `Exports/`: Generated JSON output directory