#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_NAME="CourtCaseMonitor"
MODE=$1

if [[ "$MODE" != "dev" && "$MODE" != "prod" ]]; then
  echo -e "${RED}Invalid mode. Use: dev or prod${NC}"
  echo "Example: ./manage.sh dev"
  exit 1
fi

if [ "$MODE" == "dev" ]; then
  echo -e "${CYAN}Starting ${PROJECT_NAME} in development mode...${NC}"
  docker-compose up --build
else
  echo -e "${CYAN}Starting ${PROJECT_NAME} in production mode...${NC}"
  docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
fi
