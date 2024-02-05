#!/bin/bash

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Functions for logging
log_error() {
    echo -e "${RED}ERROR [setup.utils.create_db_user] $1${NC}"
}

log_success() {
    echo -e "INFO  [setup.utils.create_db_user]${GREEN} $1${NC}"
}

log_info() {
    echo -e "INFO  [setup.utils.create_db_user] $1"
}

# Load environment variables from .env file
export $(cat .env | grep -v '^#' | awk '/=/ {print $1}')

# Create the database user
log_info "Creating database user: $DB_USER"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';" &>/dev/null
if [ $? -eq 0 ]; then
    log_success "Successfully created user: $DB_USER"
else
    log_error "Failed to create user: $DB_USER"
    exit 1
fi
