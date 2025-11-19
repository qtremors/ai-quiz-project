#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install Dependencies
# (We keep this at the root because requirements.txt is at the root)
pip install -r requirements.txt

# 2. Move into the project folder where manage.py is
cd qtrmrs

# 3. Collect Static Files
python manage.py collectstatic --no-input

# 4. Apply Migrations
python manage.py migrate