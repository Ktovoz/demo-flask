# Repository Guidelines

## Project Structure & Module Organization
- `app/` hosts the application factory plus blueprints in `controllers/`, forms in `forms/`, SQLAlchemy models in `models/`, helpers in `utils/`, and UI templates in `templates/`.
- `templates/errors/` supplies shared error views; keep page shells in `templates/` and extend `base.html`.
- Local state lives in `instance/app.db` (ignore in commits) and migrations sit in `migrations/` for Flask-Migrate.
- Delivery assets reside in `.github/workflows/docker-image.yml` and `Dockerfile`.

## Build, Test, and Development Commands
- Create a virtualenv with `python -m venv .venv`, activate via `.venv\Scripts\activate` (PowerShell) or `source .venv/bin/activate`, then `pip install -r requirements.txt`.
- Run the app with `flask --app run.py --debug run`; it wires `create_app('development')`.
- Manage schema with `flask --app run.py db migrate` and `flask --app run.py db upgrade`.
- Seed defaults through `flask --app run.py init-db`.
- Container checks mirror CI: `docker build -t demo-flask .` then `docker run -p 5000:5000 demo-flask`.

## Coding Style & Naming Conventions
- Follow PEP 8, four-space indents, and snake_case module filenames (e.g., `controllers/auth.py`).
- Keep SQLAlchemy models CamelCase with lowercase table names, matching `app/models`.
- Register routes in existing blueprints so prefixes (`/auth`, `/users`, `/groups`) remain aligned.

## Testing Guidelines
- Add automated coverage with `pytest`; place specs in `tests/` mirroring the blueprint layout.
- Run `pytest -q` with `FLASK_ENV=testing` (or `set FLASK_ENV=testing`) to leverage the in-memory DB and disabled CSRF from `TestingConfig`.
- Prefer fixtures or factories over `init-db` so cases stay isolated, and cover each new endpoint or form rule.

## Commit & Pull Request Guidelines
- Follow the Conventional Commits pattern seen in history (`feat(app): ...`, `docs(README): ...`); keep subjects under 72 characters.
- PRs need a clear summary, testing evidence, and linked issues or screenshots for UI touches.
- Exclude generated artifacts such as `instance/app.db` and IDE configs; update docs when behavior shifts.

## Environment & Configuration
- Provide secrets via environment variables consumed in `config.py` (`SECRET_KEY`, `DATABASE_URL`); never hard-code credentials.
- Set `FLASK_CONFIG=production` (or `FLASK_ENV=development`) explicitly in deployment scripts instead of editing source.
- Adjust CORS, session, or security defaults within the `Config` subclasses to keep `app/__init__.py` focused on wiring.
