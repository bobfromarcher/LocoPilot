<div align="center">

# ⚡ Agent Capabilities

**Vision • Browser • Desktop — for any local LLM**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Ollama](https://img.shields.io/badge/runtime-Ollama-purple?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjEwIi8+PC9zdmc+)](https://ollama.ai)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

*One file. Zero cloud. Full autonomy on your machine.*

[Get Started](#-quickstart) · [API Reference](#-api-reference) · [How It Works](#-how-it-works) · [Models](#-vision-models)

</div>

---

## What is this?

Agent Capabilities gives **any local LLM** the ability to:

- **👁 See** — Analyze images, OCR text, compare screenshots, describe what's on screen
- **🌐 Browse** — Navigate websites, click, type, scroll, extract text and links — like a human
- **🖱 Control** — Move mouse, click, drag, type, press keys — full desktop automation

Everything runs **locally** on your device. No cloud APIs. No API keys. No data leaves your machine.

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

That's it. Open `http://127.0.0.1:8264/docs` for the interactive API docs.

## 🎯 One-Call Autonomy

The real power is combining vision + action in a single call:

```bash
# Describe what's on screen right now
curl -X POST http://127.0.0.1:8264/vision/capture \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What application is open and what is the user doing?"}'

# Vision-guided click: describe what to click, it finds and clicks it
curl -X POST http://127.0.0.1:8264/desktop/find_and_click \
  -H "Content-Type: application/json" \
  -d '{"target": "the Submit button", "action": "click"}'

# Browse a URL, screenshot it, read it with vision, extract text — all in one call
curl -X POST http://127.0.0.1:8264/browser/browse_and_read \
  -H "Content-Type: application/json" \
  -d '{"url": "https://news.ycombinator.com"}'
```

## 📡 API Reference

### Vision

| Endpoint | Method | What it does |
|---|---|---|
| `/vision/analyze` | POST | Analyze any image file |
| `/vision/capture` | POST | Screenshot + analyze in one call |
| `/vision/ocr` | POST | Extract text from image |
| `/vision/compare` | POST | Compare two images, describe differences |

### Browser (Playwright)

| Endpoint | Method | What it does |
|---|---|---|
| `/browser/browse` | POST | Navigate to URL |
| `/browser/screenshot` | POST | Screenshot current page |
| `/browser/click` | POST | Click element by CSS selector |
| `/browser/type` | POST | Type text into element |
| `/browser/scroll` | POST | Scroll page up/down |
| `/browser/text` | POST | Extract page text |
| `/browser/links` | POST | Extract all links |
| `/browser/browse_and_read` | POST | Navigate + screenshot + vision + text (one call) |

### Desktop (pyautogui)

| Endpoint | Method | What it does |
|---|---|---|
| `/desktop/see` | POST | Screenshot + vision (one call) |
| `/desktop/find_and_click` | POST | Describe target → vision finds it → clicks it |
| `/desktop/move` | POST | Move mouse to (x, y) |
| `/desktop/click` | POST | Click at position |
| `/desktop/double_click` | POST | Double-click |
| `/desktop/right_click` | POST | Right-click |
| `/desktop/drag` | POST | Drag from A to B |
| `/desktop/scroll` | POST | Scroll wheel |
| `/desktop/type` | POST | Type text |
| `/desktop/press_key` | POST | Press single key |
| `/desktop/hotkey` | POST | Press key combo (e.g. ctrl+c) |
| `/desktop/screenshot` | POST | Desktop screenshot |
| `/desktop/mouse_position` | GET | Get current mouse position + screen size |

### System

| Endpoint | Method | What it does |
|---|---|---|
| `/health` | GET | Check server + Ollama status |
| `/tools` | GET | List all available tools |

## ⚙️ How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Your LLM   │────▶│  server.py   │────▶│   Ollama    │
│  (any model)│     │  localhost   │     │  (local)    │
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

## 🧠 Vision Models

| Model | Size | Speed | Quality | VRAM |
|---|---|---|---|---|
| moondream | 1.7 GB | ⚡⚡⚡ Fast | Good | ~2 GB |
| llava | 4.5 GB | ⚡⚡ Medium | Better | ~5 GB |
| llava-llama3 | 5.5 GB | ⚡ Slower | Best | ~6 GB |
| minicpm-v | 2.6 GB | ⚡⚡⚡ Fast | Good | ~3 GB |

**Recommendation:** Start with `moondream` — it runs on 4GB VRAM cards and processes screenshots in ~6 seconds.

## 🔧 Configuration

Create `config.json` next to `server.py`:

```json
{
  "ollama_base_url": "http://127.0.0.1:11434",
  "vision_model": "moondream"
}
```

**WSL users:** If Ollama runs inside WSL, set `"ollama_base_url": "wsl"` and it auto-proxies.

### CLI Flags

```bash
python server.py --port 9000       # Custom port
python server.py --model llava     # Different vision model
python server.py --host 0.0.0.0    # Listen on all interfaces
```

## 🔌 Integration Examples

### With OpenAI-compatible LLMs

```python
import httpx

def agent_loop(task):
    """Simple agent loop: LLM decides which tools to call."""
    messages = [{"role": "user", "content": task}]
    
    while True:
        # Ask your LLM what to do next
        response = call_your_llm(messages)
        
        if "tool_call" in response:
            # Execute the tool via Agent Capabilities
            result = httpx.post(
                f"http://127.0.0.1:8264{response['tool_call']['path']}",
                json=response['tool_call']['args'],
            ).json()
            messages.append({"role": "tool", "content": str(result)})
        else:
            return response  # Done
```

### With curl / any HTTP client

```bash
# Take a screenshot and ask what's on screen
curl -s -X POST http://127.0.0.1:8264/vision/capture \
  -d '{"prompt": "List all visible buttons and their approximate positions"}'
```

## 🛡️ Security

- **No outbound data** — Vision inference runs via local Ollama, images never leave your device
- **No API keys** — No cloud services, no accounts, no tokens
- **localhost only** — Default binds to 127.0.0.1 (not exposed to network)
- **No telemetry** — Zero analytics, zero tracking, zero phoning home

## 🖥️ Requirements

- Python 3.10+
- [Ollama](https://ollama.ai) with a vision model installed
- Windows / Linux / macOS
- GPU recommended (CPU inference works but is 10-50x slower)

## 📄 License

MIT — use it, fork it, ship it.

---

<div align="center">

**Made by [bobfromarcher](https://github.com/bobfromarcher)**

[⬆ Back to Top](#-agent-capabilities)

</div>
