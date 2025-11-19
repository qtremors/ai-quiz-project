#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install Dependencies
# Uses the requirements.txt file we generated earlier
pip install -r requirements.txt

# 2. Collect Static Files
# This gathers all CSS/JS/Images from your apps into the 'staticfiles' directory
# so WhiteNoise can serve them efficiently in production.
python manage.py collectstatic --no-input

# 3. Apply Migrations
# This updates the PostgreSQL database schema to match your models.py
python manage.py migrate