#!/bin/bash

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Functions for logging
log_error() {
    echo -e "${RED}ERROR [setup.setup_db] $1${NC}"
}

log_success() {
    echo -e "INFO  [setup.setup_db]${GREEN} $1${NC}"
}

log_info() {
    echo -e "INFO  [setup.setup_db] $1"
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

# Create the database user (ignore errors if user already exists)
setup/utils/create_db_user.sh

# Create the database (ignore errors if database already exists)
setup/utils/create_db.sh

log_success "Database setup completed successfully."
