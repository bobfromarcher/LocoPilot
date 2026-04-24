"""
form_filler.py — Fill a web form from a JSON data object.

Demonstrates the pattern for automated form submission using
LocoPilot's /browser/browse, /browser/type, and /browser/click.
"""

import requests

LOCOPILOT = "http://127.0.0.1:8264"

# Sample form data — replace URL and fields with your own target
FORM_URL = "https://httpbin.org/forms/post"
FORM_DATA = {
    "custname": "Ada Lovelace",
    "custemail": "ada@example.com",
    "custtel": "555-0123",
    "size": "medium",
    "topping": "cheese",
    "delivery": "12:00",
    "comments": "No onions please.",
}


def browse(url: str) -> dict:
    """Navigate the browser to a URL."""
    resp = requests.post(f"{LOCOPILOT}/browser/browse", json={"url": url})
    resp.raise_for_status()
    return resp.json()


def type_text(selector: str, text: str) -> dict:
    """Type text into the element matched by selector."""
    resp = requests.post(
        f"{LOCOPILOT}/browser/type", json={"selector": selector, "text": text}
    )
    resp.raise_for_status()
    return resp.json()


def click(selector: str) -> dict:
    """Click the element matched by selector."""
    resp = requests.post(
        f"{LOCOPILOT}/browser/click", json={"selector": selector}
    )
    resp.raise_for_status()
    return resp.json()


def fill_form(url: str, data: dict):
    """Navigate to the form, fill each field, and submit."""
    print(f"Navigating to {url} ...")
    browse(url)

    # Map form data keys to likely CSS selectors / input names.
    # Adjust selectors to match the actual form on your target page.
    for field, value in data.items():
        selector = f"input[name='{field}'], textarea[name='{field}']"
        print(f"  Typing into {field!r}: {value!r}")
        type_text(selector, value)

    # Submit the form by clicking the submit button
    print("  Clicking submit button...")
    click("button[type='submit'], input[type='submit']")

    print("Form submitted.")


def main():
    fill_form(FORM_URL, FORM_DATA)


if __name__ == "__main__":
    main()
