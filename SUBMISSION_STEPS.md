# Final Project Submission Steps

1. Work from the `final-project` branch.
2. Run `python -m pytest tests/ -v` and confirm all tests pass.
3. Start the API with `python -m uvicorn app.main:app --reload --port 8000`.
4. Start the frontend with `python -m http.server 5500 --directory frontend` and confirm the Kanban board and create/edit flow.
5. Build and run the Docker image, then verify `GET /health` returns HTTP 200.
6. Push `main`, `mid-course-project`, and `final-project` to the same public GitHub repository.
7. Confirm the GitHub Actions workflow is green on `final-project`.
8. Replace the pending CI/Docker notes in `docs/release-evidence.md` with the real GitHub Actions link and local Docker result.
9. Submit only the public GitHub repository URL unless the LMS asks for something else.
