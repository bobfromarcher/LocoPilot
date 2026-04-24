# LocoPilot Examples

Self-contained Python scripts that demonstrate real use cases for the LocoPilot API
running at `http://127.0.0.1:8264`.

## Prerequisites

- Python 3.8+
- `requests` library (`pip install requests`)
- LocoPilot server running locally

## Scripts

| Script | Category | Description |
|---|---|---|
| `research_agent.py` | Browser | Browses Hacker News and prints the top 5 story titles using `/browser/browse_and_read`. |
| `form_filler.py` | Browser | Fills and submits a web form from a JSON data object using `/browser/browse`, `/browser/type`, and `/browser/click`. |
| `screen_monitor.py` | Desktop | Periodically captures and describes the screen via `/desktop/see`, alerting when the description changes. |
| `coi_scanner.py` | Vision | OCRs a Certificate of Insurance image with `/vision/ocr`, then extracts policy number, dates, and carrier via regex. |
| `desktop_automation.py` | Desktop | Opens an app from the Start menu, verifies the screen, and performs a click-type-save sequence using `/desktop/hotkey`, `/desktop/see`, and `/desktop/find_and_click`. |

## Running

```bash
python examples/research_agent.py
python examples/form_filler.py
python examples/screen_monitor.py
python examples/coi_scanner.py          # update COI_IMAGE path first
python examples/desktop_automation.py   # update APP_NAME if needed
```

Adjust constants at the top of each script (URLs, image paths, app names) to suit your environment.
