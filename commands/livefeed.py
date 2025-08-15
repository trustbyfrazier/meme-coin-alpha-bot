from core.persistence import load_seen_tokens
from core.logger import log

def send_livefeed(bot, message):
    tokens = load_seen_tokens()
    if tokens:
        feed_message = "<b>🟢 Live 'Almost Graduating' Tokens:</b>\n\n"
        for token in tokens:
            feed_message += f"🔹 <code>{token}</code>\n"
    else:
        feed_message = "⚠️ No tokens tracked yet."

    bot.send_message(chat_id=message.chat.id, text=feed_message, parse_mode='HTML')
    log("Sent /livefeed response.")

