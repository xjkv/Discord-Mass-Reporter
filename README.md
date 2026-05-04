# Discord Mass Reporter

Authorized Security Assessment Tool — Discord Reporting API Pentesting Framework

## Overview

Discord Mass Reporter is a concurrent, multi-threaded penetration testing framework designed for authorized security assessments of Discord's message reporting infrastructure. The tool leverages token rotation and intelligent rate-limit evasion to stress-test Discord's v9 reporting API endpoints under controlled, authorized conditions.

This software is intended exclusively for legitimate security professionals conducting authorized audits, bug bounty research, and red team operations. Written authorization from the asset owner is required prior to deployment.

## Core Capabilities

- Token Rotation Engine — Automatic distribution of report payloads across a pool of N authentication tokens, preventing per-token rate limit saturation
- Concurrent Execution — Multi-threaded architecture utilizing Python ThreadPoolExecutor with configurable worker count (default: 5)
- Breadcrumb Path Configuration — Full support for all Discord reporting categories via customizable integer breadcrumb arrays mapped to the internal menu tree
- Adaptive Rate Limit Handling — Intelligent retry backoff with per-token cooldown tracking; tokens exceeding threshold retry times are temporarily removed from rotation
- Menu Structure Verification — Pre-execution validation of the report menu tree via GET /api/v9/reporting/menu/message to confirm breadcrumb integrity
- Real-time Telemetry — Per-thread stdout logging of HTTP status codes, report IDs, and rate limit windows

## Requirements

- Python >= 3.7
- requests >= 2.28

```bash
sudo apt update && sudo apt install python3 python3-pip -y
pip3 install requests
```

## Quick Start

-Clone the repository and navigate to the project root:
```bash
git clone https://github.com/YOUR_USERNAME/Discord-Mass-Reporter.git
cd Discord-Mass-Reporter
```

-Edit main.py and populate the configuration block:
```python
TOKENS = [
    "MTEzMDA4NDQ0OTE4Nzg0MDAw.DPNXFQ.xxxxxx",
    "MTEzNjkwNjA2MDk3NzkzMDI2.DPNczQ.xxxxxx",
    # Minimum 10 tokens recommended for meaningful throughput
]

GUILD_ID   = "1379444359505641542"
CHANNEL_ID = "1379447064894767134"
MESSAGE_ID = "1483214816398016512"

NUM_REPORTS = 50           # Total reports distributed across all tokens
MAX_WORKERS = min(5, len(TOKENS))  # Thread pool size
```

-And finally execute it :
```cmd
python main.py
```

## Breadcrumb Reference
Discord's internal reporting menu is structured as a tree of integer node IDs. Below are the validated breadcrumb paths for each report category:

Category	Breadcrumb Path
Spam:	[7, 98]
Abuse / Verbal harassment:	[7, 76, 101]
Abuse / Hate identity:	[7, 76, 107]
Abuse / Gore:	[7, 76, 86, 108]
Abuse / NSFW unwanted:	[7, 76, 86, 109]
Abuse / Threat of violence:	[7, 76, 90, 117]
Abuse / CSAM:	[7, 76, 86, 88, 116]
Misinfo / Fake news: [7, 94, 95, 131]
Something else / Underage:	[7, 80, 91, 127]
Something else / Scam:	[7, 80, 121, 167]
Something else / Stolen accounts:	[7, 80, 123]
Something else / Illicit goods:	[7, 80, 124]
Something else / Hacks cheats:	[7, 80, 126]

Set BREADCRUMBS in main.py to your desired value:
```python
BREADCRUMBS = [7, 76, 101]   # Abuse / Verbal harassment
```

## Operational Workflow
Upon execution, the framework performs the following sequence:

1 - Menu Discovery — Issues GET /api/v9/reporting/menu/message to retrieve the reporting menu tree and validate root_node_id
2 - Breadcrumb Verification — Walks the provided breadcrumb path, printing each node's key and header for operator confirmation
3 - Payload Assembly — Constructs the JSON payload containing version, variant, language, breadcrumbs, guild_id, channel_id, and message_id
4 - Token Distribution — Divides NUM_REPORTS evenly across all available tokens, allocating remainder to the first N tokens
5 - Concurrent Execution — Spawns MAX_WORKERS threads; each thread iterates its assigned report quota with jittered delays (2-5s)
6 - Rate Limit Mitigation — On HTTP 429, evaluates retry_after. If < 3600s, sleeps and retries once. If >= 3600s, marks token as cooled down for retry_after duration
7 - Token Expiry Detection — On HTTP 401, flags the token as invalid and reports to the operator
8 - Summary Reporting — Aggregates success/fail counts across all worker threads and displays final statistics

## API Internals
The framework targets Discord's internal reporting API:

- Endpoint: POST /api/v9/reporting/message
- Menu: GET /api/v9/reporting/menu/message
- Content-Type: application/json
- Required Headers: Authorization, X-Discord-Locale, X-Debug-Options

Rate limiting is enforced per-token with a retry-after header (typically 3000-4500 seconds per successful report). Token rotation is therefore mandatory for any assessment exceeding approximately 5-4 report per hour per token (proved and tested).

## Project Layout
```bash
Discord-Mass-Reporter/
├── main.py          # Entry point — configuration and execution logic
├── LICENSE          # MIT License
└── README.md        # This file
```
## Legal Notice

This tool is designed exclusively for authorized penetration testing and security research. Unauthorized use of this software to send fraudulent or abusive reports to Discord is a violation of Discord's Terms of Service and may constitute a violation of applicable computer fraud and abuse laws. The operator bears sole responsibility for ensuring proper authorization is obtained prior to deployment.

## Support

For issues, inquiries, or collaboration: Discord — desblessures

## License
MIT - See LICENSE text.




