# GitHub Discussions — Seed Posts

Enable Discussions on the LocoPilot repo, then create these 5 seed posts to jumpstart community engagement.

---

## Post 1 (Category: General)

**Title:** Welcome to LocoPilot Discussions!

**Body:**
This is the place to ask questions, share how you're using LocoPilot, request features, and connect with other builders.

LocoPilot gives any local LLM the ability to see, browse, and control — all running on your device with zero cloud dependencies. 35 endpoints, one file, MIT license.

Quick links:
- 📖 [Full API Reference](https://github.com/bobfromarcher/LocoPilot#-full-capabilities)
- 🐛 [Report a Bug](https://github.com/bobfromarcher/LocoPilot/issues/new?template=bug_report.yml)
- 💡 [Request a Feature](https://github.com/bobfromarcher/LocoPilot/issues/new?template=feature_request.yml)
- ⚡ [Quickstart Guide](https://github.com/bobfromarcher/LocoPilot#-quickstart)

What are you building with LocoPilot? Drop a comment below.

---

## Post 2 (Category: Ideas)

**Title:** What endpoints would make LocoPilot more useful for you?

**Body:**
We have 35 endpoints across Vision, Browser, and Desktop. What's missing?

Some ideas we're considering:
- `/browser/fill_form` — fill an entire form from a JSON object
- `/desktop/wait_for_text` — wait until specific text appears on screen
- `/vision/extract_tables` — structured table extraction from images
- `/system/batch` — execute multiple endpoint calls in sequence

What would you use? What's your #1 missing capability?

---

## Post 3 (Category: Show and Tell)

**Title:** LocoPilot powers TachyonTracker's COI Scanner — here's how

**Body:**
At [de Montfort LLC](https://github.com/bobfromarcher), we built LocoPilot to solve a real problem: automating Certificate of Insurance (COI) verification for construction and oil & gas companies.

Our product [TachyonTracker](https://tachyontracker.com) uses LocoPilot's vision endpoints to:
1. Accept COI images uploaded by contractors
2. OCR the document text using `/vision/ocr`
3. Parse insurance fields (policy numbers, dates, limits) with a local LLM
4. Validate against custom requirements
5. Flag errors and gaps — in 3 seconds, vs 3-7 business days for manual review

**60% of COIs contain errors.** Catching them automatically saves companies thousands per project.

The key insight: LocoPilot's local-first architecture means insurance documents never leave the user's device. No cloud, no API keys, no data privacy concerns.

What are you scanning/analyzing with LocoPilot's vision?

---

## Post 4 (Category: Q&A)

**Title:** Best vision model for find_and_click? (moondream vs llava vs minicpm-v)

**Body:**
The `/desktop/find_and_click` endpoint works by asking the vision model for pixel coordinates. We've found that model choice significantly impacts accuracy:

- **moondream** (1.7 GB): Great for descriptions, struggles with coordinate extraction
- **llava** (4.5 GB): Good spatial reasoning, decent coordinate accuracy
- **llava-llama3** (5.5 GB): Best coordinate extraction, but slowest
- **minicpm-v** (2.6 GB): Fast OCR, haven't tested extensively for coordinates

What model are you using for `find_and_click`? Any tips for improving accuracy?

---

## Post 5 (Category: Enterprise)

**Title:** Using LocoPilot in production? Let's talk

**Body:**
We're interested in hearing from anyone running LocoPilot in a production environment — whether it's embedded in a SaaS product (like our TachyonTracker), used for internal automation, or powering an agent framework.

Questions for the community:
- What's your use case?
- How do you handle reliability/error recovery?
- Do you run LocoPilot on a server or on developer machines?
- Have you needed to modify server.py for your deployment?

If there's enough interest, we could create an "Enterprise" discussion category for production deployment topics.
