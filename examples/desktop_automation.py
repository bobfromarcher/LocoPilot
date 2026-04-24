"""
desktop_automation.py — Open an app and perform a sequence of actions.

Uses LocoPilot's /desktop/hotkey to open the Start menu, /desktop/see
to verify what's on screen, and /desktop/find_and_click to interact
with UI elements. Demonstrates a typical desktop automation flow.
"""

import time
import requests

LOCOPILOT = "http://127.0.0.1:8264"
APP_NAME = "Notepad"  # change to your target app


def hotkey(keys: str) -> dict:
    """Send a keyboard shortcut via /desktop/hotkey."""
    resp = requests.post(f"{LOCOPILOT}/desktop/hotkey", json={"keys": keys})
    resp.raise_for_status()
    return resp.json()

def see() -> str:
    """Capture and describe the screen via /desktop/see."""
    resp = requests.post(f"{LOCOPILOT}/desktop/see", json={})
    resp.raise_for_status()
    data = resp.json()
    return data.get("description", data.get("text", str(data)))

def find_and_click(label: str) -> dict:
    """Find a UI element by label and click it."""
    resp = requests.post(f"{LOCOPILOT}/desktop/find_and_click", json={"label": label})
    resp.raise_for_status()
    return resp.json()

def type_text(text: str) -> dict:
    """Type text into the currently focused element."""
    resp = requests.post(f"{LOCOPILOT}/desktop/type", json={"text": text})
    resp.raise_for_status()
    return resp.json()


def open_app(name: str):
    """Open the Start menu, search for an app, and launch it."""
    print(f"Opening Start menu to search for '{name}'...")
    hotkey("win")
    time.sleep(1)
    type_text(name)
    time.sleep(1)
    hotkey("enter")
    time.sleep(2)
    description = see()
    print(f"Screen: {description[:150]}...")

def main():
    # Step 1: Open the target application
    open_app(APP_NAME)
    # Step 2: Check what's on screen
    print("\nChecking screen after launch...")
    description = see()
    print(f"  {description[:200]}")
    # Step 3: Click into the editor area
    print("\nClicking the text editor area...")
    find_and_click("text editor")
    # Step 4: Type some content
    print("Typing content...")
    type_text("Hello from LocoPilot desktop automation!")
    # Step 5: Save the file
    print("Saving with Ctrl+S...")
    hotkey("ctrl+s")
    time.sleep(1)
    print("\nAutomation sequence complete.")

if __name__ == "__main__":
    main()
