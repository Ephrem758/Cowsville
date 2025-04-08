#!/bin/bash

# Get the current directory
CURRENT_DIR=$(pwd)
PYTHON_PATH=$(which python)  # Update this if using a virtual environment
MANAGE_PATH="$CURRENT_DIR/manage.py"

# Create the cron job command
CRON_CMD="0 0 * * * cd $CURRENT_DIR && $PYTHON_PATH $MANAGE_PATH check_heat_signs >> $CURRENT_DIR/heat_check.log 2>&1"

# Add the cron job
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo "Cron job has been created successfully!"
echo "The task will run daily at midnight to check for heat signs."
echo "Logs will be written to $CURRENT_DIR/heat_check.log" 