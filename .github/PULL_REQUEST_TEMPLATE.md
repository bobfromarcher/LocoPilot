## Description

<!-- What does this PR add or change? -->

## Endpoint Changes

- [ ] New endpoint(s) added
- [ ] Existing endpoint(s) modified
- [ ] No endpoint changes

<!-- If new endpoints: list the path, method, and what it does -->

## Checklist

- [ ] Changes are in `server.py` (or justified in a separate file)
- [ ] Pydantic request model added for new endpoints
- [ ] `/tools` endpoint updated to list new endpoints
- [ ] README updated (capabilities table + use cases if applicable)
- [ ] Tested manually: `python server.py` → verified at http://127.0.0.1:8264/docs
- [ ] Error handling: endpoint returns `{"error": ...}` on failure

## Vision Model Tested

<!-- Which Ollama vision model did you test with? -->

## Screenshots (if applicable)

<!-- For UI/visual changes, add before/after screenshots -->
