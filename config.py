import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# API Endpoints
JUP_ALMOST_GRADUATING_URL = "https://datapi.jup.ag/v1/pools/gems"
JUP_ASSET_SEARCH_URL = "https://datapi.jup.ag/v1/assets/search"
JUP_NARRATIVE_URL = "https://datapi.jup.ag/v1/chaininsight/narrative"

# Bot Intervals
FETCH_INTERVAL_SECONDS = int(os.getenv("FETCH_INTERVAL_SECONDS", 5))

# Data Paths
SEEN_TOKENS_FILE = "data/seen_tokens.json"

