import requests
import json
import time
import random
import sys
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

print("──────────────────────────────────────────────────────────")
# ASCII BANNER (wings banner cool right?)
# ──────────────────────────────────────────────────────────
BANNER = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⣷⠙⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⣼⣖⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⠟⣛⠼⠓⠿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠿⠞⠧⣜⠻⣅⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣾⡷⠋⢀⣤⢄⠀⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⠀⡠⣤⡄⠑⢾⣷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣿⠟⠀⡄⡻⠇⠀⢡⠀⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⡀⠀⠺⢿⢢⡀⠻⡻⡄⠀⠀⠀⠀
⠀⠀⠀⣠⢋⠎⠀⡼⠀⡇⠀⠂⡀⠁⡀⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⢀⠌⢀⠑⠦⢸⠀⣧⠀⠱⡜⢆⠀⠀⠀
⠀⠀⡰⠁⡞⠀⣼⡃⠀⣧⡄⠚⢷⡄⠈⠀⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠗⠁⢰⣾⠟⢀⣼⡀⢸⣷⠀⢱⠈⢧⠀⠀
⠀⡸⠁⣸⠁⢠⠇⡅⢰⣿⢡⡇⠀⠻⣿⣦⡰⢌⡑⠢⢤⣤⡀⠀⠀⠀⠀⢀⣤⣤⠴⢊⡡⢆⢴⣿⠟⠀⢸⡄⣿⡇⢸⠘⡄⠀⢧⠈⢧⠀
⢀⣇⠴⡇⠀⢸⠀⡇⢸⢿⣏⣧⡇⠀⠙⠛⠿⢦⣬⡓⢄⣉⠛⣄⠀⠀⣠⠞⢋⡠⢒⣉⣴⡿⠛⠃⠀⢸⣾⣿⡿⡇⢰⠀⢇⠀⠸⠧⣘⡆
⠘⠁⢸⠀⠀⡇⢴⠁⠈⡆⢻⣿⣦⡀⣷⣰⡤⠈⠛⢻⣴⣿⡿⠛⠃⠘⠛⢿⣷⣶⡿⠛⡁⢴⣶⣿⢀⣾⣿⡟⢀⠃⢸⣄⢸⠀⠀⠇⠈⠃
⠀⠀⡄⠀⢸⠁⢸⡇⠀⡇⠀⢻⠻⠿⠿⣿⣡⣿⣶⣶⢈⡌⡅⣶⣆⢰⣶⢨⠰⡉⣷⣦⣻⣾⣿⠿⠿⠟⡻⠀⢸⠀⢸⡇⠀⡇⠀⢸⠀⠀
⠀⠀⡇⢀⠇⠀⠈⣇⠀⢹⠀⠀⣆⠀⡄⠀⣨⠿⠿⢿⣿⣷⣆⣽⠃⠘⣿⣴⣴⣿⡿⠿⠿⢇⠀⢠⢄⣰⠃⠀⡎⠀⣸⠁⠀⠸⡀⢸⠀⠀
⠀⠀⣇⣼⠀⠀⠀⣿⠀⠈⡄⠀⠸⡄⠃⠰⠁⠀⣴⡾⠘⣿⠛⠟⠀⠀⠻⠿⣿⡇⢷⣤⣄⠈⢇⢸⢀⠇⠀⢀⠃⠀⣿⠀⠀⠀⣧⣸⡇⠀
⠀⠀⡿⢹⠀⠀⠀⡿⡇⠀⢡⠀⠀⢹⣗⣿⢠⣿⣿⡇⠀⡇⠀⠀⠀⠀⠀⠀⢸⠁⢸⣿⣼⡄⣺⢾⡟⠀⠀⡜⠀⢰⢿⠀⠀⠀⡟⠻⠇⠀
⠀⠀⠀⠘⡆⠀⠀⠁⠸⠀⠀⡆⠀⠈⢿⠹⠛⠛⠿⣷⣀⡇⠀⠀⠀⠀⠀⠀⢸⡄⣼⠿⠏⠛⠟⡿⠁⠀⢰⠁⠀⡎⢸⠀⠀⠀⡇⠀⠀⠀
⠀⠀⠀⠀⡇⠀⠀⠀⠀⢧⠀⠸⡀⠀⠈⢇⠀⠀⠀⠙⣿⡁⠀⠀⠀⠀⠀⠀⠀⣿⠏⠀⠀⠀⣰⠃⠀⢀⠏⠀⡸⠀⢸⠀⠀⢸⠁⠀⠀⠀
⠀⠀⠀⠀⣧⠀⠀⠆⠀⠘⡆⠀⢣⠀⠀⠘⡆⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⢠⠇⠀⠀⡼⠀⢰⠃⠀⢸⠀⠀⣸⠀⠀⠀⠀
⠀⠀⠀⠀⢹⠀⠀⡇⠀⠀⠸⡄⠈⡆⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⠀⠀⢠⠃⢀⠏⠀⠀⢸⠀⠀⡏⠀⠀⠀⠀
⠀⠀⠀⠀⠈⣆⢸⣧⠀⠀⠀⠱⡀⠸⡄⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⢀⠇⠀⡞⠀⠀⠀⣼⡇⢰⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣾⠈⢧⠀⠀⠀⢡⠀⠹⣄⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⢠⡎⠀⡜⠀⠀⠀⡰⠁⣧⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠉⠀⠈⢣⡀⠀⠀⢇⠀⢻⣦⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣇⡰⡿⠀⠰⠁⠀⢀⡜⠁⠀⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡄⠀⠸⡄⠈⡆⠙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⢡⠁⢀⠇⠀⢠⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⠀⢣⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⠀⡜⠀⣠⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢆⠘⡟⠲⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠗⢺⠃⡰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

