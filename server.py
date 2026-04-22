"""
LocoPilot — Local vision, browser, and desktop control for any LLM.
One file. Zero cloud. Runs on your machine.

Usage:
    python server.py                # Start on localhost:8264
    python server.py --port 9000    # Custom port
    python server.py --model llava  # Use a different vision model

Requires: pip install fastapi uvicorn httpx pyautogui Pillow pydantic playwright
Then:     playwright install chromium
And:      ollama pull moondream  (or any vision model)
"""

import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
from fastapi import FastAPI
from PIL import Image
from pydantic import BaseModel, Field

# ── Config ──────────────────────────────────────────────────────────────────

DEFAULT_MODEL = os.environ.get("AC_VISION_MODEL", "moondream")
DEFAULT_HOST = os.environ.get("AC_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("AC_PORT", "8264"))
DEFAULT_OLLAMA = os.environ.get("AC_OLLAMA_URL", "http://127.0.0.1:11434")
SCREENSHOT_DIR = Path(os.environ.get("AC_SCREENSHOT_DIR", "./screenshots"))
SCREENSHOT_DIR.mkdir(exist_ok=True)

OLLAMA_BASE = DEFAULT_OLLAMA
USE_WSL = False
WSL_DISTRO = os.environ.get("AC_WSL_DISTRO", "Ubuntu")
VISION_MODEL = DEFAULT_MODEL

# ── Ollama Transport ────────────────────────────────────────────────────────

def _load_config():
    global OLLAMA_BASE, USE_WSL, VISION_MODEL, WSL_DISTRO
    cfg_path = Path(__file__).parent / "config.json"
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text())
        OLLAMA_BASE = cfg.get("ollama_base_url", OLLAMA_BASE)
        VISION_MODEL = cfg.get("vision_model", VISION_MODEL)
        WSL_DISTRO = cfg.get("wsl_distro", WSL_DISTRO)
    if OLLAMA_BASE == "wsl":
        USE_WSL = True

_load_config()


def _wsl_exec(args, timeout=600):
    return subprocess.run(
        ["wsl", "-d", WSL_DISTRO, "--"] + args,
        capture_output=True, text=True, timeout=timeout,
    )


def ollama_generate(payload: dict) -> dict:
    if USE_WSL:
        tmp = Path(tempfile.mktemp(suffix=".json"))
        tmp.write_text(json.dumps(payload), encoding="utf-8")
        wsl_path = f"/mnt/c/{tmp.resolve().as_posix()[3:]}"
        r = _wsl_exec(["bash", "-c", f"curl -s -d @{wsl_path} -H 'Content-Type: application/json' http://127.0.0.1:11434/api/generate"])
        try: tmp.unlink(missing_ok=True)
        except: pass
        if r.returncode != 0:
            return {"error": f"WSL curl failed: {r.stderr[:300]}"}
        try: return json.loads(r.stdout.strip())
        except: return {"error": f"Bad response: {r.stdout[:200]}"}
    resp = httpx.post(f"{OLLAMA_BASE}/api/generate", json=payload, timeout=600)
    if resp.status_code != 200:
        return {"error": f"Ollama HTTP {resp.status_code}: {resp.text[:200]}"}
    return resp.json()


def ollama_chat(messages: list, images: list = None, model: str = None) -> dict:
    payload = {"model": model or VISION_MODEL, "messages": messages, "stream": False}
    if images:
        content = messages[-1].get("content", "")
        payload["messages"][-1] = {
            "role": "user",
            "content": content,
            "images": images,
        }
    if USE_WSL:
        tmp = Path(tempfile.mktemp(suffix=".json"))
        tmp.write_text(json.dumps(payload), encoding="utf-8")
        wsl_path = f"/mnt/c/{tmp.resolve().as_posix()[3:]}"
        r = _wsl_exec(["bash", "-c", f"curl -s -d @{wsl_path} -H 'Content-Type: application/json' http://127.0.0.1:11434/api/chat"])
        try: tmp.unlink(missing_ok=True)
        except: pass
        if r.returncode != 0:
            return {"error": f"WSL curl failed: {r.stderr[:300]}"}
        try: return json.loads(r.stdout.strip())
        except: return {"error": f"Bad response: {r.stdout[:200]}"}
    resp = httpx.post(f"{OLLAMA_BASE}/api/chat", json=payload, timeout=600)
    if resp.status_code != 200:
        return {"error": f"Ollama HTTP {resp.status_code}: {resp.text[:200]}"}
    return resp.json()


