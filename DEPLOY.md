Deploying to Render

1. Create a Git repository (if you haven't) and push your code to GitHub:
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-git-url>
   git push -u origin main

2. On Render dashboard, create a new Web Service and connect your GitHub repo.
   - Build command: pip install -r requirements.txt
   - Start command: gunicorn manage:app
   - Environment: Python
   - Set environment variables: SECRET_KEY, DATABASE_URL

3. (Optional) Use render.yaml to configure the service via Infrastructure as Code. See Render docs.

4. After deployment, open the live URL from Render dashboard. Monitor logs from Render's dashboard or via the CLI.

Notes
- This repository includes Procfile and runtime.txt. Ensure SECRET_KEY and DATABASE_URL are set in Render environment.
