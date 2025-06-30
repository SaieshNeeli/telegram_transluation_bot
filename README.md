🌐 Multilingual Telegram Translator Bot
This Telegram bot allows users to automatically translate messages from group chats and private messages into their preferred language.
It’s built using python-telegram-bot and deep-translator.

✨ Features
✅ Private Chat Translation

Set a preferred language using /lang <language> or /setlang

All your messages will be translated automatically to your selected language

One-off translation: Use /translate <language> <text> for instant translation

✅ Group Message Translation

Add the bot to any group

Users can privately set their own preferred languages

The bot will listen to all group messages and send private translations to each user based on their chosen language

✅ Message Reply Translation

Reply to any message with /lang <language> or /translate <language> to translate that specific message

✅ Interactive Language Selection

Use /setlang to get an inline keyboard with popular language buttons

💬 Supported Commands
Command	Description
/start	Get started with the bot
/lang <language>	Set your preferred language or reply to a message to translate it
/translate <language> <text>	Instantly translate provided text or reply to a message
/setlang	Select language from interactive buttons

🛠️ Technologies Used
Python 3.10+

python-telegram-bot

deep-translator

httpx

asyncio

💡 Use Case Scenarios
🧑‍🤝‍🧑 Multilingual Teams: Automatically translate team discussions into each member's preferred language

🌍 International Communities: Help users communicate across languages in group chats

🧳 Travel Groups: Let users from different countries talk without needing manual translation

🚀 Getting Started (For Developers)
Clone the repository:

git clone https://github.com/SaieshNeeli/telegram-translate-bot.git
cd telegram-translate-bot
Install dependencies:

pip install -r requirements.txt
Create a .env file (optional) or replace TELEGRAM_BOT_TOKEN directly in main.py.

Run the bot:

python main.py
