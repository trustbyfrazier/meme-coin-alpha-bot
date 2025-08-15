import asyncio
from core.researcher import research_token
from core.assembler import assemble_message
from core.sender import send_message_with_image
from core.logger import log

def manual_research(bot, message):
    try:
        # Extract CA from message text
        parts = message.text.strip().split()
        if len(parts) < 2:
            bot.send_message(chat_id=message.chat.id, text="❌ Please provide a Contract Address.\nUsage: /research <CA>")
            return
        
        token_id = parts[1]
        bot.send_message(chat_id=message.chat.id, text=f"🔍 Starting research for:\n<code>{token_id}</code>", parse_mode='HTML')

        # Run async research in a new thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        token_data = loop.run_until_complete(research_token(token_id))

        # Assemble and Send
        message_text = assemble_message(token_data)
        image_url = token_data.get("asset", {}).get("icon", "")

        send_message_with_image(bot, message.chat.id, message_text, image_url)
        log(f"Sent manual research result for token: {token_id}")

    except Exception as e:
        log(f"Manual research failed: {e}")
        bot.send_message(chat_id=message.chat.id, text=f"❌ Research failed for {token_id}")

