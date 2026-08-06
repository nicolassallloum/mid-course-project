# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes.
- Docs-first/read-first guardrail included: yes.
- Unexpected `app/` and `frontend/` edits rule included: yes.
- Explicit protection against a React/Vite or Node rewrite included: yes.

## AI code review mini-log

Reviewed change set: the final-project release files, especially `Dockerfile`, `.github/workflows/ci.yml`, `README.md`, and the evidence documents.

| AI comment | Grade | Reason | Verification or decision |
|---|---|---|---|
| Reuse the separate React/Vite application and document `npm run dev` on port 3000 | Wrong | The course requires the same mid-course repository; the actual application is FastAPI plus vanilla JavaScript | Rejected the generated application and kept `app/`, `frontend/`, and the 31-test suite from the real mid-course project |
| Keep `pip install -r requirements.txt || pip install ...` as a CI fallback | Wrong | The fallback can hide a broken or incomplete dependency file and is one of the dangerous shortcuts the brief warns against | Removed the fallback; CI now fails honestly when declared dependencies cannot install |
| Add a non-root runtime user to the Docker image | Useful | It improves container safety without changing product behavior | Added `appuser`, copied files with the correct ownership, and set `USER appuser` |

## AI security mini-review

| Finding | File evidence | Grade | Reason | Next action |
|---|---|---|---|---|
| Task titles and descriptions are inserted with `textContent`, not raw HTML | `frontend/index.html` | Valid | This avoids interpreting task-controlled strings as HTML and reduces DOM-XSS risk | Keep `textContent`; do not introduce `innerHTML` for task fields |
| CORS is limited to the local course frontend origins and credentials are disabled | `app/main.py` | Valid | The configuration is narrower than a wildcard and matches the local-only workflow | Keep the allowlist aligned with documented local ports |
| The API has no authentication | `app/main.py` | Noise | Authentication is intentionally outside the course scope and adding it would violate the no-new-features rule | Record the scope limitation; do not add authentication for this submission |
| The in-memory store is not production persistence | `app/storage.py` | Noise | The brief explicitly protects the existing application rather than asking for a production database | Keep in-memory storage and describe it accurately |

## Manual security check

I searched the repository for common secret terms and reviewed `.gitignore`, `.dockerignore`, the CI workflow, and the Dockerfile. I found no committed `.env` file, API token, password, production log, or customer data. I also manually confirmed that CI contains no `continue-on-error`, `|| true`, or skipped test command.

## One AI output I rejected or corrected

The second uploaded repository treated a newly generated React/Vite Evidence Hub as the final Task Tracker and documented `npm install`, `npm run dev`, and port 3000. I rejected that output because it replaced the actual FastAPI/vanilla-JavaScript project instead of extending it. I used only the useful release-document ideas, rewrote them against the real source tree, and corrected the Docker and CI commands.

## Three AI usage rules

1. Never paste: credentials, `.env` values, real personal/customer data, private production logs, or access tokens.
2. Always verify: inspect the diff, run the full pytest suite, start the real API, check `/health`, and test the frontend flow before accepting a change.
3. Record AI contributions by: naming the affected file, grading each suggestion as Useful, Noise, or Wrong, and documenting rejected or corrected output.

## Ownership statement

I am comfortable submitting this repository as my own work because the application is the actual mid-course FastAPI Task Tracker rather than a replacement project. I reviewed the merged files, preserved the existing product scope, and verified the application and all 31 tests. I can explain the CI workflow, Docker command, repository guardrails, and every evidence statement. Where this preparation environment could not run Docker or a hosted GitHub Action, I recorded the limitation instead of inventing a result.
