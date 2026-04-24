"""
coi_scanner.py — OCR a Certificate of Insurance image and extract key fields.

Uses LocoPilot's /vision/ocr endpoint to extract text from a COI
image, then applies simple regex parsing to pull out the policy
number, effective dates, and carrier name.
"""

import re
import requests

LOCOPILOT = "http://127.0.0.1:8264"

# Path or URL to the COI image — update before running
COI_IMAGE = "coi_sample.png"


def ocr_image(image_path: str) -> str:
    """Send an image to /vision/ocr and return extracted text."""
    import base64
    from pathlib import Path

    img_bytes = Path(image_path).read_bytes()
    b64 = base64.b64encode(img_bytes).decode()

    resp = requests.post(
        f"{LOCOPILOT}/vision/ocr",
        json={"image": f"data:image/png;base64,{b64}"},
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("text", data.get("content", ""))


def extract_fields(text: str) -> dict:
    """Parse policy number, dates, and carrier from OCR text."""
    fields = {}

    # Policy number: patterns like "POL-123456" or "Policy #: ABC-789"
    m = re.search(r"(?:policy\s*(?:no|#|number)[:\s]*)([A-Z0-9\-]+)", text, re.I)
    if m:
        fields["policy_number"] = m.group(1)

    # Effective date: MM/DD/YYYY or YYYY-MM-DD
    m = re.search(r"(?:effective\s*(?:date)?[:\s]*)(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text, re.I)
    if m:
        fields["effective_date"] = m.group(1)

    # Expiration date
    m = re.search(r"(?:expir(?:e|ation)\s*(?:date)?[:\s]*)(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text, re.I)
    if m:
        fields["expiration_date"] = m.group(1)

    # Carrier / insurer name (line after "Carrier" or "Insurer")
    m = re.search(r"(?:carrier|insurer|insurance\s*co\.?)[:\s]*([A-Za-z0-9\s&]+)", text, re.I)
    if m:
        fields["carrier"] = m.group(1).strip()

    return fields


def main():
    print(f"Scanning {COI_IMAGE} with OCR...")
    text = ocr_image(COI_IMAGE)
    print("\n--- Raw OCR Output (first 500 chars) ---")
    print(text[:500])
    fields = extract_fields(text)
    print("\n--- Extracted Fields ---")
    for key, value in fields.items():
        print(f"  {key}: {value}")
    if not fields:
        print("  (no fields matched — adjust regex patterns as needed)")

if __name__ == "__main__":
    main()
