import requests
from config import JUP_ALMOST_GRADUATING_URL
from core.logger import log, error_log
from core.persistence import load_seen_tokens, save_seen_token
from core import researcher  # ✅ Import the researcher module

def fetch_new_tokens():
    seen_tokens = load_seen_tokens()
    new_tokens = []

    payload = {
        "recent": {"timeframe": "24h"},
        "graduated": {"timeframe": "24h"},
        "aboutToGraduate": {"timeframe": "24h", "minHolderCount": 20, "minTokenAge": 9}
    }

    # ✅ Browser-like headers for stealth
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://jup.ag",
        "Referer": "https://jup.ag/"
    }

    try:
        response = requests.post(JUP_ALMOST_GRADUATING_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        pools = data.get("aboutToGraduate", {}).get("pools", [])
        log(f"Fetched {len(pools)} tokens from API.")

        for token in pools:
            token_id = token.get("id")
            if token_id and token_id not in seen_tokens:
                log(f"New token found: {token_id}")
                new_tokens.append(token_id)
                save_seen_token(token_id)

                # ✅ Trigger researcher immediately after saving
                log(f"Researching token: {token_id}")
                try:
                    researcher.run_research(token_id)
                except Exception as e:
                    error_log(f"Research failed for {token_id}: {e}")
            else:
                log(f"Duplicate token skipped: {token_id}")

    except Exception as e:
        error_log(f"Failed to fetch tokens: {e}")

    return new_tokens

