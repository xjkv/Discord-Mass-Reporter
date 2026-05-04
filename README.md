# Discord Mass Reporter

⚠️ Disclaimer: This tool is for educational and authorized security testing purposes only. Misuse of this tool to harass or abuse Discord's reporting system violates Discord's Terms of Service. Use at your own risk.

A multi-threaded Discord message reporting tool that rotates through multiple authentication tokens to bypass rate limits. Built for penetration testing and security assessment of Discord's reporting API.

Features:
- Token Rotation — Automatically distributes reports across multiple tokens to avoid rate limiting
- Multi-threaded — Uses ThreadPoolExecutor for concurrent report submission (up to 5 workers)
- Configurable Breadcrumbs — Supports all Discord report categories via customizable breadcrumb paths
- Rate Limit Handling — Intelligent retry logic with token cooldown tracking
- Menu Verification — Fetches and validates the report menu structure before sending

## Prerequisites:
- Python 3.7+
- requests library

## Installation:
pip install requests

## Configuration:

1. Add Tokens — Edit the TOKENS list in main.py:
TOKENS = [
    "your_token_here",
    "another_token_here",
]
Add as many as possible — 10+ recommended. Each token can send approximately 1 report per hour before being rate-limited.

2. Set Target Message:
GUILD_ID = "your_guild_id"
CHANNEL_ID = "your_channel_id"
MESSAGE_ID = "your_message_id"
NUM_REPORTS = 50

3. Choose Report Category (Breadcrumbs):
Spam = [7, 98]
Abuse / Verbal harassment = [7, 76, 101]
Abuse / Hate identity = [7, 76, 107]
Abuse / Gore = [7, 76, 86, 108]
Abuse / NSFW unwanted = [7, 76, 86, 109]
Abuse / Threat of violence = [7, 76, 90, 117]
Abuse / CSAM = [7, 76, 86, 88, 116]
Misinfo / Fake news = [7, 94, 95, 131]
Something else / Underage = [7, 80, 91, 127]
Something else / Scam = [7, 80, 121, 167]
Something else / Stolen accounts = [7, 80, 123]
Something else / Illicit goods = [7, 80, 124]
Something else / Hacks cheats = [7, 80, 126]

Set BREADCRUMBS = [7, 76, 101] for Abuse / Verbal harassment.

# Usage:
python main.py

The tool will:
- Fetch and verify the report menu structure
- Display the selected breadcrumb path nodes
- Distribute reports across all available tokens
- Display real-time progress for each token thread
- Show a summary on completion

# How It Works:
Discord's reporting API uses a breadcrumb-based navigation system (/api/v9/reporting/menu/message) that mirrors the in-app reporting flow. Each breadcrumb represents a selection in the reporting wizard. For example, 7 is the report category selection root, 76 is abuse or harassment, and 101 is verbal harassment. The tool sends POST requests to /api/v9/reporting/message with the breadcrumb payload. Rate limits are per-token at approximately 1 report per hour, so rotating across many tokens enables higher throughput.

Project Structure:
Discord-Mass-Reporter/
├── main.py
├── LICENSE
└── README.md

If you face any issue, send me a dm on discord: desblessures.

License : MIT