# ──────────────────────────────────────────────────────────
# CONFIGURATION
#────────────────────────────────────────────────────────────


print(BANNER)
# PUT MULTIPLE TOKENS HERE — one per line
TOKENS = [
    "MTM5OTE1NjQ5MTY1ODk4OTc1Mg.GYAhPL.6jtRe6C4jS4Oj9J8JpDiIJivk4IhAEXeAldi9Q",
    # Add more tokens here, I recommend you to use atleast ten, buy tokens its cheap as fuck..
]

GUILD_ID = "1379444359505641542"
CHANNEL_ID = "1379447064894767134"
MESSAGE_ID = "1483214816398016512"
NUM_REPORTS = 5  # Total reports across all tokens

# CORRECTED breadcrumbs based on your fetch output:
# "Abuse or harassment" → "Verbally harassing me or someone else"
# You can check every reporting breadcrumb on github, scroll down and usually you would find it
BREADCRUMBS = [7, 76, 101]

VERSION = "1.0"
VARIANT = "latest"
LANGUAGE = "en"

# Threading - use 1 token per thread
MAX_WORKERS = min(5, len(TOKENS))

BASE_URL = "https://discord.com"
API_ENDPOINT = "/api/v9/reporting/message"
MENU_ENDPOINT = "/api/v9/reporting/menu/message"

def build_headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://discord.com",
        "Referer": "https://discord.com/channels/@me",
        "X-Discord-Locale": "en",
        "X-Debug-Options": "bugReporterEnabled",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

def fetch_menu(token):
    """Fetch the report menu tree."""
    url = f"{BASE_URL}{MENU_ENDPOINT}"
    try:
        resp = requests.get(url, headers=build_headers(token), timeout=15)
        if resp.status_code == 200:
            return resp.json()
        print(f"[!] Menu fetch failed: HTTP {resp.status_code}")
        return None
    except Exception as e:
        print(f"[!] Menu fetch error: {e}")
        return None

def send_report(token, payload):
    """Send a single report."""
    url = f"{BASE_URL}{API_ENDPOINT}"
    try:
        resp = requests.post(url, headers=build_headers(token), json=payload, timeout=15)
        return resp
    except Exception as e:
        return type("Resp", (), {"status_code": 0, "text": str(e)})()