def ollama_check() -> bool:
    try:
        if USE_WSL:
            r = _wsl_exec(["bash", "-c", "curl -s http://127.0.0.1:11434/api/tags"], timeout=10)
            return r.returncode == 0 and "models" in r.stdout
        httpx.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        return True
    except:
        return False


def ollama_list_models() -> list:
    try:
        if USE_WSL:
            r = _wsl_exec(["bash", "-c", "curl -s http://127.0.0.1:11434/api/tags"], timeout=10)
            if r.returncode != 0: return []
            data = json.loads(r.stdout)
        else:
            resp = httpx.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
            if resp.status_code != 200: return []
            data = resp.json()
        return [m.get("name", "") for m in data.get("models", [])]
    except:
        return []


# ── Image Helpers ────────────────────────────────────────────────────────────

def _img_to_b64(img: Image.Image, max_kb=2048) -> str:
    if img.mode == "RGBA":
        img = img.convert("RGB")
    buf = io.BytesIO()
    q = 85
    img.save(buf, format="JPEG", quality=q)
    while buf.tell() > max_kb * 1024 and q > 30:
        buf = io.BytesIO()
        q -= 10
        img.save(buf, format="JPEG", quality=q)
    return base64.b64encode(buf.getvalue()).decode()


def _load_image(src) -> Image.Image:
    if isinstance(src, Image.Image):
        return src
    if isinstance(src, str) and src.startswith("data:image"):
        header, b64data = src.split(",", 1)
        return Image.open(io.BytesIO(base64.b64decode(b64data)))
    p = Path(src)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p}")
    return Image.open(p)


def _save_screenshot(img: Image.Image, prefix="screen") -> str:
    ts = int(time.time())
    p = SCREENSHOT_DIR / f"{prefix}_{ts}.png"
    img.save(p)
    return str(p)


# ── Coordinate Parsing ──────────────────────────────────────────────────────

def _parse_coords(text: str) -> Optional[Tuple[int, int]]:
    text = text.strip()
    for pattern in [
        r'\(?(\d{1,4})\s*[,x]\s*(\d{1,4})\)?',
        r'x\s*=\s*(\d{1,4})\D+y\s*=\s*(\d{1,4})',
        r'(\d{1,4})\s+(\d{1,4})',
        r'at\s+(\d{1,4})\D+(\d{1,4})',
        r'position[:\s]+(\d{1,4})\D+(\d{1,4})',
    ]:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return int(m.group(1)), int(m.group(2))
    nums = re.findall(r'\d{2,4}', text)
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    return None


# ── Core Actions ────────────────────────────────────────────────────────────

def act_analyze(image, prompt="Describe this image in detail.", model=None) -> dict:
    img = _load_image(image)
    b64 = _img_to_b64(img)
    t0 = time.time()
    r = ollama_generate({"model": model or VISION_MODEL, "prompt": prompt, "images": [b64], "stream": False})
    return {"description": r.get("response", ""), "model": r.get("model"), "duration_s": round(time.time() - t0, 1), "tokens": r.get("eval_count", 0), "error": r.get("error")}


def act_capture(prompt="Describe what is on screen.", model=None, save_path=None) -> dict:
    import pyautogui
    img = pyautogui.screenshot()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(save_path)
    else:
        save_path = _save_screenshot(img, "capture")
    return act_analyze(img, prompt=prompt, model=model)


def act_ocr(image, model=None) -> dict:
    return act_analyze(image, prompt="Extract ALL text from this image verbatim. Preserve layout and formatting. For forms or documents, list each field name and its value.", model=model)


