# Good First Issues — Content for GitHub Issues

Create these issues on the LocoPilot repo with the `good first issue` label to onboard new contributors.

---

## Issue 1

**Title:** [good first issue] Add `/browser/select_option` to the `/tools` endpoint response
**Labels:** good first issue, enhancement
**Body:**
The `/browser/select_option` endpoint exists and works, but it's missing from the list returned by `GET /tools`. 

**Where to look:** `server.py`, line ~580, the `browser` array in the `list_tools()` function.

**Fix:** Add an entry following the existing pattern:
```python
{"name": "select_option", "path": "/browser/select_option", "method": "POST", "desc": "Select a dropdown option by value"},
```

**Testing:** Start the server, call `GET http://127.0.0.1:8264/tools`, verify `select_option` appears in the browser list.

---

## Issue 2

**Title:** [good first issue] Add `/browser/cookies` method as POST in `/tools` listing
**Labels:** good first issue, bug
**Body:**
In the `/tools` endpoint, `/browser/cookies` is listed with `"method": "GET"`, but the actual route handler is `@app.post("/browser/cookies")`. The tools listing should show `"method": "POST"`.

**Where to look:** `server.py`, the `list_tools()` function, browser array.

**Fix:** Change `"method": "GET"` to `"method": "POST"` for the cookies entry.

**Testing:** `GET /tools` → verify cookies shows POST.

---

## Issue 3

**Title:** [good first issue] Add error handling to `/desktop/mouse_position` endpoint
**Labels:** good first issue, enhancement
**Body:**
The `/desktop/mouse_position` endpoint doesn't have try/except error handling, unlike most other endpoints. If `pyautogui` fails (e.g., no display), it'll throw an unhandled exception.

**Fix:** Wrap in try/except like other desktop endpoints:
```python
@app.get("/desktop/mouse_position")
def api_mouse():
    try:
        import pyautogui
        x, y = pyautogui.position()
        w, h = pyautogui.size()
        return {"x": x, "y": y, "screen": [w, h]}
    except Exception as e:
        return {"error": str(e)}
```

**Testing:** Verify it still works on a normal setup and returns `{"error": ...}` if pyautogui is unavailable.

---

## Issue 4

**Title:** [good first issue] Add a `/vision/extract_fields` endpoint for structured form data extraction
**Labels:** good first issue, enhancement
**Body:**
Add a new endpoint that extracts structured field/value pairs from form images (like insurance certificates, invoices, etc.).

**Proposed behavior:**
- Input: `image_path`, optional `fields` list (e.g., `["policy_number", "effective_date", "limits"]`)
- Output: `{field_name: extracted_value}` mapping

**Implementation approach:**
1. Create a Pydantic model `ExtractFieldsReq` with `image_path: str`, `fields: list[str] | None`
2. Create an action function that calls `ollama_chat` with a prompt like "Extract these fields from the document image: {fields}. Return as JSON."
3. Parse the LLM response as JSON
4. Add the route handler and update `/tools`

**Tips:**
- Look at how `/vision/ocr` is implemented — this is similar but with a more specific prompt
- Use `ollama_chat` instead of `ollama_generate` for better instruction-following
- The `/tools` endpoint and README need updating too

---

## Issue 5

**Title:** [good first issue] Update pyproject.toml version to match server.py (1.1.0)
**Labels:** good first issue, chore
**Body:**
`server.py` declares version `1.1.0` in the FastAPI app init, but `pyproject.toml` still has `version = "1.0.0"`. These should match.

**Fix:** In `pyproject.toml`, change:
```toml
version = "1.0.0"
```
to:
```toml
version = "1.1.0"
```

---

## Issue 6

**Title:** [good first issue] Add setup.py / pip-installable package support
**Labels:** good first issue, enhancement
**Body:**
`pyproject.toml` exists but there's no `setup.py` and the package isn't installable via pip yet. Users currently just run `python server.py` directly.

**Goal:** Make LocoPilot installable with `pip install .` or eventually `pip install locopilot`.

**Steps:**
1. Ensure `pyproject.toml` has correct metadata (author, URLs, classifiers)
2. Add a `__init__.py` or restructure minimally so `pip install .` works
3. Verify the `agent-capabilities` console script entry point in `[project.scripts]` works
4. Test: `pip install -e .` then run `agent-capabilities` or `python -m locopilot`

**Note:** The single-file philosophy is important. Don't restructure into a deep package hierarchy. A minimal change that keeps `server.py` as the core is preferred.
