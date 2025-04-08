# Get the current directory
$currentDir = Get-Location
$pythonPath = "python"  # Update this if using a virtual environment
$managePath = Join-Path $currentDir "manage.py"

# Create the scheduled task
$taskName = "CowsvilleHeatCheck"
$taskDescription = "Check cow heat signs every 24 hours"

# Create the action to run the management command
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "$managePath check_heat_signs"

# Create the trigger (run daily at midnight)
$trigger = New-ScheduledTaskTrigger -Daily -At 12am

# Register the task (will prompt for admin credentials)
Register-ScheduledTask -TaskName $taskName -Description $taskDescription -Action $action -Trigger $trigger -RunLevel Highest

Write-Host "Scheduled task '$taskName' has been created successfully!"
Write-Host "The task will run daily at midnight to check for heat signs."
Write-Host "You can view and modify the task in Task Scheduler." 