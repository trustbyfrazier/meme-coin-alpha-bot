import telebot
import threading
import time
import asyncio
import os
import logging
from dotenv import load_dotenv
from config import TELEGRAM_BOT_TOKEN, FETCH_INTERVAL_SECONDS
from core.fetcher import fetch_new_tokens
from core.researcher import research_token
from core.assembler import assemble_message
from core.sender import send_message_with_image
from core.logger import log, error_log
from commands import livefeed, research_manual, status

# =========================
# LOGGING CONFIG
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Load environment variables
load_dotenv()

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Global Runtime Trackers
start_time = time.time()
last_fetch_time = None
CHAT_ID = os.getenv("CHAT_ID")  # <-- Pulled from .env now

# =========================
# COMMAND HANDLERS
# =========================
@bot.message_handler(commands=['livefeed'])
def handle_livefeed(message):
    livefeed.send_livefeed(bot, message)

@bot.message_handler(commands=['research'])
def handle_manual_research(message):
    research_manual.manual_research(bot, message)

@bot.message_handler(commands=['status'])
def handle_status(message):
    global last_fetch_time
    status.send_status(bot, message, start_time, last_fetch_time)

# =========================
# TOKEN PROCESS PIPELINE
# =========================
async def process_token(token_id):
    try:
        log(f"🔍 Starting research for {token_id}")
        token_data = await research_token(token_id)

        if not token_data or not token_data.get("asset"):
            error_log(f"❌ Research returned no data for {token_id}")
            return

        log(f"🛠 Assembling message for {token_id}")
        message_text = assemble_message(token_data)
        image_url = token_data.get("asset", {}).get("icon", "")

        if not message_text:
            error_log(f"❌ Failed to assemble message for {token_id}")
            return

        if CHAT_ID:
            log(f"📤 Sending token {token_id} to Telegram...")
            send_message_with_image(bot, CHAT_ID, message_text, image_url)
            log(f"✅ Token {token_id} sent successfully.")
        else:
            error_log("⚠️ CHAT_ID is not set. Message not sent.")

    except Exception as e:
        error_log(f"Pipeline error for {token_id}: {e}")

# =========================
# AUTO FETCH LOOP
# =========================
def fetch_loop():
    global last_fetch_time
    while True:
        try:
            log("🚀 Starting fetch cycle...")
            new_tokens = fetch_new_tokens()
            last_fetch_time = time.time()

            if new_tokens:
                log(f"📦 {len(new_tokens)} new token(s) found. Processing...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(
                    asyncio.gather(*(process_token(token_id) for token_id in new_tokens))
                )
            else:
                log("ℹ️ No new tokens this cycle.")

        except Exception as e:
            error_log(f"❌ Fetch loop encountered an error: {e}")

        time.sleep(FETCH_INTERVAL_SECONDS)

# =========================
# BOT STARTER WITH RESTART LOOP
# =========================
def start_bot():
    while True:
        try:
            log("🤖 Bot is up and running...")
            # Start Fetch Loop in a Thread
            fetch_thread = threading.Thread(target=fetch_loop)
            fetch_thread.daemon = True
            fetch_thread.start()

            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            logging.error(f"❌ Bot crashed due to: {e}", exc_info=True)
            logging.info("♻️ Restarting in 5 seconds...")
            time.sleep(5)

# =========================
# MAIN ENTRY
# =========================
if __name__ == "__main__":
    start_bot()

