# 🌐 Multilingual Telegram Translator Bot

This is a Telegram bot that translates messages in groups and private chats into a user's preferred language. Built using `python-telegram-bot` and `deep-translator`.

---

## 🚀 Features

- ✅ **/start**: See instructions
- ✅ **/lang `<language>`**: Set preferred language for auto-translation
- ✅ **/translate `<language>` `<text>`**: Instant translation
- ✅ **/translate `<language>`** (reply to a message): Translates replied message
- ✅ **/setlang**: Choose from a list of popular languages with buttons
- ✅ **Group Support**: Translates group messages privately to subscribed users
- ✅ **Private Chat Support**: Translates messages directly in private chats

---

## 🧪 Example

/lang hindi

/translate french How are you?

/translate german (as a reply to a message)


---

## 🌍 Supported Languages

Supports all languages listed by Google Translate (via `deep_translator`). For example: `english`, `hindi`, `french`, `german`, `telugu`, `tamil`, `oriya`, etc.

Use `/start` to see full supported list.

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
