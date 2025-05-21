Setup Guide for Naukri Auto Apply
Prerequisites

OS: Linux, macOS, or Windows (with WSL for scripts)
Python: 3.8 or higher
Chrome Browser: Latest version
Dependencies: Listed in requirements.txt
Naukri.com Account: Valid account with completed profile

Installation Steps

Clone the Repository:
git clone <repo-url>
cd naukri-auto-apply


Run Setup Script:
./scripts/setup.sh

This installs dependencies and checks for Python 3.8+.

Configure Environment:

Copy the example environment file:cp config/.env.example config/.env


Edit config/.env with your details:NAUKRI_USERNAME=your_email
NAUKRI_PASSWORD=your_password
KEYWORDS=software engineer
LOCATION=Bangalore
SCHEDULE_TIME=09:00
MAX_APPLICATIONS=50




Verify Logging Configuration:

Ensure config/logging.yaml exists (created by setup script).
Logs are written to logs/naukri_auto_apply.log.



Troubleshooting

Dependency Errors: Check logs/setup.log for pip errors. Run pip install -r requirements.txt manually.
Python Version: Ensure Python 3.8+ is installed (python3 --version).
.env Missing: Copy config/.env.example to config/.env and configure.


