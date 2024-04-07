#!/bin/bash

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Functions for logging
log_error() {
    echo -e "${RED}ERROR [setup.utils.drop_db] $1${NC}"
}

log_warning() {
    echo -e "WARN  [setup.utils.drop_db]${RED} $1${NC}"
}

log_success() {
    echo -e "INFO  [setup.utils.drop_db]${GREEN} $1${NC}"
}

log_info() {
    echo -e "INFO  [setup.utils.drop_db] $1"
}

# Check if an argument is provided for the environment file
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -env)
            ENV_FILE="$2"
            shift
            shift
            ;;
        *)  # unknown option
            shift
            ;;
    esac
done

# Use default environment file if -env option is not provided
ENV_FILE="${ENV_FILE:-.env}"

# Load environment variables from "$ENV_FILE" file
export $(cat "$ENV_FILE" | grep -v '^#' | awk '/=/ {print $1}')

# Ask for confirmation
log_warning "WARNING: This will drop the database: $DB_NAME"
read -p "Are you sure you want to proceed? (y/N): " -n 1 -r
echo # Move to a new line

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Drop the database
    log_info "Dropping database: $DB_NAME"
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;" &>/dev/null
    if [ $? -eq 0 ]; then
        log_success "Successfully dropped database: $DB_NAME"
    else
        log_error "Failed to drop database: $DB_NAME"
        exit 1
    fi
else
    log_info "Database reset aborted."
    exit 1
fi
