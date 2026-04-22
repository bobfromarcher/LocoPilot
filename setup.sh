#!/usr/bin/env bash
set -e

MODEL="${1:-moondream}"
PORT="${2:-8264}"

echo ""
echo "========================================"
echo "  Agent Capabilities - Setup"
echo "========================================"
echo ""

if ! command -v python3 &>/dev/null; then
    echo "[FAIL] Python3 not found. Install Python 3.10+"
    exit 1
fi
echo "[OK] Python3 found"

echo ""
echo "Installing Python packages..."
pip3 install fastapi uvicorn httpx pyautogui Pillow pydantic playwright --quiet
echo "[OK] Python packages installed"

echo ""
echo "Installing Playwright Chromium..."
playwright install chromium
echo "[OK] Playwright Chromium installed"

if command -v ollama &>/dev/null; then
    echo ""
    echo "Pulling vision model '$MODEL'..."
    ollama pull "$MODEL" || echo "[WARN] Model pull failed. Run manually: ollama pull $MODEL"
    echo "[OK] Model '$MODEL' pulled"
else
    echo ""
    echo "[WARN] Ollama not found. Install from https://ollama.ai"
    echo "       Then run: ollama pull $MODEL"
fi

echo ""
echo "========================================"
echo "  Setup complete!"
echo "========================================"
echo ""
echo "  Start:  python3 server.py --port $PORT --model $MODEL"
echo "  Docs:   http://127.0.0.1:$PORT/docs"
echo ""