def act_compare(img_a, img_b, prompt="Compare these two images. Describe what changed between them in detail.", model=None) -> dict:
    a = _img_to_b64(_load_image(img_a))
    b = _img_to_b64(_load_image(img_b))
    t0 = time.time()
    r = ollama_generate({"model": model or VISION_MODEL, "prompt": prompt, "images": [a, b], "stream": False})
    return {"differences": r.get("response", ""), "model": r.get("model"), "duration_s": round(time.time() - t0, 1), "error": r.get("error")}


def act_see(prompt="Describe the screen. List all visible buttons, links, icons, and UI elements with their approximate pixel positions.", model=None, region=None) -> dict:
    import pyautogui
    img = pyautogui.screenshot(region=region)
    save_path = _save_screenshot(img, "see")
    r = act_analyze(img, prompt=prompt, model=model)
    r["screenshot"] = save_path
    return r


def act_find_click(target, action="click", model=None) -> dict:
    import pyautogui
    r = act_see(prompt=f"Where is '{target}' on screen? Respond with ONLY the pixel coordinates as two numbers separated by a comma, like: 500,300. No other text.", model=model)
    desc = r.get("description", "").strip()
    coords = _parse_coords(desc)
    if coords:
        x, y = coords
        if action == "click":
            pyautogui.click(x, y)
        elif action == "double_click":
            pyautogui.doubleClick(x, y)
        elif action == "right_click":
            pyautogui.rightClick(x, y)
        elif action == "hover":
            pyautogui.moveTo(x, y)
        elif action == "triple_click":
            pyautogui.tripleClick(x, y)
        return {"found": True, "action": action, "target": target, "position": [x, y]}
    return {"found": False, "target": target, "vision_response": desc}


# ── Browser State ──────────────────────────────────────────────────────────

_bw = None


async def _get_page():
    global _bw
    if _bw and not _bw[3].is_closed():
        return _bw[3]
    from playwright.async_api import async_playwright
    pw = await async_playwright().start()
    br = await pw.chromium.launch(headless=False)
    ctx = await br.new_context(viewport={"width": 1280, "height": 900})
    pg = await ctx.new_page()
    pg.set_default_timeout(30000)
    _bw = (pw, br, ctx, pg)
    return pg


async def act_browse(url, wait=2.0) -> dict:
    import asyncio
    pg = await _get_page()
    try:
        await pg.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(wait)
        return {"url": pg.url, "title": await pg.title()}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_screenshot(full_page=False) -> dict:
    pg = await _get_page()
    try:
        png = await pg.screenshot(full_page=full_page)
        img = Image.open(io.BytesIO(png))
        save_path = _save_screenshot(img, "browser")
        return {"path": save_path, "width": img.width, "height": img.height, "full_page": full_page}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_click(selector, button="left", click_count=1) -> dict:
    import asyncio
    pg = await _get_page()
    try:
        el = await pg.wait_for_selector(selector)
        await el.click(button=button, click_count=click_count)
        await asyncio.sleep(0.5)
        return {"clicked": selector, "button": button}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_type(selector, text, clear=True, enter=False, delay=50) -> dict:
    import asyncio
    pg = await _get_page()
    try:
        el = await pg.wait_for_selector(selector)
        if clear: await el.fill("")
        await el.type(text, delay=delay)
        if enter:
            await el.press("Enter")
            await asyncio.sleep(1)
        return {"typed": text, "into": selector}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_scroll(direction="down", amount=3) -> dict:
    pg = await _get_page()
    delta = 300 * amount * (1 if direction == "down" else -1)
    await pg.mouse.wheel(0, delta)
    return {"scrolled": direction, "pixels": abs(delta)}


async def act_page_text() -> dict:
    pg = await _get_page()
    try:
        return {"title": await pg.title(), "url": pg.url, "text": (await pg.inner_text("body"))[:50000]}
    except Exception as e:
        return {"error": str(e)}


