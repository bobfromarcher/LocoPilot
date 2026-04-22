param(
    [string]$Model = "moondream",
    [string]$Port = "8264"
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LocoPilot - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$pythonOk = $false
try { $null = python --version 2>&1; $pythonOk = $true } catch {}

if (-not $pythonOk) {
    Write-Host "[FAIL] Python not found. Install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Python found" -ForegroundColor Green

Write-Host ""
Write-Host "Installing Python packages..." -ForegroundColor Yellow
pip install fastapi uvicorn httpx pyautogui Pillow pydantic playwright --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] pip install failed" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Python packages installed" -ForegroundColor Green

Write-Host ""
Write-Host "Installing Playwright Chromium..." -ForegroundColor Yellow
playwright install chromium
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Playwright install failed" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Playwright Chromium installed" -ForegroundColor Green

$ollamaOk = $false
try { $null = ollama --version 2>&1; $ollamaOk = $true } catch {}

if (-not $ollamaOk) {
    Write-Host ""
    Write-Host "[WARN] Ollama not found. Install from https://ollama.ai" -ForegroundColor Yellow
    Write-Host "       Then run: ollama pull $Model" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "Pulling vision model '$Model'..." -ForegroundColor Yellow
    ollama pull $Model
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[WARN] Model pull failed. Run manually: ollama pull $Model" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] Model '$Model' pulled" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Start:  python server.py --port $Port --model $Model" -ForegroundColor White
Write-Host "  Docs:   http://127.0.0.1:$Port/docs" -ForegroundColor White
Write-Host ""
