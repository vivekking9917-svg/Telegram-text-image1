import os
import io
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import google.generativeai as genai

# =============================
# ENVIRONMENT VARIABLES
# =============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ⚠️ Apna Telegram user_id yahan daalo
ALLOWED_USERS = [7449498833]  # ← CHANGE THIS

# =============================
# GEMINI CONFIG
# =============================
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro")

# =============================
# COMMAND: /start
# =============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ Sorry bhai, ye private bot hai.")
        return

    await update.message.reply_text(
        "👋 Welcome bhai!\n\n"
        "Bas koi bhi text bhejo 👇\n"
        "🎨 Main usse image bana dunga"
    )

# =============================
# IMAGE GENERATOR
# =============================
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return

    prompt = update.message.text
    await update.message.reply_text("⏳ Image generate ho rahi hai...")

    try:
        response = model.generate_content(prompt)

        image_data = (
            response.candidates[0]
            .content.parts[0]
            .inline_data.data
        )

        image_bytes = io.BytesIO(image_data)
        image_bytes.name = "image.png"

        await update.message.reply_photo(photo=image_bytes)

    except Exception as e:
        await update.message.reply_text(
            "❌ Error aa gaya bhai 😢\n"
            f"{e}"
        )

# =============================
# MAIN APP
# =============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image)
    )

    print("🤖 Bot successfully start ho gaya...")
    app.run_polling()

if __name__ == "__main__":
    main()