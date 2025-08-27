# LinkedIn Job Search Workflow

## 1. Search Execution
- **Function**: `linkedin_job_search_advanced()` in `src/mcp_linkedin/client.py`
- **Process**: Executes advanced job search with filters (keywords, location, job_type, experience, remote, etc.)

## 2. Location Processing
- **Function**: `get_location_id()` in `src/mcp_linkedin/client.py`
- **Process**: Converts city name to LinkedIn geoId using typeaheadHits API endpoint

## 3. API Query Construction
- **Function**: `search_jobs_with_proper_location()` in `src/mcp_linkedin/client.py`
- **Process**: Builds voyagerJobsDashJobCards query with locationUnion:(geoId:ID) syntax and filters

## 4. Data Retrieval
- **Function**: `client.get_job(job_id=job_id)` in `src/mcp_linkedin/client.py`
- **Process**: Fetches complete job data for each job posting ID from search results

## 5. Data Structuring
- **Function**: Job processing loop in `linkedin_job_search_advanced()`
- **Process**: Extracts 50+ fields into ultra-complete job_structured dictionary

## 6. Export Generation
- **Function**: `save_jobs_ultra_complete_to_json()` in `src/mcp_linkedin/client.py`
- **Process**: Creates JSON file with search_info metadata and structured jobs array

## 7. File Output
- **Location**: `Exports/{keywords}_{location}_{limit}_{date}_{time}.json`
- **Format**: Ultra-complete v3.0 with all LinkedIn API fields and custom URLs

---

# Extracted Fields Analysis (Verified from Real Data)

## Critical Fields (Must Keep)
- **id**: Job posting unique identifier - Essential for tracking
- **job_posting_id**: LinkedIn's internal job ID - Critical for URL generation  
- **title**: Job position title - Critical for relevance filtering
- **company**: Company name - Critical for company targeting
- **location**: Job geographic location - Critical for location filtering
- **description**: Complete job description text - Critical for content analysis
- **company_details**: Full company structure with logo/URL - Critical for company research
- **listed_at**: Job posting timestamp (Unix) - Critical for freshness tracking (always populated)
- **apply_method.companyApplyUrl**: External application URL - Critical for direct application (96% populated)
- **workplace_types_resolution_results**: Work mode details (Remote/Hybrid/On-site) - Critical for remote work filtering
- **custom_logo_url**: Company logo URL 400x400 - Critical for visual display (always populated)
- **job_state**: Job status (LISTED/CLOSED) - Critical for filtering active jobs

## Optional Fields (Sometimes Useful)  
- **entity_urn**: Full LinkedIn URN identifier - Optional for advanced tracking
- **dash_entity_urn**: Dashboard entity URN - Optional for internal references
- **work_remote_allowed**: Boolean remote flag - Optional backup for workplace_types
- **workplace_types**: Work arrangement URN codes - Optional as structured backup
- **recipe_type**: API response type identifier - Optional for debugging

## Useless Fields (Always Empty - Remove)
- **seniority_level**: Experience level - Always empty string ""
- **employment_type**: Job type - Always empty string ""  
- **industry_name**: Company industry - Always empty string ""
- **posting_timestamp**: Alternative date - Always empty string ""
- **created_at**: Creation timestamp - Always empty string ""
- **updated_at**: Update timestamp - Always empty string ""
- **application_url**: Alternative app URL - Always empty string ""
- **application_type**: App method type - Always empty string ""
- **tracking_id**: Internal tracking - Always empty string ""
- **job_posting_status**: Status code - Always empty string ""
- **experience_level**: Experience requirement - Always empty string ""
- **education_level**: Education requirement - Always empty string ""
- **country**: Country code - Always empty string ""
- **city**: City name - Always empty string ""
- **postal_code**: ZIP code - Always empty string ""
- **company_size**: Employee count - Always empty string ""
- **company_type**: Company legal type - Always empty string ""
- **travel_requirements**: Travel % - Always empty string ""
- **relocation_assistance**: Relocation help - Always empty string ""
- **internal_job**: Internal flag - Always empty string ""
- **sponsored_job**: Sponsored flag - Always empty string ""
- **premium_job**: Premium flag - Always empty string ""

## Useless Fields (Always Empty Arrays - Remove)
- **skills**: Required skills - Always empty array []
- **benefits**: Company benefits - Always empty array []
- **job_functions**: Job categories - Always empty array []
- **job_categories**: Alternative categories - Always empty array []
- **certifications**: Required certs - Always empty array []
- **languages**: Language requirements - Always empty array []

## Useless Fields (Always Empty Objects - Remove)  
- **employment_status**: Status object - Always empty object {}
- **requirements**: Requirements object - Always empty object {}
- **salary_insights**: Salary data - Always empty object {}
- **compensation**: Compensation details - Always empty object {}
- **location_details**: Location breakdown - Always empty object {}

## Redundant Fields (Remove)
- **talent_hub_job**: Always false - Useless for external users
- **raw_data_complete**: Full API dump - Redundant with structured fields
- **all_available_keys**: Available field list - Redundant metadata