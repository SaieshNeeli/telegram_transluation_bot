# 🌐 Multilingual Telegram Translator Bot

This Telegram bot allows users to **automatically translate messages** from **group chats** and **private messages** into their preferred language.  
It is built using **[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)** and **[deep-translator](https://github.com/nidhaloff/deep-translator)**.
The bot is created with the username @last_message_reply_bot. By seraching the bot with this username we can start the bot either in the bot chat or in the groups . it is very useful in community chatting groups . 

I have deployed this bot for 20 days from now . So it will be active for 20 days . The bot was deployed in railway.com . 
If you want to run this code on your system you can follow the below instruction and can run of your system or can directly deply the code in any deployment platforms.

---

## ✨ Features

### ✅ Private Chat Translation
- Set a preferred language using `/lang <language>` or `/setlang`
- All your messages will be translated automatically to your selected language
- One-off translation using:
  ```bash
  /translate <language> <text>
  
Group Message Translation
Add the bot to any Telegram group

Users can privately set their own language preference

The bot reads group messages and sends private translations based on user preferences

## Supported Commands
Command	Description
/start	Start the bot and view help
/lang <language>	Set preferred language OR translate a replied message
/translate <language> <text>	Translate provided text OR replied message
/setlang	Choose language via interactive buttons

## Technologies Used
✅ Python 3.10+

✅ python-telegram-bot

✅ deep-translator

✅ httpx

✅ asyncio

## Use Case Scenarios
👥 Multilingual Teams: Automatically translate messages for global team collaboration

🌎 International Communities: Break language barriers in active Telegram groups

✈️ Travel Groups: Enable seamless communication across different languages
## Getting Started (For Developers)
1. Clone the Repository

git clone https://github.com/SaieshNeeli/telegram-translate-bot.git
cd telegram-translate-bot
2. Install Dependencies

pip install -r requirements.txt
 Setup Environment (Optional)
You can either:

3.Create a .env file and store your token:

env
TELEGRAM_BOT_TOKEN=your_token_here
OR directly replace TELEGRAM_BOT_TOKEN in main.py
4. Run the Bot

python main.py
## Screenshots
 ![image](https://github.com/user-attachments/assets/506df24b-7c54-4e62-afd5-c75c59f3944d)
 ![image](https://github.com/user-attachments/assets/556c981b-30b4-48c2-b637-624bee804453)


