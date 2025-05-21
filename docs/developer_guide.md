# Developer Guide for Naukri Auto Apply

## Project Structure
- `src/`: Source code (main.py, config/, automation/, scheduler/, logger/).
- `tests/`: Unit and integration tests.
- `scripts/`: Setup, run, and deploy scripts.
- `docs/`: Documentation.
- `config/`: Configuration files (.env, logging.yaml).
- `logs/`: Runtime logs.
- `.github/workflows/`: CI/CD pipelines.

## Key Modules
- **config/settings.py**: Loads and validates .env variables.
- **automation/browser.py**: Manages Selenium WebDriver.
- **automation/naukri.py**: Handles Naukri.com automation (login, apply).
- **scheduler/job_scheduler.py**: Schedules daily job applications.
- **logger/logging_config.py**: Configures logging.

## Updating XPath Selectors
- **Issue**: Naukri.com UI changes may break XPath selectors in `naukri.py`.
- **Solution**:
  1. Check `logs/naukri_auto_apply.log` for `NoSuchElementException`.
  2. Inspect Naukri.com’s HTML using Chrome DevTools.
  3. Update selectors in `naukri.py` (e.g., `usernameField`, `passwordField`).
  4. Test changes with `tests/unit/test_naukri.py`.

## Adding New Platforms
- **Steps**:
  1. Create a new module in `src/automation/` (e.g., `linkedin.py`).
  2. Implement login and apply_to_jobs methods, following `naukri.py`.
  3. Update `job_scheduler.py` to support multiple platforms.
  4. Add tests in `tests/unit/` and `tests/integration/`.

## Testing
- **Run Tests**:
   ```bash
   pytest tests/
   ```
- **Coverage**:
   ```bash
   pytest --cov=src tests/
   ```
- **Update Tests**: Add new tests in `tests/unit/` for new features.

## Deployment
- **Docker**:
  - Build: `docker build -t naukri-auto-apply:latest .`
  - Run: `docker run --env-file config/.env naukri-auto-apply:latest`
- **AWS EC2**:
  - Customize `scripts/deploy.sh` for your EC2 instance.
  - Use `Dockerfile` for containerized deployment.

## Error Handling
- **Custom Exceptions**: `ConfigError`, `BrowserError`, `NaukriError`, `SchedulerError`, `LoggingConfigError`.
- **Retries**: Login and job applications retry on transient failures (see `utils.py`).
- **Logging**: All actions and errors are logged to `logs/naukri_auto_apply.log`.

## Maintenance Tips
- **Monitor Logs**: Regularly check `logs/naukri_auto_apply.log` for errors.
- **Update Dependencies**: Run `./scripts/setup.sh` after updating `requirements.txt`.
- **Compliance**: Verify automation complies with Naukri.com’s terms to avoid account suspension.
