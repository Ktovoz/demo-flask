# Repository Guidelines

## Project Structure & Module Organization
- pp/ contains the application factory (__init__.py), blueprint packages under controllers/, form definitions in orms/, SQLAlchemy models in models/, utilities in utils/, and Jinja templates in 	emplates/.
- 	emplates/ root holds layout pages while 	emplates/errors/ provides the shared error views used by the registered handlers.
- instance/app.db stores the local SQLite database; delete or ignore it when shipping code.
- migrations/ carries the Alembic environment used by Flask-Migrate.
- CI and container assets live in .github/workflows/docker-image.yml and Dockerfile.

## Build, Test, and Development Commands
- python -m venv .venv && .venv\Scripts\activate (PowerShell) or source .venv/bin/activate (bash) to enter an isolated environment, then pip install -r requirements.txt.
- lask --app run.py --debug run starts the development server using the create_app('development') factory wired in 
un.py.
- lask --app run.py db migrate followed by lask --app run.py db upgrade manages schema changes via Flask-Migrate.
- lask --app run.py init-db invokes pp/commands.py to bootstrap default groups and an admin account.
- docker build -t demo-flask . and docker run -p 5000:5000 demo-flask mirror the GitHub Actions workflow for container validation.

## Coding Style & Naming Conventions
- Follow PEP 8 with four-space indentation; keep modules and blueprints snake_case (e.g., controllers/auth.py).
- SQLAlchemy models in pp/models use CamelCase classes with lowercase table names; reuse that pattern when adding entities.
- Route functions should live in the existing blueprint modules so URL prefixes (/auth, /users, /groups) stay consistent.
- Templates under pp/templates adopt lower_snake_case filenames; extend ase.html for shared chrome.

## Testing Guidelines
- Target pytest for new automated coverage; create a top-level 	ests/ package mirroring the blueprint layout.
- Use pytest -q with FLASK_ENV=testing (or set FLASK_ENV=testing) so the TestingConfig in config.py enables the in-memory SQLite database and disables CSRF.
- Stub default data via fixtures instead of depending on init-db; this keeps tests hermetic.
- Add regression cases for every new endpoint or form validation path.

## Commit & Pull Request Guidelines
- Match the existing Conventional Commits style observed in git log (eat(app): ..., docs(README): ...); scope names should reflect the touched module.
- Keep subject lines under 72 characters and add concise body bullets when the change needs context (lists prefixed with - are fine).
- Pull requests must include a summary, testing notes (command outputs or screenshots for UI flows), and linked issues when available.
- Avoid committing local artifacts such as instance/app.db or IDE files; ensure .gitignore stays effective.

## Environment & Configuration
- Manage secrets via environment variables consumed in config.py (SECRET_KEY, DATABASE_URL); never commit real credentials.
- Align environment selection with deployment: set FLASK_CONFIG=production inside containers, or rely on the default development profile locally.
- When configuring CORS or session settings, prefer modifications in Config subclasses rather than inline tweaks inside controllers.
