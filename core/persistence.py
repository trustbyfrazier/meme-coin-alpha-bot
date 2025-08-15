import json
import os
from config import SEEN_TOKENS_FILE
from core.logger import log, error_log

def load_seen_tokens():
    """Load the list of seen token IDs from the persistent storage."""
    if not os.path.exists(SEEN_TOKENS_FILE):
        log("Seen tokens file not found. Creating a new one.")
        return set()
    try:
        with open(SEEN_TOKENS_FILE, 'r') as f:
            tokens = json.load(f)
            return set(tokens)
    except json.JSONDecodeError:
        error_log("Seen tokens file is corrupted. Resetting it.")
        return set()
    except Exception as e:
        error_log(f"Failed to load seen tokens: {e}")
        return set()

def save_seen_token(token_id):
    """Add a token ID to the seen list and save it persistently."""
    tokens = load_seen_tokens()
    if token_id not in tokens:
        tokens.add(token_id)
        try:
            with open(SEEN_TOKENS_FILE, 'w') as f:
                json.dump(list(tokens), f, indent=4)
            log(f"Saved token ID: {token_id}")
        except Exception as e:
            error_log(f"Failed to save token ID: {e}")
    else:
        log(f"Token ID {token_id} already exists in seen tokens.")

def is_token_seen(token_id):
    """Check if a token ID has already been seen."""
    tokens = load_seen_tokens()
    return token_id in tokens