async def act_page_links() -> dict:
    pg = await _get_page()
    try:
        links = await pg.eval_on_selector_all("a[href]", "els => els.map(e => ({text: e.innerText.trim(), href: e.href}))")
        return {"count": len(links), "links": links[:200]}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_evaluate(expression: str) -> dict:
    pg = await _get_page()
    try:
        result = await pg.evaluate(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_go_back() -> dict:
    import asyncio
    pg = await _get_page()
    try:
        await pg.go_back(wait_until="domcontentloaded")
        await asyncio.sleep(1)
        return {"url": pg.url, "title": await pg.title()}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_go_forward() -> dict:
    import asyncio
    pg = await _get_page()
    try:
        await pg.go_forward(wait_until="domcontentloaded")
        await asyncio.sleep(1)
        return {"url": pg.url, "title": await pg.title()}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_select_option(selector: str, value: str) -> dict:
    pg = await _get_page()
    try:
        el = await pg.wait_for_selector(selector)
        await el.select_option(value=value)
        return {"selected": value, "element": selector}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_wait(selector: str, timeout=10000) -> dict:
    pg = await _get_page()
    try:
        await pg.wait_for_selector(selector, timeout=timeout)
        return {"found": selector}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_close() -> dict:
    global _bw
    if _bw:
        try:
            await _bw[3].close()
            await _bw[2].close()
            await _bw[1].close()
            await _bw[0].stop()
        except: pass
        _bw = None
    return {"closed": True}


async def act_browse_and_read(url, vision_model=None) -> dict:
    nav = await act_browse(url, wait=3.0)
    if "error" in nav: return nav
    ss = await act_browse_screenshot(full_page=False)
    if "error" in ss: return ss
    txt = await act_page_text()
    vision = act_analyze(ss["path"], model=vision_model)
    return {"url": nav.get("url"), "title": nav.get("title"), "text_preview": txt.get("text", "")[:3000], "vision": vision.get("description", ""), "model": vision.get("model")}


async def act_browse_cookies() -> dict:
    pg = await _get_page()
    try:
        ctx = pg.context
        cookies = await ctx.cookies()
        return {"count": len(cookies), "cookies": cookies}
    except Exception as e:
        return {"error": str(e)}


async def act_browse_pdf(path: str = "") -> dict:
    pg = await _get_page()
    try:
        if not path:
            ts = int(time.time())
            path = str(SCREENSHOT_DIR / f"page_{ts}.pdf")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        await pg.pdf(path=path)
        return {"path": path}
    except Exception as e:
        return {"error": str(e)}


# ── Request Models ──────────────────────────────────────────────────────────

class ImageReq(BaseModel):
    image_path: str
    prompt: str = "Describe this image in detail."
    model: str | None = None

class CaptureReq(BaseModel):
    prompt: str = "Describe what is on screen."
    model: str | None = None
    save_path: str | None = None

class OCRReq(BaseModel):
    image_path: str
    model: str | None = None

class CompareReq(BaseModel):
    image_a: str
    image_b: str
    prompt: str = "Compare these two images. Describe what changed between them in detail."
    model: str | None = None

class SeeReq(BaseModel):
    prompt: str = "Describe the screen. List all visible buttons, links, icons, and UI elements with their approximate pixel positions."
    model: str | None = None
    region: list[int] | None = None

class FindReq(BaseModel):
    target: str
    action: str = "click"
    model: str | None = None

class MoveReq(BaseModel):
    x: int
    y: int
    duration: float = 0.3

class ClickReq(BaseModel):
    x: int | None = None
    y: int | None = None
    button: str = "left"
    clicks: int = 1

class DragReq(BaseModel):
    from_x: int; from_y: int; to_x: int; to_y: int
    duration: float = 0.5

class DScrollReq(BaseModel):
    clicks: int; x: int | None = None; y: int | None = None

class DTypeReq(BaseModel):
    text: str; interval: float = 0.05

class KeyReq(BaseModel):
    key: str; presses: int = 1

class HotkeyReq(BaseModel):
    keys: List[str]

class DScreenshotReq(BaseModel):
    save_path: str | None = None
    region: list[int] | None = None

class BrowseReq(BaseModel):
    url: str; wait: float = 2.0

class BrowseClickReq(BaseModel):
    selector: str; button: str = "left"; click_count: int = 1

class BrowseTypeReq(BaseModel):
    selector: str; text: str; clear: bool = True; enter: bool = False; delay: int = 50

class BrowseScrollReq(BaseModel):
    direction: str = "down"; amount: int = 3

class BrowseAndReadReq(BaseModel):
    url: str; vision_model: str | None = None

class BrowseEvalReq(BaseModel):
    expression: str

class BrowseSelectReq(BaseModel):
    selector: str; value: str

class BrowseWaitReq(BaseModel):
    selector: str; timeout: int = 10000

class BrowseScreenshotReq(BaseModel):
    full_page: bool = False

class BrowsePdfReq(BaseModel):
    path: str = ""


# ── FastAPI App ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="LocoPilot",
    version="1.1.0",
    description="Local vision, browser, and desktop control for any LLM. 35 endpoints across vision, browser, and desktop — all running on your device.",
)