def worker(token, token_index, reports_to_send, payload, results):
    """Worker function for each token thread."""
    success = 0
    fail = 0
    rate_limited_until = 0

    for i in range(reports_to_send):
        now = time.time()
        if now < rate_limited_until:
            wait = rate_limited_until - now
            print(f"  [Token {token_index}] Waiting {wait:.0f}s (rate limited until {datetime.fromtimestamp(rate_limited_until).strftime('%H:%M:%S')})")
            time.sleep(min(wait, 5))
            if time.time() < rate_limited_until:
                continue

        if i > 0:
            time.sleep(random.uniform(2.0, 5.0))

        resp = send_report(token, payload)

        if resp.status_code in (200, 201, 204):
            success += 1
            try:
                rid = resp.json().get("report_id", "N/A")
                print(f"  [Token {token_index}][{i+1}/{reports_to_send}] ✓ ID: {rid}")
            except:
                print(f"  [Token {token_index}][{i+1}/{reports_to_send}] ✓ (status {resp.status_code})")

        elif resp.status_code == 429:
            try:
                retry_after = resp.json().get("retry_after", 60)
            except:
                retry_after = 60

            print(f"  [Token {token_index}][{i+1}/{reports_to_send}] ✗ 429 — retry_after={retry_after}s")

            if retry_after < 3600:
                # Retry once
                print(f"     Waiting {retry_after+1:.0f}s then retrying...")
                time.sleep(retry_after + 2)
                resp2 = send_report(token, payload)
                if resp2.status_code in (200, 201, 204):
                    success += 1
                    print(f"  [Token {token_index}][{i+1}/{reports_to_send}] ✓ Retry OK")
                else:
                    fail += 1
                    print(f"  [Token {token_index}][{i+1}/{reports_to_send}] ✗ Retry failed: {resp2.status_code}")
                    # Mark this token as rate-limited for a while
                    rate_limited_until = time.time() + retry_after
            else:
                print(f"     Retry time too long, marking token as rate-limited")
                rate_limited_until = time.time() + retry_after

        elif resp.status_code == 401:
            print(f"  [Token {token_index}] ✗ 401 — Token invalid, removing from rotation")
            return success, fail, False  # signal token dead
        else:
            fail += 1
            print(f"  [Token {token_index}][{i+1}/{reports_to_send}] ✗ {resp.status_code} — {resp.text[:200]}")

    return success, fail, True

def main():

    if not TOKENS:
        print("[!] No tokens configured!")
        sys.exit(1)

    # Verify menu with first token
    print("[*] Fetching report menu to verify structure...")
    menu = fetch_menu(TOKENS[0])
    if not menu:
        print("[!] Could not fetch menu. Check your first token.")
        sys.exit(1)

    print(f"  [+] Menu fetched! root_node_id={menu.get('root_node_id')}, variant={menu.get('variant')}")
    print(f"  [+] Using breadcrumbs: {BREADCRUMBS}")

    # Build payload
    payload = {
        "version": VERSION,
        "variant": VARIANT,
        "name": "message",
        "language": LANGUAGE,
        "breadcrumbs": BREADCRUMBS,
        "guild_id": GUILD_ID,
        "channel_id": CHANNEL_ID,
        "message_id": MESSAGE_ID,
    }

    # Try to discover elements along breadcrumb path
    nodes = menu.get("nodes", {})
    for node_id in BREADCRUMBS:
        node = nodes.get(str(node_id))
        if node:
            print(f"  [+] Node {node_id}: key={node.get('key','?')}, header={node.get('header','?')}")
            elements = node.get("elements", [])
            for elem in elements:
                if elem.get("type") in ("checkbox", "select", "multi_select"):
                    options = elem.get("options", [])
                    if options:
                        val = options[0].get("value", options[0].get("name", ""))
                        payload.setdefault("elements", {})[elem["name"]] = [[val]]
                        print(f"      -> element '{elem['name']}' = [[\"{val}\"]]")
        else:
            print(f"  [!] Node {node_id} NOT FOUND in menu tree!")

    print(f"\n[*] Final payload:\n{json.dumps(payload, indent=2)}")

    # Distribute reports across tokens
    active_tokens = len(TOKENS)
    reports_per_token = max(1, NUM_REPORTS // active_tokens)
    remainder = NUM_REPORTS % active_tokens

    print(f"\n[*] Starting: {NUM_REPORTS} reports across {active_tokens} tokens\n")

    all_results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for idx, token in enumerate(TOKENS):
            count = reports_per_token + (1 if idx < remainder else 0)
            if count > 0:
                futures.append(executor.submit(worker, token, idx+1, count, payload, all_results))

        for future in as_completed(futures):
            try:
                result = future.result()
                all_results.append(result)
            except Exception as e:
                print(f"[!] Worker exception: {e}")

    # Summary
    total_success = sum(r[0] for r in all_results if r)
    total_fail = sum(r[1] for r in all_results if r)

    print(f"\n{'='*60}")
    print(f"  DONE — {total_success} successful / {total_fail} failed / {NUM_REPORTS} total")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()