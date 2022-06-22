#!/bin/bash

cd DjangoShop

#Start Tests
echo "Starting tests"
poetry shell
pytest -rP

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000