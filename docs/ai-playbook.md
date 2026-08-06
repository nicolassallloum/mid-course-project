# Personal AI Playbook

## When I reach for AI first

I use AI first for bounded tasks where the source of truth is already available: drafting a CI workflow from known commands, reviewing a Dockerfile, proposing edge cases for existing tests, comparing documentation with code, and summarizing a small diff. I give it the relevant files and the exact scope instead of asking it to redesign the application.

## When I do not reach for AI first

I do not use AI first to choose the architecture, replace a working course project, handle secrets or private data, or make a change I am still trying to learn. I also slow down when the repository context is incomplete, because a polished answer can still target the wrong application.

## My non-negotiables

- Never paste credentials, tokens, `.env` values, production logs, or real customer data.
- Never accept an architecture or feature that violates the project brief.
- Never hide failures with CI shortcuts or unsupported evidence claims.
- Never submit a line, command, or configuration that I cannot explain.

## My review rules

I read the existing docs and source first, inspect every diff, and run the real command named in the documentation. I grade AI findings as Useful, Noise, or Wrong and write the reason. For release work, I verify pytest, the API startup command, `/health`, the frontend flow, and Docker when Docker is available. I reject generated tests that only assert hard-coded sample values instead of calling the application.

## What I am still figuring out

I am still refining how much repository context to provide for efficient reviews and how teams should store lightweight AI-review evidence without creating unnecessary documentation overhead.

## Decision Card

- New feature: confirm it is in scope before asking AI for implementation help.
- Code review: perform a manual read, then use AI as a second reviewer.
- Debugging: provide the smallest reproducible error without secrets.
- Infrastructure: verify commands locally and reject failure-hiding shortcuts.
- Never paste: secrets, private data, or production-only context.
- One rule: the repository and running application are the source of truth, not the generated explanation.
