#!/bin/bash

# LinkedIn Job Search Docker Runner
# Usage: ./run-docker.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 LinkedIn Job Search Docker Setup${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${RED}❗ Please edit .env file with your LinkedIn credentials before running!${NC}"
    echo -e "${YELLOW}   Edit: LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env${NC}"
    exit 1
fi

# Create Exports directory if it doesn't exist
mkdir -p Exports

case "${1:-interactive}" in
    "build")
        echo -e "${BLUE}🏗️  Building Docker image...${NC}"
        docker compose build
        echo -e "${GREEN}✅ Build completed!${NC}"
        ;;
    
    "interactive")
        echo -e "${BLUE}🚀 Starting interactive LinkedIn job search container...${NC}"
        echo -e "${YELLOW}💡 Access the container with: docker exec -it linkedin-job-search-app python${NC}"
        docker compose up linkedin-job-search
        ;;
    
    "search")
        # One-shot search mode
        KEYWORDS=${2:-"product manager"}
        LOCATION=${3:-"Paris"}
        LIMIT=${4:-5}
        JOB_TYPE=${5:-""}
        
        echo -e "${BLUE}🔍 Running one-shot search...${NC}"
        echo -e "${YELLOW}Keywords: ${KEYWORDS}${NC}"
        echo -e "${YELLOW}Location: ${LOCATION}${NC}"
        echo -e "${YELLOW}Limit: ${LIMIT}${NC}"
        
        SEARCH_KEYWORDS="$KEYWORDS" \
        SEARCH_LOCATION="$LOCATION" \
        SEARCH_LIMIT="$LIMIT" \
        SEARCH_JOB_TYPE="$JOB_TYPE" \
        docker compose --profile oneshot run --rm linkedin-search-oneshot
        ;;
    
    "shell")
        echo -e "${BLUE}🐚 Opening shell in LinkedIn job search container...${NC}"
        docker compose exec linkedin-job-search /bin/bash
        ;;
    
    "logs")
        echo -e "${BLUE}📋 Showing container logs...${NC}"
        docker compose logs -f linkedin-job-search
        ;;
    
    "stop")
        echo -e "${BLUE}🛑 Stopping LinkedIn job search container...${NC}"
        docker compose down
        echo -e "${GREEN}✅ Container stopped!${NC}"
        ;;
    
    "clean")
        echo -e "${BLUE}🧹 Cleaning up Docker resources...${NC}"
        docker compose down --volumes --remove-orphans
        docker system prune -f
        echo -e "${GREEN}✅ Cleanup completed!${NC}"
        ;;
    
    "help"|*)
        echo -e "${GREEN}Usage: ./run-docker.sh [command]${NC}"
        echo ""
        echo -e "${YELLOW}Commands:${NC}"
        echo -e "  ${GREEN}build${NC}        Build the Docker image"
        echo -e "  ${GREEN}interactive${NC}  Start interactive container (default)"
        echo -e "  ${GREEN}search${NC}       Run one-shot search: ./run-docker.sh search \"keywords\" \"location\" limit \"job_type\""
        echo -e "  ${GREEN}shell${NC}        Open shell in running container"
        echo -e "  ${GREEN}logs${NC}         Show container logs"
        echo -e "  ${GREEN}stop${NC}         Stop the container"
        echo -e "  ${GREEN}clean${NC}        Clean up Docker resources"
        echo -e "  ${GREEN}help${NC}         Show this help"
        echo ""
        echo -e "${YELLOW}Examples:${NC}"
        echo -e "  ./run-docker.sh search \"SEO specialist\" \"Los Angeles\" 10 \"F,C\""
        echo -e "  ./run-docker.sh search \"product manager\" \"Berlin\" 5"
        echo ""
        echo -e "${YELLOW}Job Types (comma-separated):${NC}"
        echo -e "  F = Full-time, C = Contract, P = Part-time, T = Temporary"
        echo -e "  I = Internship, V = Volunteer, O = Other"
        ;;
esac