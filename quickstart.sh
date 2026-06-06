#!/bin/bash
# Prompt-to-Prod Quick Start Script

set -e

echo "========================================="
echo "Prompt-to-Prod Platform Quick Start"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
echo -e "${BLUE}[1/5] Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker not found. Please install Docker Desktop.${NC}"
    exit 1
fi
docker --version
echo -e "${GREEN}✓ Docker is installed${NC}"
echo ""

# Setup .env
echo -e "${BLUE}[2/5] Setting up environment...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env and add your OPENAI_API_KEY${NC}"
    echo -e "${YELLOW}Then run this script again.${NC}"
    exit 0
fi
echo -e "${GREEN}✓ .env file exists${NC}"
echo ""

# Load environment
source .env

# Build image
echo -e "${BLUE}[3/5] Building Docker image...${NC}"
docker build -t p2p-agent:latest ./ai-agent
echo -e "${GREEN}✓ Image built successfully${NC}"
echo ""

# Start services
echo -e "${BLUE}[4/5] Starting services...${NC}"
docker compose up -d
echo -e "${GREEN}✓ Services started${NC}"
echo ""

# Wait for health check
echo -e "${BLUE}[5/5] Waiting for services to be healthy...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ API is healthy${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${YELLOW}⚠ API health check timeout. Check logs with: docker compose logs${NC}"
    fi
    echo -n "."
    sleep 1
done
echo ""
echo ""

# Summary
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}✓ Prompt-to-Prod Platform is Running!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Access points:"
echo -e "  ${BLUE}API${NC}:        http://localhost:8000"
echo -e "  ${BLUE}API Docs${NC}:    http://localhost:8000/docs"
echo -e "  ${BLUE}Health${NC}:      http://localhost:8000/health"
echo -e "  ${BLUE}Metrics${NC}:     http://localhost:8000/metrics"
echo -e "  ${BLUE}Database${NC}:    localhost:5432 (admin/postgres123)"
echo ""
echo "Quick commands:"
echo -e "  ${BLUE}View logs${NC}:       docker compose logs -f"
echo -e "  ${BLUE}Stop services${NC}:   docker compose down"
echo -e "  ${BLUE}Test API${NC}:        curl http://localhost:8000/health"
echo ""
echo "Next steps:"
echo "  1. Test the API with curl or Postman"
echo "  2. Deploy to Kubernetes: kubectl apply -f manifests/"
echo "  3. Run tests: pytest ai-agent/tests/ -v"
echo "  4. Check DEPLOYMENT.md for full setup guide"
echo ""
