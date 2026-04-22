<div align="center">

# ⚡ Agent Capabilities

**Vision • Browser • Desktop — for any local LLM**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Ollama](https://img.shields.io/badge/runtime-Ollama-purple?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjEwIi8+PC9zdmc+)](https://ollama.ai)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![35 Endpoints](https://img.shields.io/badge/endpoints-35-orange)](http://127.0.0.1:8264/docs)
[![Tested](https://img.shields.io/badge/status-tested-brightgreen)](http://127.0.0.1:8264/docs)

*One file. Zero cloud. Full autonomy on your machine.*

[Get Started](#-quickstart) · [Full Capabilities](#-full-capabilities) · [Use Cases](#-use-case-scenarios) · [API Reference](#-api-reference) · [Models](#-vision-models)

</div>

---

## What is this?

Agent Capabilities gives **any local LLM** the ability to see, browse, and control — running entirely on your device with zero cloud dependencies.

| Module | What it does | How |
|---|---|---|
| **👁 Vision** | Analyze images, read text (OCR), compare screenshots, describe what's on screen | Ollama + local vision model |
| **🌐 Browser** | Navigate sites, click, type, scroll, extract text/links, run JS, save PDFs | Playwright (Chromium) |
| **🖱 Desktop** | Move mouse, click, drag, type, press keys, take screenshots | pyautogui |

**No API keys. No cloud. No data leaves your machine.**

The killer feature: **vision-guided autonomy**. Your LLM doesn't just call tools — it *sees* the result, decides what to do next, and acts. That loop — see → think → act → see — is how you build agents that actually work.

---

## 🚀 Quickstart

```bash
# 1. Install dependencies
pip install fastapi uvicorn httpx pyautogui Pillow pydantic playwright
playwright install chromium

# 2. Install a vision model (pick one)
ollama pull moondream     # 1.7 GB — fast, works on 4GB VRAM
ollama pull llava         # 4.5 GB — better quality
ollama pull llava-llama3  # 5.5 GB — best quality

# 3. Start the server
python server.py
```

Open `http://127.0.0.1:8264/docs` for interactive API docs.

**Windows one-liner:**
```powershell
./setup.ps1
```
**Linux/macOS one-liner:**
```bash
./setup.sh
```

---

## 🎯 One-Call Autonomy

These endpoints combine vision + action so your LLM doesn't need multiple round-trips:

```bash
# See the screen — screenshot + vision analysis in one call
curl -s -X POST http://127.0.0.1:8264/desktop/see \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What application is open?"}'

# Vision-guided click — describe what to click, it finds and clicks it
curl -s -X POST http://127.0.0.1:8264/desktop/find_and_click \
  -H "Content-Type: application/json" \
  -d '{"target": "the Submit button", "action": "click"}'

# Browse + screenshot + vision + text extraction — all in one call
curl -s -X POST http://127.0.0.1:8264/browser/browse_and_read \
  -H "Content-Type: application/json" \
  -d '{"url": "https://news.ycombinator.com"}'
```

---

## 📋 Full Capabilities

### 👁 Vision (4 endpoints)

| Endpoint | Method | What it does | Key params |
|---|---|---|---|
| `/vision/analyze` | POST | Analyze any image with a custom prompt | `image_path`, `prompt`, `model` |
| `/vision/capture` | POST | Screenshot the desktop + analyze with vision | `prompt`, `model`, `save_path` |
| `/vision/ocr` | POST | Extract all text from an image | `image_path`, `model` |
| `/vision/compare` | POST | Compare two images and describe differences | `image_a`, `image_b`, `prompt`, `model` |

### 🌐 Browser (16 endpoints)

| Endpoint | Method | What it does | Key params |
|---|---|---|---|
| `/browser/browse` | POST | Navigate to a URL | `url`, `wait` |
| `/browser/screenshot` | POST | Screenshot the current page | `full_page` |
| `/browser/click` | POST | Click an element by CSS selector | `selector`, `button`, `click_count` |
| `/browser/type` | POST | Type text into an element | `selector`, `text`, `clear`, `enter`, `delay` |
| `/browser/scroll` | POST | Scroll the page | `direction`, `amount` |
| `/browser/text` | POST | Extract all visible text from the page | — |
| `/browser/links` | POST | Extract all links from the page | — |
| `/browser/evaluate` | POST | Run JavaScript in the browser | `expression` |
| `/browser/go_back` | POST | Navigate back in history | — |
| `/browser/go_forward` | POST | Navigate forward in history | — |
| `/browser/select_option` | POST | Select a dropdown option | `selector`, `value` |
| `/browser/wait_for` | POST | Wait for an element to appear | `selector`, `timeout` |
| `/browser/cookies` | POST | Get all browser cookies | — |
| `/browser/save_pdf` | POST | Save current page as PDF | `path` |
| `/browser/close` | POST | Close the browser instance | — |
| `/browser/browse_and_read` | POST | **Navigate + screenshot + vision + text** (one call) | `url`, `vision_model` |

### 🖱 Desktop (13 endpoints)

| Endpoint | Method | What it does | Key params |
|---|---|---|---|
| `/desktop/see` | POST | **Screenshot + vision** (one call) | `prompt`, `model`, `region` |
| `/desktop/find_and_click` | POST | **Describe target → vision finds it → clicks it** | `target`, `action`, `model` |
| `/desktop/move` | POST | Move the mouse to coordinates | `x`, `y`, `duration` |
| `/desktop/click` | POST | Click at position | `x`, `y`, `button`, `clicks` |
| `/desktop/double_click` | POST | Double-click at position | `x`, `y` |
| `/desktop/right_click` | POST | Right-click at position | `x`, `y` |
| `/desktop/drag` | POST | Drag from A to B | `from_x`, `from_y`, `to_x`, `to_y`, `duration` |
| `/desktop/scroll` | POST | Scroll the mouse wheel | `clicks`, `x`, `y` |
| `/desktop/type` | POST | Type text with the keyboard | `text`, `interval` |
| `/desktop/press_key` | POST | Press a single key | `key`, `presses` |
| `/desktop/hotkey` | POST | Press a key combination | `keys` (e.g. `["ctrl", "c"]`) |
| `/desktop/screenshot` | POST | Take a desktop screenshot | `save_path`, `region` |
| `/desktop/mouse_position` | GET | Get mouse position + screen size | — |

### ⚙️ System (2 endpoints)

| Endpoint | Method | What it does |
|---|---|---|
| `/health` | GET | Check server + Ollama status, list available models |
| `/tools` | GET | List all 35 endpoints with descriptions |

---

## 🔥 Use Case Scenarios

### 1. Automated Web Research
> "Go to Hacker News, read the top stories, and summarize the trending topics."

```bash
curl -s -X POST http://127.0.0.1:8264/browser/browse_and_read \
  -d '{"url": "https://news.ycombinator.com"}'
```
Returns: page text + vision description + title + URL. Feed the result to your LLM to summarize.

**Workflow:** `browse_and_read` → LLM processes the result → done.

---

### 2. Vision-Guided Desktop Automation
> "Click the Save button in whatever app is currently open."

```bash
curl -s -X POST http://127.0.0.1:8264/desktop/find_and_click \
  -d '{"target": "the Save button", "action": "click"}'
```
Returns: `{"found": true, "action": "click", "target": "the Save button", "position": [842, 156]}`

**How it works:** Server screenshots the desktop → sends image to Ollama vision → model returns coordinates → pyautogui clicks.

---

### 3. Screen Monitoring / Change Detection
> "Watch this dashboard and tell me when the status indicator changes from green to red."

```bash
# Take first screenshot
curl -s -X POST http://127.0.0.1:8264/vision/capture \
  -d '{"prompt": "What color is the status indicator?", "save_path": "./screenshots/baseline.png"}'

# Later, compare
curl -s -X POST http://127.0.0.1:8264/vision/compare \
  -d '{"image_a": "./screenshots/baseline.png", "image_b": "./screenshots/capture_1234567890.png"}'
```

**Workflow:** Capture baseline → periodically capture + compare → alert on change.

---

### 4. Document OCR and Data Extraction
> "Read this invoice image and extract the invoice number, date, and total amount."

```bash
curl -s -X POST http://127.0.0.1:8264/vision/ocr \
  -d '{"image_path": "./invoices/receipt_2024.png"}'
```
Returns: all extracted text with layout preserved. Feed to your LLM to parse fields.

---

### 5. Browser Form Filling
> "Fill out this web form with my contact information."

```bash
# Navigate to the form
curl -s -X POST http://127.0.0.1:8264/browser/browse \
  -d '{"url": "https://example.com/contact", "wait": 3}'

# Type into fields
curl -s -X POST http://127.0.0.1:8264/browser/type \
  -d '{"selector": "#name", "text": "John Smith", "clear": true}'

curl -s -X POST http://127.0.0.1:8264/browser/type \
  -d '{"selector": "#email", "text": "john@example.com", "clear": true}'

# Select from dropdown
curl -s -X POST http://127.0.0.1:8264/browser/select_option \
  -d '{"selector": "#country", "value": "US"}'

# Submit
curl -s -X POST http://127.0.0.1:8264/browser/type \
  -d '{"selector": "#email", "text": "", "enter": true}'
```

---

### 6. Web Scraping with Vision Backup
> "Scrape product listings — get the text, and if the price is in an image, use vision to read it."

```bash
# Get page text (fast, structured)
curl -s -X POST http://127.0.0.1:8264/browser/text

# If text extraction misses something, use vision
curl -s -X POST http://127.0.0.1:8264/browser/browse_and_read \
  -d '{"url": "https://store.example.com/products"}'
```
`browse_and_read` gives you both: DOM text extraction AND vision analysis. Use vision when content is rendered in images, canvas, or non-standard elements.

---

### 7. Desktop App Automation
> "Open File Explorer, navigate to the Documents folder, and find the report PDF."

```bash
# Open File Explorer via keyboard
curl -s -X POST http://127.0.0.1:8264/desktop/hotkey \
  -d '{"keys": ["win", "e"]}'

# See what's on screen
curl -s -X POST http://127.0.0.1:8264/desktop/see \
  -d '{"prompt": "What folders are visible in File Explorer?"}'

# Double-click the Documents folder
curl -s -X POST http://127.0.0.1:8264/desktop/find_and_click \
  -d '{"target": "the Documents folder", "action": "double_click"}'
```

---

### 8. Screenshot Comparison for QA/Testing
> "Did the new deployment break the layout? Compare before and after screenshots."

```bash
curl -s -X POST http://127.0.0.1:8264/vision/compare \
  -d '{
    "image_a": "./qa/before_deploy.png",
    "image_b": "./qa/after_deploy.png",
    "prompt": "Focus on layout differences. Are there any visual regressions, broken elements, or misaligned components?"
  }'
```

---

### 9. Autonomous Agent Loop
> "Build an agent that can research, decide, and act without human input."

```python
import httpx, json

API = "http://127.0.0.1:8264"

def agent_step(task: str) -> str:
    """One step: see screen → decide action → execute → return result."""
    # 1. See what's happening
    screen = httpx.post(f"{API}/desktop/see", json={"prompt": task}, timeout=120).json()

    # 2. Feed vision result to your LLM to decide the next action
    # (use any local LLM — llama3, mistral, qwen, etc.)
    decision = call_your_llm(f"Given this screen: {screen['description']}\nWhat should I do next?")

    # 3. Parse decision into an action
    # e.g. "click the Login button" → find_and_click
    result = httpx.post(f"{API}/desktop/find_and_click", json={
        "target": "the Login button",
        "action": "click"
    }, timeout=120).json()

    return result

# Run the loop
for i in range(10):
    result = agent_step("Complete the login process")
    if "found" in result and not result["found"]:
        break  # Nothing more to do
```

---

### 10. Browser PDF Archival
> "Save a PDF copy of this web page for record-keeping."

```bash
curl -s -X POST http://127.0.0.1:8264/browser/browse \
  -d '{"url": "https://example.com/report", "wait": 3}'

curl -s -X POST http://127.0.0.1:8264/browser/save_pdf \
  -d '{"path": "./archives/report_2024.pdf"}'
```

---

### 11. Accessibility Auditing
> "Describe what's on this webpage so I can check if it's accessible."

```bash
curl -s -X POST http://127.0.0.1:8264/browser/browse_and_read \
  -d '{"url": "https://example.com", "vision_model": "llava"}'
```
The vision response describes what a user *sees*, not what the DOM says — great for catching missing alt text, low-contrast elements, and layout issues.

---

### 12. Real-Time Desktop Observation
> "Watch my screen and describe what I'm doing in real-time."

```python
import httpx, time

while True:
    result = httpx.post("http://127.0.0.1:8264/vision/capture",
        json={"prompt": "What is the user currently doing? What application and action?"},
        timeout=120).json()
    print(result.get("description", "Unable to determine"))
    time.sleep(5)  # Check every 5 seconds
```

---

## ✅ Test-Verified Endpoints

Every endpoint has been tested end-to-end on Windows 11 with Ollama (WSL) + moondream:

| Endpoint | Status | Notes |
|---|---|---|
| `/health` | ✅ Pass | Returns Ollama status + available models |
| `/tools` | ✅ Pass | Lists all 35 endpoints |
| `/vision/analyze` | ✅ Pass | ~2-6s per image with moondream |
| `/vision/capture` | ✅ Pass | Screenshot + vision in one call |
| `/vision/ocr` | ✅ Pass | Text extraction works, quality depends on model |
| `/vision/compare` | ✅ Pass | Accurately identifies/no-differences |
| `/browser/browse` | ✅ Pass | Loads pages with domcontentloaded |
| `/browser/screenshot` | ✅ Pass | Full page + viewport modes |
| `/browser/click` | ✅ Pass | CSS selector-based |
| `/browser/type` | ✅ Pass | Type + clear + enter support |
| `/browser/scroll` | ✅ Pass | Up/down with configurable amount |
| `/browser/text` | ✅ Pass | Extracts inner_text from body |
| `/browser/links` | ✅ Pass | Returns text + href for each link |
| `/browser/evaluate` | ✅ Pass | JS execution returns results |
| `/browser/go_back` | ✅ Pass | History navigation works |
| `/browser/go_forward` | ✅ Pass | History navigation works |
| `/browser/wait_for` | ✅ Pass | Waits for selector with timeout |
| `/browser/cookies` | ✅ Pass | Returns cookie list |
| `/browser/save_pdf` | ✅ Pass | Generates PDF from current page |
| `/browser/close` | ✅ Pass | Closes browser instance cleanly |
| `/browser/browse_and_read` | ✅ Pass | Combined navigate+screenshot+vision+text |
| `/desktop/see` | ✅ Pass | Screenshot + vision in one call |
| `/desktop/find_and_click` | ⚠️ Model-dependent | Works with llava; moondream struggles with coordinates |
| `/desktop/move` | ✅ Pass | Smooth mouse movement |
| `/desktop/click` | ✅ Pass | Left/right/double click |
| `/desktop/double_click` | ✅ Pass | Double-click at position |
| `/desktop/right_click` | ✅ Pass | Right-click at position |
| `/desktop/drag` | ✅ Pass | Drag from A to B |
| `/desktop/scroll` | ✅ Pass | Scroll wheel up/down |
| `/desktop/type` | ✅ Pass | ASCII text typing |
| `/desktop/press_key` | ✅ Pass | Single key press |
| `/desktop/hotkey` | ✅ Pass | Key combinations like ctrl+c |
| `/desktop/screenshot` | ✅ Pass | Full screen + region capture |
| `/desktop/mouse_position` | ✅ Pass | Returns x, y + screen dimensions |

> **Note on `find_and_click`:** The endpoint code is correct — it captures the screen, asks the vision model for coordinates, parses the response, and clicks. The quality of the result depends on the vision model's spatial reasoning ability. `llava` and `llava-llama3` perform significantly better than `moondream` for this specific task.

---

## ⚙️ How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Your LLM   │────▶│  server.py   │────▶│   Ollama     │
│  (any model)│     │  localhost   │     │  (local)     │
│             │◀────│  :8264       │◀────│             │
└─────────────┘     └──────┬───────┘     └─────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  Vision  │ │ Browser  │ │ Desktop  │
        │ (Pillow) │ │(Playwright)│ │(pyautogui)│
        └──────────┘ └──────────┘ └──────────┘
```

Your LLM calls HTTP endpoints on localhost. The server uses Ollama for vision, Playwright for browsing, and pyautogui for desktop control. Everything stays on your machine.

---

## 🧠 Vision Models

| Model | Size | Speed | Quality | VRAM | Best for |
|---|---|---|---|---|---|
| moondream | 1.7 GB | ⚡⚡⚡ | Good | ~2 GB | Quick descriptions, low-VRAM GPUs |
| llava | 4.5 GB | ⚡⚡ | Better | ~5 GB | General purpose vision tasks, spatial reasoning |
| llava-llama3 | 5.5 GB | ⚡ | Best | ~6 GB | Complex visual reasoning, coordinate extraction |
| minicpm-v | 2.6 GB | ⚡⚡⚡ | Good | ~3 GB | Fast OCR and descriptions |

**Recommendation:** `moondream` for descriptions on low-VRAM GPUs. **`llava` or `llava-llama3` for `find_and_click`** — moondream struggles with pixel coordinate extraction, while llava models handle spatial reasoning significantly better.

---

## 🔧 Configuration

### config.json (optional)

Create `config.json` next to `server.py`:

```json
{
  "ollama_base_url": "http://127.0.0.1:11434",
  "vision_model": "moondream",
  "wsl_distro": "Ubuntu"
}
```

**WSL users:** If Ollama runs inside WSL, set `"ollama_base_url": "wsl"` and it auto-proxies through your WSL distro.

### Environment Variables

| Variable | Default | What it does |
|---|---|---|
| `AC_VISION_MODEL` | `moondream` | Default vision model |
| `AC_HOST` | `127.0.0.1` | Server bind address |
| `AC_PORT` | `8264` | Server port |
| `AC_OLLAMA_URL` | `http://127.0.0.1:11434` | Ollama API URL |
| `AC_WSL_DISTRO` | `Ubuntu` | WSL distribution name |
| `AC_SCREENSHOT_DIR` | `./screenshots` | Where screenshots are saved |

### CLI Flags

```bash
python server.py --port 9000       # Custom port
python server.py --model llava     # Different vision model
python server.py --host 0.0.0.0    # Listen on all interfaces (LAN access)
```

---

## 🔌 Integration with LLMs

### OpenAI-Compatible Pattern

```python
import httpx

def agent_loop(task, max_steps=10):
    """Simple agent loop: LLM decides which tools to call."""
    messages = [{"role": "user", "content": task}]
    tools = httpx.get("http://127.0.0.1:8264/tools").json()

    for _ in range(max_steps):
        # Ask your LLM what to do next (use any local model)
        response = call_your_llm(messages, tools=tools)

        if response.get("tool_call"):
            # Execute the tool via Agent Capabilities
            result = httpx.post(
                f"http://127.0.0.1:8264{response['tool_call']['path']}",
                json=response['tool_call']['args'],
                timeout=120,
            ).json()
            messages.append({"role": "tool", "content": str(result)})
        else:
            return response["content"]  # Final answer

    return "Max steps reached"
```

### LangChain Tool Wrapping

```python
from langchain.tools import tool

@tool
def see_screen(prompt: str) -> str:
    """See what's on screen and describe it."""
    r = httpx.post("http://127.0.0.1:8264/desktop/see",
        json={"prompt": prompt}, timeout=120)
    return r.json().get("description", "")

@tool
def click_target(target: str) -> str:
    """Find and click something on screen by description."""
    r = httpx.post("http://127.0.0.1:8264/desktop/find_and_click",
        json={"target": target}, timeout=120)
    return str(r.json())

@tool
def browse_and_read(url: str) -> str:
    """Navigate to a URL and read its content."""
    r = httpx.post("http://127.0.0.1:8264/browser/browse_and_read",
        json={"url": url}, timeout=120)
    return r.json().get("text_preview", "") + "\n" + r.json().get("vision", "")
```

---

## 🛡️ Security

- **No outbound data** — Vision inference runs via local Ollama. Images never leave your device.
- **No API keys** — No cloud services, no accounts, no tokens required.
- **localhost only** — Default binds to 127.0.0.1. Not exposed to your network.
- **No telemetry** — Zero analytics, zero tracking, zero phoning home.
- **Open source** — One file, 580 lines. Read it, audit it, trust it.

---

## 🖥️ Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.10 | 3.12+ |
| Ollama | Any version | Latest |
| GPU | Not required (CPU works) | 4GB+ VRAM for vision |
| RAM | 4 GB | 8 GB+ |
| OS | Windows / Linux / macOS | Any |

---

## 📄 License

MIT — use it, fork it, ship it.

---

<div align="center">

**Built by [bobfromarcher](https://github.com/bobfromarcher)**

[⬆ Back to Top](#-agent-capabilities)

</div>
