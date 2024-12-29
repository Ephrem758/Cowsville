from uuid import uuid4
from models import Farm

import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmManagerSystem.settings')  # Replace 'myproject' with your project name

# Setup Django
django.setup()

farms = Farm.objects.all()
for farm in farms:
    if not farm.farm_id:
        farm.farm_id = str(uuid4())  # Generate unique ID
        farm.save()
