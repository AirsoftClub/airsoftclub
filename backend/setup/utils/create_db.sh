#!/bin/bash

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Functions for logging
log_error() {
    echo -e "${RED}ERROR [setup.utils.create_db] $1${NC}"
}

log_success() {
    echo -e "INFO  [setup.utils.create_db]${GREEN} $1${NC}"
}

log_info() {
    echo -e "INFO  [setup.utils.create_db] $1"
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

# Create the database
log_info "Creating database: $DB_NAME"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" &>/dev/null
if [ $? -eq 0 ]; then
    log_success "Successfully created database: $DB_NAME"
else
    log_error "Failed to create database: $DB_NAME (Already exists?)"
    exit 1
fi

# Grant all privileges of the database to the user
log_info "Granting privileges to $DB_USER on $DB_NAME"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" &>/dev/null
if [ $? -eq 0 ]; then
    log_success "Successfully granted privileges to $DB_USER on $DB_NAME"
else
    log_error "Failed to grant privileges to $DB_USER on $DB_NAME"
    exit 1
fi

# Run migrations
log_info "Running migrations for $DB_NAME"
alembic upgrade head
if [ $? -eq 0 ]; then
    log_success "Successfully ran migrations for $DB_NAME"
else
    log_error "Failed to run migrations for $DB_NAME"
    exit 1
fi

# TODO: Seed the database
# log_info "Seeding the database for $DB_NAME"
# python3 seed.py
# if [ $? -eq 0 ]; then
#     log_success "Successfully seeded the database for $DB_NAME"
# else
#     log_error "Failed to seed the database for $DB_NAME"
#     exit 1
# fi
