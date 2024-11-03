#!/bin/bash

# Set strict error handling
set -euo pipefail

# Load environment variables if .env exists
if [ -f .env ]; then
  source .env
fi

# Validate required environment variables
if [ -z "$DATABASE_URL" ]; then
  log_error "Missing DATABASE_URL environment variable"
  exit 1
fi

if [ -z "$OPENAI_API_KEY" ]; then
  log_error "Missing OPENAI_API_KEY environment variable"
  exit 1
fi

# Set default values for optional variables
DEBUG="${DEBUG:-False}"
LOG_LEVEL="${LOG_LEVEL:-INFO}"

# Set project root directory
PROJECT_ROOT=$(dirname "$0")

# Set log file location
LOG_FILE="${PROJECT_ROOT}/app.log"

# Set PID file location
PID_FILE="${PROJECT_ROOT}/app.pid"

# Set service timeouts (in seconds)
DATABASE_TIMEOUT=30
BACKEND_TIMEOUT=60

# Set health check intervals (in seconds)
HEALTH_CHECK_INTERVAL=5

# Utility functions
log_info() {
  echo "$(date +"%Y-%m-%d %H:%M:%S") INFO: $*"
}

log_error() {
  echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR: $*" >&2
}

cleanup() {
  log_info "Cleaning up processes and files..."
  if [ -f "$PID_FILE" ]; then
    kill -9 $(cat "$PID_FILE")
  fi
  rm -f "$PID_FILE"
  # ... (add any other cleanup steps if needed)
}

check_dependencies() {
  log_info "Checking for dependencies..."
  which psql || log_error "psql not found. Install PostgreSQL."
  which pg_ctl || log_error "pg_ctl not found. Install PostgreSQL."
  which uvicorn || log_error "uvicorn not found. Install FastAPI."
}

# Health check functions
check_port() {
  local port="$1"
  nc -z localhost "$port" > /dev/null 2>&1
  return $?
}

wait_for_service() {
  local port="$1"
  local timeout="$2"
  local interval="$3"
  local elapsed=0
  while [[ "$elapsed" -lt "$timeout" ]]; do
    if check_port "$port"; then
      log_info "Service on port $port is ready"
      return 0
    fi
    sleep "$interval"
    elapsed=$((elapsed + interval))
  done
  log_error "Service on port $port not ready after $timeout seconds"
  exit 1
}

verify_service() {
  local port="$1"
  # ... (implement specific service health check)
}

# Service management functions
start_database() {
  log_info "Starting PostgreSQL..."
  pg_ctl start -D "/var/lib/postgresql/data"
  wait_for_service 5432 "$DATABASE_TIMEOUT" "$HEALTH_CHECK_INTERVAL"
  store_pid $(pgrep postgres)
  log_info "PostgreSQL started"
}

start_backend() {
  log_info "Starting backend server..."
  nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
  wait_for_service 8000 "$BACKEND_TIMEOUT" "$HEALTH_CHECK_INTERVAL"
  store_pid $(pgrep uvicorn)
  log_info "Backend server started on http://localhost:8000"
}

store_pid() {
  local pid="$1"
  echo "$pid" > "$PID_FILE"
}

# Main execution flow
check_dependencies
if [[ "$DATABASE_URL" == *"postgresql"* ]]; then
  start_database
fi
start_backend

# Trap exit signals
trap cleanup EXIT ERR

log_info "Application started successfully"