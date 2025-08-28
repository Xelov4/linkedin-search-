# 🐳 Docker Guide - LinkedIn Job Search

## Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/Xelov4/linkedin-search-.git
cd linkedin-search-
cp .env.example .env
# Edit .env with your LinkedIn credentials
```

### 2. One-Command Launch
```bash
./run-docker.sh
```

## Installation Methods

### Method 1: Easy Script (Recommended)
```bash
# Make script executable (if needed)
chmod +x run-docker.sh

# Start interactive container
./run-docker.sh

# Run specific search
./run-docker.sh search "SEO specialist" "Los Angeles" 10 "F,C"
```

### Method 2: Docker Compose
```bash
# Build and start
docker compose up --build

# Run one-shot search
SEARCH_KEYWORDS="product manager" \
SEARCH_LOCATION="Paris" \
SEARCH_LIMIT=5 \
docker compose --profile oneshot run --rm linkedin-search-oneshot
```

### Method 3: Pure Docker
```bash
# Build image
docker build -t linkedin-job-search .

# Run container
docker run -it --name linkedin-search \
  -v $(pwd)/Exports:/app/Exports \
  -v $(pwd)/.env:/app/.env:ro \
  linkedin-job-search
```

## Usage Examples

### Interactive Mode
```bash
# Start container
./run-docker.sh interactive

# In another terminal, access Python
docker exec -it linkedin-job-search-app python

# Run searches
>>> import sys; sys.path.append('/app')
>>> from src.mcp_linkedin.client import linkedin_job_search_advanced
>>> linkedin_job_search_advanced("data scientist", "Berlin", 5)
```

### One-Shot Searches
```bash
# Basic search
./run-docker.sh search "product manager" "Tokyo" 10

# With job type filters (Full-time + Contract)
./run-docker.sh search "SEO expert" "Paris" 15 "F,C"

# Remote jobs only
./run-docker.sh search "developer" "Amsterdam" 20 "F" 
```

### Container Management
```bash
# View logs
./run-docker.sh logs

# Open shell in container
./run-docker.sh shell

# Stop container
./run-docker.sh stop

# Clean up everything
./run-docker.sh clean
```

## Configuration

### Environment Variables
```bash
# Required
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password

# Optional
DEBUG=false
```

### Search Parameters
- **Keywords**: Job title or skills ("product manager", "SEO specialist")
- **Location**: City name ("Paris", "Los Angeles", "Berlin")  
- **Limit**: Number of results (1-1000)
- **Job Types**: F=Full-time, C=Contract, P=Part-time, T=Temporary, I=Internship, V=Volunteer, O=Other

## File Structure
```
linkedin-search-/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-service setup
├── run-docker.sh          # Easy launcher script
├── .env.example           # Environment template
├── DOCKER.md              # This documentation
├── src/                   # Application source
├── Exports/               # Search results (mounted)
└── workflow*.md           # Technical documentation
```

## Data Persistence

### Results Export
- All search results saved to `./Exports/` directory
- Automatically mounted from container to host
- Files persist after container stops

### Volume Mounts
```yaml
volumes:
  - ./Exports:/app/Exports          # Results persistence
  - ./.env:/app/.env:ro             # Credentials (read-only)
```

## Networking

### Exposed Ports
- **8000**: Reserved for potential web interface
- **Interactive**: Access via `docker exec` commands

### Container Access
```bash
# Python shell
docker exec -it linkedin-job-search-app python

# System shell  
docker exec -it linkedin-job-search-app /bin/bash

# Direct search execution
docker exec -it linkedin-job-search-app python -c "
import sys; sys.path.append('/app');
from src.mcp_linkedin.client import linkedin_job_search_advanced;
linkedin_job_search_advanced('DevOps', 'Madrid', 8)
"
```

## Advanced Usage

### Custom Docker Build
```bash
# Build with specific tag
docker build -t my-linkedin-search:v1.0 .

# Build with build arguments
docker build --build-arg PYTHON_VERSION=3.12 -t linkedin-search .
```

### Multi-Stage Production Build
```dockerfile
# Add to Dockerfile for production
FROM linkedin-job-search as production
RUN pip install --no-cache-dir gunicorn
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Container Monitoring
```bash
# Resource usage
docker stats linkedin-job-search-app

# Container info
docker inspect linkedin-job-search-app

# Process list
docker exec linkedin-job-search-app ps aux
```

## Troubleshooting

### Common Issues

#### 1. Permission Denied
```bash
chmod +x run-docker.sh
sudo chown -R $USER:$USER Exports/
```

#### 2. LinkedIn Authentication Failed
```bash
# Check credentials in .env
cat .env
# Verify LinkedIn account is accessible
```

#### 3. Container Won't Start
```bash
# Check logs
docker logs linkedin-job-search-app
# Rebuild image
./run-docker.sh build
```

#### 4. No Results Found
```bash
# Test with basic search
./run-docker.sh search "manager" "Paris" 3
# Check network connectivity
docker exec linkedin-job-search-app curl -I https://linkedin.com
```

### Debug Mode
```bash
# Enable debug output
export DEBUG=true
./run-docker.sh

# Run with verbose logging
docker compose up --verbose linkedin-job-search
```

## Performance

### Resource Requirements
- **Memory**: 512MB minimum, 1GB recommended
- **CPU**: 1 core minimum
- **Disk**: 100MB for container + space for exports
- **Network**: Internet connection required

### Optimization
```bash
# Limit container resources
docker run --memory=1g --cpus=1 linkedin-job-search

# Clean up unused images
docker system prune -a
```

## Security

### Best Practices
- ✅ Non-root user in container (linkedin-user:1000)
- ✅ Read-only .env mount
- ✅ No sensitive data in image layers
- ✅ Health checks enabled
- ✅ Minimal base image (python:3.11-slim)

### Credential Protection
```bash
# Option 1: Environment variables
docker run -e LINKEDIN_EMAIL=xxx -e LINKEDIN_PASSWORD=xxx linkedin-job-search

# Option 2: Docker secrets (Swarm mode)
docker secret create linkedin_email email.txt
docker secret create linkedin_password password.txt
```

## Integration Examples

### CI/CD Pipeline
```yaml
# .github/workflows/linkedin-search.yml
name: Automated Job Search
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
jobs:
  search:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run job search
        run: |
          echo "LINKEDIN_EMAIL=${{ secrets.LINKEDIN_EMAIL }}" > .env
          echo "LINKEDIN_PASSWORD=${{ secrets.LINKEDIN_PASSWORD }}" >> .env
          ./run-docker.sh search "python developer" "remote" 50
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: linkedin-job-search
spec:
  replicas: 1
  selector:
    matchLabels:
      app: linkedin-search
  template:
    metadata:
      labels:
        app: linkedin-search
    spec:
      containers:
      - name: linkedin-search
        image: linkedin-job-search:latest
        env:
        - name: LINKEDIN_EMAIL
          valueFrom:
            secretKeyRef:
              name: linkedin-creds
              key: email
        - name: LINKEDIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: linkedin-creds
              key: password
        volumeMounts:
        - name: exports
          mountPath: /app/Exports
      volumes:
      - name: exports
        persistentVolumeClaim:
          claimName: linkedin-exports-pvc
```