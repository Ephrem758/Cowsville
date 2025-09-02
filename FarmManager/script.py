"""
Farm ID Update Script

This script updates farms that don't have farm_id values by generating unique UUIDs.
It's designed to be run as a one-time migration script.
"""

import os
import django
import logging
from uuid import uuid4

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "FarmManagerSystem.settings"
    )
    django.setup()

def update_farm_ids():
    """Update farms without farm_id values"""
    try:
        from .models import Farm
        
        farms_without_id = Farm.objects.filter(farm_id__isnull=True) | Farm.objects.filter(farm_id='')
        total_farms = farms_without_id.count()
        
        if total_farms == 0:
            logger.info("No farms found without farm_id. All farms already have IDs.")
            return
            
        logger.info(f"Found {total_farms} farms without farm_id. Updating...")
        
        updated_count = 0
        for farm in farms_without_id:
            old_id = farm.farm_id
            farm.farm_id = str(uuid4())
            farm.save()
            logger.info(f"Updated farm: {old_id or 'None'} -> {farm.farm_id}")
            updated_count += 1
            
        logger.info(f"Successfully updated {updated_count} farms with new farm_ids.")
        
    except Exception as e:
        logger.error(f"Error updating farm IDs: {str(e)}")
        raise

def main():
    """Main function to run the script"""
    try:
        logger.info("Starting farm ID update script...")
        setup_django()
        update_farm_ids()
        logger.info("Farm ID update script completed successfully.")
        
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
