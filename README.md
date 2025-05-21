# Naukri.com Automated Job Application System
Automates daily job applications on Naukri.com with configurable keywords, location, and schedule.

## Quick Start
1. Clone the repository: `git clone <repo-url>`
2. Install dependencies: `./scripts/setup.sh`
3. Configure `.env` (see `config/.env.example`).
4. Run the application: `./scripts/run.sh`


Naukri.com Automated Job Application System
Automates daily job applications on Naukri.com with configurable keywords, location, and schedule.
Features

Automated Login: Securely logs into Naukri.com.
Job Search: Searches jobs based on keywords and location.
Job Applications: Applies to up to 50 jobs daily (Naukri’s limit).
Scheduling: Runs daily at a configurable time.
Logging: Detailed logs in logs/naukri_auto_apply.log.
Error Handling: Robust handling of timeouts, UI changes, and network issues.

Quick Start

Clone the Repository:git clone <repo-url>
cd naukri-auto-apply


Run Setup:./scripts/setup.sh


Configure:cp config/.env.example config/.env

Edit config/.env with your Naukri credentials, keywords, location, and schedule time.
Run:./scripts/run.sh



Documentation

Setup: docs/setup.md
User Guide: docs/user_guide.md
Developer Guide: docs/developer_guide.md
API Reference: docs/api_reference.md (generate with Sphinx)

Testing
pytest tests/
pytest --cov=src tests/

Deployment

Docker:docker build -t naukri-auto-apply:latest .
docker run --env-file config/.env naukri-auto-apply:latest


AWS EC2: Customize scripts/deploy.sh.

Compliance

Warning: Automation may violate Naukri.com’s terms. Verify with Naukri support.
Mitigation: Uses random delays and limits applications to 50/day.

License
MIT License (see LICENSE).

