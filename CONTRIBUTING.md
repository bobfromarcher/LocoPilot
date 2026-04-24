# Contributing to LocoPilot

Thank you for your interest in contributing! LocoPilot is a single-file project by design — `server.py` is the entire codebase. This makes contribution straightforward.

## Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes in `server.py` (or add supporting files if needed)
4. Test your changes: `python server.py` → verify at http://127.0.0.1:8264/docs
5. Submit a pull request

## Code Style

- **Single file philosophy.** New endpoints go in `server.py`. If you need helpers, put them above the `# ── FastAPI App ──` section.
- **Follow existing patterns.** Look at how current endpoints are structured:
  - Action function (e.g., `act_analyze`)
  - Pydantic request model (e.g., `ImageReq`)
  - API route handler (e.g., `@app.post("/vision/analyze")`)
- **Type hints everywhere.** All function signatures should have full type annotations.
- **Error handling.** Wrap endpoint handlers in try/except and return `{"error": str(e)}`.
- **No external state.** Endpoints should be stateless where possible. The browser state (`_bw`) is the one exception.

## Adding a New Endpoint

1. Write the action function in the appropriate section (Vision / Browser / Desktop / System)
2. Add a Pydantic request model in the `# ── Request Models ──` section
3. Add the route handler in the corresponding API section
4. Update the `/tools` endpoint to list your new endpoint
5. Update the README with your endpoint in the capabilities table
6. Add a use case example if the endpoint enables a new workflow

## Reporting Bugs

Use the [Bug Report](https://github.com/bobfromarcher/LocoPilot/issues/new?template=bug_report.yml) template. Include:
- Which endpoint
- Request payload
- Response received
- Vision model used
- OS

## Suggesting Features

Use the [Feature Request](https://github.com/bobfromarcher/LocoPilot/issues/new?template=feature_request.yml) template. Focus on the use case, not just the implementation.

## Good First Issues

Look for issues labeled [`good first issue`](https://github.com/bobfromarcher/LocoPilot/labels/good%20first%20issue). These are scoped for newcomers and include guidance.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
