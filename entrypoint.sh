#!/bin/sh

set -e  # Exit on any error

# Function to check database connection
check_db_connection() {
    echo "Waiting for database..."
    local max_attempts=30
    local attempt=1
    
    until python -c "
import os
import psycopg2
import sys

try:
    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        connect_timeout=3
    )
    conn.close()
    print('Database connection successful')
    sys.exit(0)
except psycopg2.OperationalError as e:
    print(f'Database connection attempt {${attempt}}/${max_attempts} failed: {e}')
    sys.exit(1)
except KeyError as e:
    print(f'Missing environment variable: {e}')
    sys.exit(1)
except Exception as e:
    print(f'Unexpected error: {e}')
    sys.exit(1)
"; do
        if [ $attempt -ge $max_attempts ]; then
            echo "Max database connection attempts reached. Exiting."
            exit 1
        fi
        
        echo "Database not ready, waiting... (Attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    echo "Database is ready!"
}

# Function to create migrations for an app if needed
create_migrations() {
    local app_name=$1
    local migration_dir="${app_name}/migrations"
    local initial_migration="${migration_dir}/0001_initial.py"
    
    if [ ! -d "$migration_dir" ] || [ ! -f "$initial_migration" ]; then
        echo "Creating migrations for ${app_name}..."
        python manage.py makemigrations "$app_name" --no-input
    else
        echo "Migrations already exist for ${app_name}"
    fi
}

# Function to apply migrations if needed
apply_migrations() {
    echo "Checking for unapplied migrations..."
    if python manage.py showmigrations --plan | grep -q '\[ \]'; then
        echo "Applying migrations..."
        python manage.py migrate --no-input
    else
        echo "All migrations are already applied."
    fi
}

# Function to collect static files if needed
collect_static() {
    if [ "$DEBUG" = "0" ]; then
        echo "Collecting static files..."
        python manage.py collectstatic --no-input --clear
    else
        echo "DEBUG mode is enabled, skipping static file collection."
    fi
}

# Function to create superuser if needed
create_superuser() {
    echo "Checking if superuser needs to be created..."
    python manage.py shell << EOF
import os
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError

User = get_user_model()
admin_email = os.environ.get('SUPERUSER_EMAIL')
admin_password = os.environ.get('SUPERUSER_PASSWORD')

try:
    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(
            email=admin_email,
            password=admin_password,
            first_name='Admin',
            last_name='User'
        )
        print('Superuser created successfully')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f'Error creating superuser: {e}')
EOF
}

# Main execution
main() {
    # Check database connection
    check_db_connection
    
    
    for app in locations users categories; do
        if [ -d "$app" ]; then
            create_migrations "$app"
        else
            echo "Warning: App directory '$app' not found, skipping migrations"
        fi
    done
    
    # Apply migrations
    apply_migrations
    
    # Collect static files in production
    collect_static
    
    # Create superuser
    create_superuser
    
    echo "Initialization complete. Starting server..."
    exec "$@"
}

# Run main function
main "$@"