@app.get("/health")
def health():
    ollama_ok = ollama_check()
    models = ollama_list_models() if ollama_ok else []
    return {
        "status": "ok" if ollama_ok else "degraded",
        "version": "1.1.0",
        "ollama": ollama_ok,
        "vision_model": VISION_MODEL,
        "available_models": models,
        "tools": ["vision", "browser", "desktop"],
    }


@app.get("/tools")
def list_tools():
    return {
        "vision": [
            {"name": "analyze_image", "path": "/vision/analyze", "method": "POST", "desc": "Analyze any image file with a custom prompt"},
            {"name": "capture_screen", "path": "/vision/capture", "method": "POST", "desc": "Screenshot the desktop and analyze with vision"},
            {"name": "ocr", "path": "/vision/ocr", "method": "POST", "desc": "Extract all text from an image"},
            {"name": "compare", "path": "/vision/compare", "method": "POST", "desc": "Compare two images and describe differences"},
        ],
        "browser": [
            {"name": "browse", "path": "/browser/browse", "method": "POST", "desc": "Navigate to a URL"},
            {"name": "screenshot", "path": "/browser/screenshot", "method": "POST", "desc": "Screenshot the current browser page"},
            {"name": "click", "path": "/browser/click", "method": "POST", "desc": "Click an element by CSS selector"},
            {"name": "type", "path": "/browser/type", "method": "POST", "desc": "Type text into an element"},
            {"name": "scroll", "path": "/browser/scroll", "method": "POST", "desc": "Scroll the page up or down"},
            {"name": "text", "path": "/browser/text", "method": "POST", "desc": "Extract all visible text from the page"},
            {"name": "links", "path": "/browser/links", "method": "POST", "desc": "Extract all links from the page"},
            {"name": "evaluate", "path": "/browser/evaluate", "method": "POST", "desc": "Run JavaScript in the browser"},
            {"name": "go_back", "path": "/browser/go_back", "method": "POST", "desc": "Navigate back in browser history"},
            {"name": "go_forward", "path": "/browser/go_forward", "method": "POST", "desc": "Navigate forward in browser history"},
            {"name": "select_option", "path": "/browser/select_option", "method": "POST", "desc": "Select a dropdown option by value"},
            {"name": "wait_for", "path": "/browser/wait_for", "method": "POST", "desc": "Wait for an element to appear on the page"},
            {"name": "cookies", "path": "/browser/cookies", "method": "GET", "desc": "Get all browser cookies"},
            {"name": "save_pdf", "path": "/browser/save_pdf", "method": "POST", "desc": "Save the current page as a PDF"},
            {"name": "close", "path": "/browser/close", "method": "POST", "desc": "Close the browser instance"},
            {"name": "browse_and_read", "path": "/browser/browse_and_read", "method": "POST", "desc": "Navigate + screenshot + vision + text extraction in one call"},
        ],
        "desktop": [
            {"name": "see", "path": "/desktop/see", "method": "POST", "desc": "Screenshot + vision analysis (one call)"},
            {"name": "find_and_click", "path": "/desktop/find_and_click", "method": "POST", "desc": "Describe a target, vision finds it, then clicks it"},
            {"name": "move", "path": "/desktop/move", "method": "POST", "desc": "Move the mouse to (x, y)"},
            {"name": "click", "path": "/desktop/click", "method": "POST", "desc": "Click at a position"},
            {"name": "double_click", "path": "/desktop/double_click", "method": "POST", "desc": "Double-click at a position"},
            {"name": "right_click", "path": "/desktop/right_click", "method": "POST", "desc": "Right-click at a position"},
            {"name": "drag", "path": "/desktop/drag", "method": "POST", "desc": "Drag from one point to another"},
            {"name": "scroll", "path": "/desktop/scroll", "method": "POST", "desc": "Scroll the mouse wheel"},
            {"name": "type_text", "path": "/desktop/type", "method": "POST", "desc": "Type text with the keyboard"},
            {"name": "press_key", "path": "/desktop/press_key", "method": "POST", "desc": "Press a single key"},
            {"name": "hotkey", "path": "/desktop/hotkey", "method": "POST", "desc": "Press a key combination (e.g. ctrl+c)"},
            {"name": "screenshot", "path": "/desktop/screenshot", "method": "POST", "desc": "Take a desktop screenshot"},
            {"name": "mouse_position", "path": "/desktop/mouse_position", "method": "GET", "desc": "Get current mouse position and screen size"},
        ],
    }


