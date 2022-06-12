#!/bin/bash

# Collect static files
# echo "Collect static files"
# python DjangoShop/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python DjangoShop/manage.py migrate

# Start server
echo "Starting server"
python DjangoShop/manage.py runserver 0.0.0.0:8000