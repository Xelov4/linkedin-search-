# LinkedIn Job Search Application - Dockerized
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create requirements.txt from dependencies
RUN echo "linkedin-api==2.3.0" > requirements.txt && \
    echo "fastmcp>=0.2.0" >> requirements.txt && \
    echo "python-dotenv>=1.0.0" >> requirements.txt && \
    echo "requests>=2.31.0" >> requirements.txt && \
    echo "uvicorn>=0.24.0" >> requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/ ./src/
COPY workflow*.md ./
COPY README.md ./
COPY .env.example .env
COPY startup.py ./
COPY oneshot.py ./

# Create Exports directory for job search results
RUN mkdir -p Exports

# Create non-root user for security
RUN useradd -m -u 1000 linkedin-user && chown -R linkedin-user:linkedin-user /app
# Ensure Exports directory is writable
RUN chmod 755 /app/Exports
USER linkedin-user

# Set Python path
ENV PYTHONPATH=/app

# Expose port for potential web interface
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.append('/app'); from src.mcp_linkedin.client import linkedin_job_search_advanced; print('OK')" || exit 1

# Default command - interactive Python with job search ready
CMD ["python", "-c", "print('🔍 LinkedIn Job Search Docker Container Ready!'); print(''); print('Quick start examples:'); print('import sys; sys.path.append(\"/app\")'); print('from src.mcp_linkedin.client import linkedin_job_search_advanced'); print(''); print('# Search examples:'); print('linkedin_job_search_advanced(\"product manager\", \"Paris\", 5)'); print('linkedin_job_search_advanced(\"SEO specialist\", \"Los Angeles\", 10, job_type=[\"F\", \"C\"])'); print(''); print('Results will be saved in /app/Exports/'); print(''); import time; time.sleep(3600)"]