# ── Vision ───────────────────────────────────────────────────────────────────

@app.post("/vision/analyze")
def api_analyze(req: ImageReq):
    try: return act_analyze(req.image_path, req.prompt, req.model)
    except Exception as e: return {"error": str(e)}

@app.post("/vision/capture")
def api_capture(req: CaptureReq):
    try: return act_capture(req.prompt, req.model, req.save_path)
    except Exception as e: return {"error": str(e)}

@app.post("/vision/ocr")
def api_ocr(req: OCRReq):
    try: return act_ocr(req.image_path, req.model)
    except Exception as e: return {"error": str(e)}

@app.post("/vision/compare")
def api_compare(req: CompareReq):
    try: return act_compare(req.image_a, req.image_b, req.prompt, req.model)
    except Exception as e: return {"error": str(e)}


# ── Browser ─────────────────────────────────────────────────────────────────

@app.post("/browser/browse")
async def api_browse(req: BrowseReq):
    return await act_browse(req.url, req.wait)

@app.post("/browser/screenshot")
async def api_browse_screenshot(req: BrowseScreenshotReq = BrowseScreenshotReq()):
    return await act_browse_screenshot(full_page=req.full_page)

@app.post("/browser/click")
async def api_browse_click(req: BrowseClickReq):
    return await act_browse_click(req.selector, req.button, req.click_count)

@app.post("/browser/type")
async def api_browse_type(req: BrowseTypeReq):
    return await act_browse_type(req.selector, req.text, req.clear, req.enter, req.delay)

@app.post("/browser/scroll")
async def api_browse_scroll(req: BrowseScrollReq):
    return await act_browse_scroll(req.direction, req.amount)

@app.post("/browser/text")
async def api_page_text():
    return await act_page_text()

@app.post("/browser/links")
async def api_page_links():
    return await act_page_links()

@app.post("/browser/evaluate")
async def api_browse_evaluate(req: BrowseEvalReq):
    return await act_browse_evaluate(req.expression)

@app.post("/browser/go_back")
async def api_browse_go_back():
    return await act_browse_go_back()

@app.post("/browser/go_forward")
async def api_browse_go_forward():
    return await act_browse_go_forward()

@app.post("/browser/select_option")
async def api_browse_select_option(req: BrowseSelectReq):
    return await act_browse_select_option(req.selector, req.value)

@app.post("/browser/wait_for")
async def api_browse_wait(req: BrowseWaitReq):
    return await act_browse_wait(req.selector, req.timeout)

@app.post("/browser/cookies")
async def api_browse_cookies():
    return await act_browse_cookies()

@app.post("/browser/save_pdf")
async def api_browse_pdf(req: BrowsePdfReq = BrowsePdfReq()):
    return await act_browse_pdf(req.path)

