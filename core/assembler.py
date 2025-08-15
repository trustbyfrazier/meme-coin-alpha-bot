from jinja2 import Template
import os

TEMPLATE_FILE = 'templates/message_template.jinja2'

def _format_created_at(created_at: str) -> str:
    """Turn ISO 'YYYY-MM-DDTHH:MM:SSZ' into 'YYYY-MM-DD | HH:MM:SS' without parsing libs."""
    if not created_at or not isinstance(created_at, str):
        return ""
    return created_at.replace('T', ' | ').replace('Z', '')

def _normalize_bonding_curve(raw):
    """
    Jupiter sometimes returns bondingCurve as a fraction (0..1) and sometimes as a percent (>1).
    If <= 1 => treat as fraction -> *100; if > 1 => assume already percent.
    """
    try:
        val = float(raw or 0)
    except (TypeError, ValueError):
        val = 0.0
    if val <= 1:
        val = val * 100.0
    return round(val, 2)

def assemble_message(token_data):
    with open(TEMPLATE_FILE, 'r') as file:
        template = Template(file.read())

    # Ensure None mcaps in similar_coins are defaulted to 0 (prevents int(None) errors in template)
    similar_coins = token_data.get("similar_coins", []) or []
    for coin in similar_coins:
        if coin.get("mcap") is None:
            coin["mcap"] = 0

        # (optional) keep createdAt as-is for similar coins; user didn't request reformat there

    # Extract necessary fields for rendering
    asset = token_data.get("asset", {}) or {}

    # Normalize / format fields
    mcap_val = asset.get("mcap", 0) or 0
    bonding_curve_pct = _normalize_bonding_curve(asset.get("bondingCurve"))
    organic_score_rounded = round(float(asset.get("organicScore") or 0), 2)
    created_at_fmt = _format_created_at(asset.get("firstPool", {}).get("createdAt", ""))

    return template.render(
        int=int,   # allow int() in template if needed
        float=float,
        icon=asset.get("icon", "") or "",
        name=asset.get("name", "Unknown") or "Unknown",
        symbol=asset.get("symbol", "N/A") or "N/A",
        mcap=int(mcap_val),
        id=token_data.get("id", "") or "",
        bondingCurvePct=bonding_curve_pct,
        summary=token_data.get("narrative", "") or "",
        createdAt=created_at_fmt,
        twitter=asset.get("twitter", "") or "",
        website=asset.get("website", "") or "",
        telegram=asset.get("telegram", "") or "",
        reddit=asset.get("reddit", "") or "",
        tiktok=asset.get("tiktok", "") or "",
        launchpad=asset.get("launchpad", "") or "",
        holderCount=asset.get("holderCount", 0) or 0,
        organicScore=organic_score_rounded,
        similarCoins=similar_coins
    )

