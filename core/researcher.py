import aiohttp
import asyncio
from config import JUP_ASSET_SEARCH_URL, JUP_NARRATIVE_URL
from core.logger import log, error_log

# Browser-like headers to bypass 403
STEALTH_HEADERS = {
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

async def fetch_json(session, url):
    try:
        async with session.get(url, headers=STEALTH_HEADERS) as response:
            response.raise_for_status()
            return await response.json()
    except Exception as e:
        error_log(f"Failed to fetch {url}: {e}")
        return {}

async def research_token(token_id):
    async with aiohttp.ClientSession(headers=STEALTH_HEADERS) as session:
        # 1. Asset Search by CA
        asset_url = f"{JUP_ASSET_SEARCH_URL}?query={token_id}"
        asset_response = await fetch_json(session, asset_url)

        asset_data = {}
        if isinstance(asset_response, list) and len(asset_response) > 0:
            token_info = asset_response[0]  # Assuming first match is the token we want
            asset_data = {
                "id": token_info.get("id"),
                "name": token_info.get("name"),
                "symbol": token_info.get("symbol"),
                "icon": token_info.get("icon"),
                "twitter": token_info.get("twitter"),
                "website": token_info.get("website"),
                "telegram": token_info.get("telegram"),
                "reddit": token_info.get("reddit"),
                "tiktok": token_info.get("tiktok"),
                "launchpad": token_info.get("launchpad"),
                "holderCount": token_info.get("holderCount"),
                "organicScore": token_info.get("organicScore"),
                "mcap": token_info.get("mcap"),
                "bondingCurve": token_info.get("bondingCurve"),
                "firstPool": {
                    "createdAt": token_info.get("firstPool", {}).get("createdAt")
                }
            }
        else:
            error_log(f"No asset data found for token ID: {token_id}")

        # 2. Narrative Summary
        narrative_url = f"{JUP_NARRATIVE_URL}/{token_id}"
        narrative_response = await fetch_json(session, narrative_url)
        narrative_text = narrative_response.get("narrative", "No summary available.")

        # 3. Similar Coins Search (using symbol from asset_data)
        similar_coins_data = []
        symbol = asset_data.get("symbol")
        if symbol:
            similar_url = f"{JUP_ASSET_SEARCH_URL}?query={symbol}&limit=10"
            similar_response = await fetch_json(session, similar_url)
            if isinstance(similar_response, list):
                for token in similar_response:
                    if token.get("id") != token_id:
                        similar_coins_data.append({
                            "id": token.get("id"),
                            "createdAt": token.get("firstPool", {}).get("createdAt"),
                            "mcap": token.get("mcap")
                        })

        # Consolidate Research Result
        token_info = {
            "id": token_id,
            "asset": asset_data,
            "narrative": narrative_text,
            "similar_coins": similar_coins_data
        }

        log(f"Completed research for token: {token_id}")
        return token_info

# Wrapper for minimal changes
async def run_research(token_id):
    return await research_token(token_id)

