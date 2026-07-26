# Submission Steps

The project files are complete. Perform these repository steps using your own GitHub account so the commits use your real identity.

```bash
cd mid-course-task-tracker
git init
git config user.name "Your Name"
git config user.email "your-email@example.com"
git checkout -b mid-course-project
git add .
git commit -m "Complete AI-assisted mid-course feature sprint"
```

Create a new **public** GitHub repository, then connect and push:

```bash
git remote add origin <YOUR-PUBLIC-REPOSITORY-URL>
git push -u origin mid-course-project
```

Before submitting the URL:

```bash
git branch --show-current
pytest tests/ -v
```

Confirm:

- Branch output is `mid-course-project`.
- Test result is `31 passed`.
- The frontend opens from `http://localhost:5500/index.html`.
- The repository contains `docs/midcourse/` and the required five Markdown files.
- The repository is public.
- No secrets, credentials, `.env` files, or private data were added.
