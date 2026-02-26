Project: Full-stack TODO Web App (Flask + SQLite + Jinja2)

Problem statement
- Build a simple, secure, full-stack TODO web app using Python Flask for the backend, SQLite for storage, and Jinja2 templates for frontend rendering (no JS frameworks). Include user authentication, full CRUD for todo items, tests, and deployment to Render.

Scope / Non-goals
- In-scope: project scaffolding, DB models, routes, templates, user auth (email + password), session management, input validation, unit and integration tests, Render deployment config.
- Out-of-scope: SPA frameworks, third-party complex OAuth providers (can be added later), advanced CI pipelines beyond basic test run.

High-level approach
- Keep the app minimal and idiomatic Flask with clear separation: app factory, blueprints (auth, todos, main), models, templates, static assets.
- Use SQLite via SQLAlchemy (ORM) for clear models and migrations (Flask-Migrate optional). Use Werkzeug security helpers for password hashing.

Phases (milestones)
1) Setup (project scaffolding)
   - Create virtualenv, requirements.txt, basic Flask app factory, config for dev/test/prod, .gitignore, README.
   - Files: app/__init__.py, config.py, run.py, requirements.txt
2) Models / DB
   - Add SQLAlchemy models: User, Todo (id, title, description, completed, due_date, created_at, owner_id)
   - Create DB initialization scripts and sample seed data for development.
   - Files: app/models.py, migrations/ (optional)
3) Routes / Templates (CRUD)
   - Blueprints: todos (list, create, read, update, delete), main (home/dashboard).
   - Jinja2 templates for list, form, detail, layout, auth pages.
   - Files: app/todos/routes.py, app/templates/*.html
4) Auth
   - Implement registration, login, logout, login_required decorator, session-based auth, user password hashing.
   - Protect todo routes so items are per-user.
   - Files: app/auth/routes.py, app/auth/forms.py (or simple WTForms), templates/auth/*.html
5) Tests
   - Add unit tests for models, authentication flows, and functional tests for CRUD routes using Flask test client.
   - Files: tests/test_auth.py, tests/test_todos.py, pytest.ini
6) Deploy to Render
   - Add Procfile (gunicorn), requirements.txt, runtime config, and Render-specific docs; ensure environment variables for SECRET_KEY and DATABASE_URL.
   - Files: Procfile, render.yaml (optional), README deploy section.

Deliverables
- app/ (blueprints, models, templates, static)
- tests/ with CI-friendly test suite
- docs/README with setup and Render deployment steps
- ROADMAP.md saved in session folder (high-level plan)

Key design decisions
- Use Flask app factory + blueprints for modularity.
- Use SQLAlchemy for models (easier to extend) with SQLite for dev and simple deployment.
- Session-based auth with Werkzeug password hashing; keep registration simple.
- Minimal JS (vanilla for small UX bits if necessary), no frontend framework.

Notes / Risks
- SQLite works on Render for small apps; for scale, recommend Postgres in future.
- If Flask-Migrate is added, include alembic migrations; otherwise use simple db.create_all() for MVP.

Progress
- Completed: setup-project, models-db, routes-templates (scaffolding, models, templates, CRUD, pagination, delete/edit implemented without AJAX).
- In progress: tests (pytest test_app.py added; running/iterating), forms and auth implementation next.
- Pending: auth (register/login/logout, protect routes), deploy-render (Procfile and env example added; finalize Render config).

Next actions (to track as todos)
- auth: implement registration/login/logout, WTForms, protect routes (in_progress)
- tests: finalize and run pytest, fix any failures (in_progress)
- deploy-render: finalize render.yaml, set env vars, document deploy steps (pending)

Notes
- Mobile responsiveness: Bootstrap is included; templates use responsive classes. Further polish planned in the auth/forms iteration.
- Secrets: .env.example added; update SECRET_KEY and DATABASE_URL in production.
