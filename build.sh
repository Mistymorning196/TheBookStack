#!/bin/bash

# Install requirements (Python packages)
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create the superuser if it doesn't exist already
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError

# Get the User model
User = get_user_model()

# Try to create the superuser
try:
    # Check if the superuser already exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',  # You can change this to any email
            password='adminpassword'  # Use a secure password or set via environment variable
        )
except IntegrityError:
    print("Superuser already exists.")
EOF

# Restart the server if necessary (depends on your provider)
