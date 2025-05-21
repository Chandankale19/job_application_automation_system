User Guide for Naukri Auto Apply
Overview
The Naukri Auto Apply system automates job applications on Naukri.com, running daily at a specified time with configurable search criteria.
Configuration

Edit config/.env:

NAUKRI_USERNAME: Your Naukri.com email.
NAUKRI_PASSWORD: Your Naukri.com password.
KEYWORDS: Job search keywords (e.g., software engineer).
LOCATION: Job location (e.g., Bangalore).
SCHEDULE_TIME: Daily run time in HH:MM format (e.g., 09:00).
MAX_APPLICATIONS: Maximum applications per day (1–50, default 50).


Example:
NAUKRI_USERNAME=test@example.com
NAUKRI_PASSWORD=secret123
KEYWORDS=data scientist
LOCATION=Hyderabad
SCHEDULE_TIME=08:30
MAX_APPLICATIONS=40



Running the Application

Start the Application:
./scripts/run.sh

Or:
python3 src/main.py


Monitor Logs:

Check logs/naukri_auto_apply.log for runtime information, errors, and application counts.



Stopping the Application

Press Ctrl+C to stop the scheduler gracefully.
Logs will indicate a clean shutdown.

Compliance Note

Naukri.com Terms: Automation may violate Naukri’s terms of service. Verify compliance with Naukri support.
Risk Mitigation: The system uses random delays and limits applications to 50 per day.

Troubleshooting

No Applications: Check logs/naukri_auto_apply.log for errors (e.g., login failure, no jobs found).
Login Issues: Verify NAUKRI_USERNAME and NAUKRI_PASSWORD in config/.env.
Schedule Not Running: Ensure SCHEDULE_TIME is in HH:MM format and the system is running.


