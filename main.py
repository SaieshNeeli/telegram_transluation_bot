import nest_asyncio
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from deep_translator import GoogleTranslator

# Enable nested asyncio for Colab/Jupyter
nest_asyncio.apply()

# Set up logging
logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = "7578413491:AAGcWTkG_OezfWBQK9hbJNNnQDHyCDdYflM"

# User language preferences
user_langs = {}
users_warned = set()

# Aliases for better usability
LANGUAGE_ALIASES = {
    "oriya": "odia",
    "mandarin": "chinese (simplified)",
}

# Language support setup
translator_instance = GoogleTranslator(source='auto', target='english')
SUPPORTED_LANG_DICT = translator_instance.get_supported_languages(as_dict=True)
SUPPORTED_LANGUAGES = list(SUPPORTED_LANG_DICT.keys())
LANGUAGE_LIST_STRING = ", ".join(sorted(SUPPORTED_LANGUAGES))

POPULAR_LANGS = ["english", "hindi", "telugu", "tamil", "french", "german" , "odia (oriya)"]


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 I'm your translation bot!\n"
        "Use `/lang <language>` to get group messages translated privately.\n"
        "Or reply to a message with `/lang <language>` to translate just that message.\n"
        "Use `/translate <language> <text>` for quick translations.\n"
        "Use `/setlang` to pick a language from buttons.\n\n"
        f"Supported: `{LANGUAGE_LIST_STRING}`",
        parse_mode="Markdown"
    )


# /lang command
async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/lang <language>` or reply to a message with `/lang <language>`", parse_mode="Markdown")
        return

    lang_input = " ".join(context.args).strip().lower()
    lang_input = LANGUAGE_ALIASES.get(lang_input, lang_input)

    if lang_input not in SUPPORTED_LANG_DICT:
        await update.message.reply_text("❌ Invalid language. Use `/start` to see supported ones.")
        return

    lang_code = SUPPORTED_LANG_DICT[lang_input]
    user_id = update.effective_user.id

    if update.message.reply_to_message:
        original_text = update.message.reply_to_message.text
        if not original_text:
            await update.message.reply_text("⚠️ The replied message has no text to translate.")
            return
        try:
            translated = GoogleTranslator(source='auto', target=lang_code).translate(original_text)
            await update.message.reply_text(
                f"📤 *Translated Message:*\n`{translated}`",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"[ERROR] Translation failed: {e}")
            await update.message.reply_text("❌ Translation failed.")
        return

    # Set user preference
    user_langs[user_id] = lang_code
    await update.message.reply_text(f"✅ Your messages will be translated to **{lang_input}**.", parse_mode="Markdown")


# /translate <language> <text> OR reply to a message and use /translate <language>
async def quick_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/translate <language> <text>` or reply to a message with `/translate <language>`", parse_mode="Markdown")
        return

    lang_input = context.args[0].lower()
    lang_input = LANGUAGE_ALIASES.get(lang_input, lang_input)

    if lang_input not in SUPPORTED_LANG_DICT:
        await update.message.reply_text("❌ Invalid language.")
        return

    # Case 1: Translate replied message
    if update.message.reply_to_message and len(context.args) == 1:
        original_text = update.message.reply_to_message.text
        if not original_text:
            await update.message.reply_text("⚠️ The replied message has no text to translate.")
            return
        try:
            translated = GoogleTranslator(source='auto', target=SUPPORTED_LANG_DICT[lang_input]).translate(original_text)
            await update.message.reply_text(f"📤 *Translated Replied Message:*\n`{translated}`", parse_mode="Markdown")
        except Exception as e:
            print(f"[ERROR] Translation failed: {e}")
            await update.message.reply_text("❌ Translation failed.")
        return

    # Case 2: Translate user-provided text
    if len(context.args) >= 2:
        text_to_translate = " ".join(context.args[1:])
        try:
            translated = GoogleTranslator(source='auto', target=SUPPORTED_LANG_DICT[lang_input]).translate(text_to_translate)
            await update.message.reply_text(f"🌍 *Translated:* \n`{translated}`", parse_mode="Markdown")
        except Exception as e:
            print(f"[ERROR] Quick translation failed: {e}")
            await update.message.reply_text("❌ Translation failed.")
        return

    # Case 3: Invalid usage
    await update.message.reply_text("⚠️ Please provide text or reply to a message.", parse_mode="Markdown")

# /setlang inline buttons
async def choose_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(lang.title(), callback_data=lang)] for lang in POPULAR_LANGS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select your preferred language:", reply_markup=reply_markup)


# Inline button callback
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang_input = query.data.lower()
    await query.answer()

    user_id = query.from_user.id
    lang_code = SUPPORTED_LANG_DICT.get(lang_input)

    if not lang_code:
        await query.edit_message_text("❌ Unsupported language.")
        return

    user_langs[user_id] = lang_code
    await query.edit_message_text(f"✅ Language set to {lang_input.title()}.")


# Group message handler
async def group_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    sender_id = update.effective_user.id

    print(f"[LOG] Group message from {sender_id}: {message_text}")

    for user_id, lang_code in user_langs.items():
        if user_id == sender_id:
            continue

        try:
            translated = GoogleTranslator(source='auto', target=lang_code).translate(message_text)
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📥 *Translated from Group:*\n`{translated}`",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"[ERROR] Could not send to {user_id}: {e}")

    # Notify users without language set (only once)
    for member in update.message.new_chat_members or []:
        if member.id not in user_langs and member.id not in users_warned:
            await context.bot.send_message(
                chat_id=member.id,
                text="⚠️ Please set a preferred language using `/lang <language>` or `/setlang`."
            )
            users_warned.add(member.id)


# Private message handler
async def private_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_lang = user_langs.get(user_id)

    if not user_lang:
        await update.message.reply_text("⚠️ Please set your preferred language using `/lang <language>` or `/setlang`.")
        return

    try:
        translated = GoogleTranslator(source='auto', target=user_lang).translate(update.message.text)
        await update.message.reply_text(f"🌐 *Translated:* \n`{translated}`", parse_mode="Markdown")
    except Exception as e:
        print(f"[ERROR] Private translation failed: {e}")
        await update.message.reply_text("❌ Translation failed.")


# Run the bot
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lang", set_lang))
    app.add_handler(CommandHandler("translate", quick_translate))
    app.add_handler(CommandHandler("setlang", choose_lang))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, group_message_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, private_message_handler))

    print("✅ Bot is running...")
    await app.run_polling()


# Entry
try:
    asyncio.get_running_loop().run_until_complete(main())
except RuntimeError:
    asyncio.create_task(main())