@app.post("/browser/close")
async def api_browse_close():
    return await act_browse_close()

@app.post("/browser/browse_and_read")
async def api_browse_and_read(req: BrowseAndReadReq):
    return await act_browse_and_read(req.url, req.vision_model)


# ── Desktop ─────────────────────────────────────────────────────────────────

@app.post("/desktop/see")
def api_see(req: SeeReq):
    try: return act_see(req.prompt, req.model, tuple(req.region) if req.region else None)
    except Exception as e: return {"error": str(e)}

@app.post("/desktop/find_and_click")
def api_find(req: FindReq):
    try: return act_find_click(req.target, req.action, req.model)
    except Exception as e: return {"error": str(e)}

@app.post("/desktop/move")
def api_move(req: MoveReq):
    import pyautogui
    pyautogui.moveTo(req.x, req.y, duration=req.duration)
    return {"moved_to": [req.x, req.y]}

@app.post("/desktop/click")
def api_click(req: ClickReq):
    import pyautogui
    pyautogui.click(x=req.x, y=req.y, button=req.button, clicks=req.clicks)
    return {"clicked": [req.x, req.y, req.button]}

@app.post("/desktop/double_click")
def api_dblclick(req: ClickReq):
    import pyautogui
    pyautogui.doubleClick(x=req.x, y=req.y)
    return {"double_clicked": [req.x, req.y]}

@app.post("/desktop/right_click")
def api_rclick(req: ClickReq):
    import pyautogui
    pyautogui.rightClick(x=req.x, y=req.y)
    return {"right_clicked": [req.x, req.y]}

@app.post("/desktop/drag")
def api_drag(req: DragReq):
    import pyautogui
    pyautogui.moveTo(req.from_x, req.from_y)
    pyautogui.drag(req.to_x - req.from_x, req.to_y - req.from_y, duration=req.duration)
    return {"dragged": [[req.from_x, req.from_y], [req.to_x, req.to_y]]}

@app.post("/desktop/scroll")
def api_dscroll(req: DScrollReq):
    import pyautogui
    pyautogui.scroll(req.clicks, x=req.x, y=req.y)
    return {"scrolled": req.clicks}

@app.post("/desktop/type")
def api_dtype(req: DTypeReq):
    import pyautogui
    pyautogui.typewrite(req.text, interval=req.interval)
    return {"typed": req.text}

@app.post("/desktop/press_key")
def api_key(req: KeyReq):
    import pyautogui
    pyautogui.press(req.key, presses=req.presses)
    return {"pressed": req.key}

@app.post("/desktop/hotkey")
def api_hotkey(req: HotkeyReq):
    import pyautogui
    pyautogui.hotkey(*req.keys)
    return {"hotkey": req.keys}

@app.post("/desktop/screenshot")
def api_dscreenshot(req: DScreenshotReq):
    import pyautogui
    img = pyautogui.screenshot(region=tuple(req.region) if req.region else None)
    if req.save_path:
        Path(req.save_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(req.save_path)
        return {"path": req.save_path, "size": [img.width, img.height]}
    save_path = _save_screenshot(img, "desktop")
    return {"path": save_path, "size": [img.width, img.height]}

@app.get("/desktop/mouse_position")
def api_mouse():
    import pyautogui
    x, y = pyautogui.position()
    w, h = pyautogui.size()
    return {"x": x, "y": y, "screen": [w, h]}


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    parser = argparse.ArgumentParser(description="LocoPilot — Local vision, browser, and desktop control for any LLM")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama vision model (default: moondream)")
    args = parser.parse_args()
    VISION_MODEL = args.model
    print(f"""
  LocoPilot v1.1.0
  Vision + Browser + Desktop

  Server:  http://{args.host}:{args.port}
  Model:   {VISION_MODEL}
  Ollama:  {"WSL proxy" if USE_WSL else OLLAMA_BASE}
  Docs:    http://{args.host}:{args.port}/docs
""")
    uvicorn.run(app, host=args.host, port=args.port)
