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
if [ -f "$ENV_FILE" ]; then
    export $(cat "$ENV_FILE" | grep -v '^#' | awk '/=/ {print $1}')
    log_success "Environment variables loaded successfully from '$ENV_FILE' file"
    log_info "DB_USER: $DB_USER"
    log_info "DB_PASS: $DB_PASS"
    log_info "DB_NAME: $DB_NAME"
else
    log_error "Specified environment file '$ENV_FILE' not found"
    exit 1
fi

# Create the database user (ignore errors if user already exists)
./setup/utils/create_db_user.sh -env "$ENV_FILE"

# Create the database (ignore errors if database already exists)
./setup/utils/create_db.sh -env "$ENV_FILE"

log_success "Database setup completed successfully."
