#!/bin/bash

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Functions for logging
log_error() {
    echo -e "${RED}ERROR [setup.reset_db] $1${NC}"
}

log_success() {
    echo -e "INFO  [setup.reset_db]${GREEN} $1${NC}"
}

log_info() {
    echo -e "INFO  [setup.reset_db] $1"
}

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | awk '/=/ {print $1}')
    log_success "Environment variables loaded successfully from .env file"
    log_info "DB_USER: $DB_USER"
    log_info "DB_PASS: $DB_PASS"
    log_info "DB_NAME: $DB_NAME"
else
    log_error "No .env file found"
    exit 1
fi

# Drop the database
setup/utils/drop_db.sh
if [ $? -eq 1 ]; then
    exit 1
fi

# Recreate the database
setup/utils/create_db.sh
if [ $? -eq 1 ]; then
    exit 1
fi

log_success "Database reset completed successfully."