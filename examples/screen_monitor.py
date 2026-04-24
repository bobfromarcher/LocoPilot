"""
screen_monitor.py — Monitor the screen for changes.

Periodically captures and describes the screen using LocoPilot's
/desktop/see endpoint, then compares descriptions to detect changes.
Alerts when something new appears.
"""

import time
import requests

LOCOPILOT = "http://127.0.0.1:8264"
POLL_INTERVAL = 10  # seconds between checks


def see_screen() -> str:
    """Capture and describe the current screen via /desktop/see."""
    resp = requests.post(f"{LOCOPILOT}/desktop/see", json={})
    resp.raise_for_status()
    data = resp.json()
    # /desktop/see returns a natural-language description of the screen
    return data.get("description", data.get("text", str(data)))


def monitor(loop_count: int = 20):
    """Poll the screen and alert on changes."""
    last_description = None

    for i in range(loop_count):
        current = see_screen()
        timestamp = time.strftime("%H:%M:%S")

        if last_description is None:
            print(f"[{timestamp}] Initial screen captured.")
        elif current != last_description:
            print(f"\n[{timestamp}] *** CHANGE DETECTED ***")
            print(f"  Previous: {last_description[:120]}...")
            print(f"  Current:  {current[:120]}...")
        else:
            print(f"[{timestamp}] No change.")

        last_description = current
        time.sleep(POLL_INTERVAL)

    print("\nMonitoring complete.")


def main():
    print(f"Starting screen monitor (every {POLL_INTERVAL}s, {20} rounds)...")
    monitor(loop_count=20)


if __name__ == "__main__":
    main()
