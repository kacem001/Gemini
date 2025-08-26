import os
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# قراءة المتغيرات من Environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://gemini.googleapis.com/v1beta2/assistants:generateMessage"

# دالة للتفاعل مع Gemini API
def ask_gemini(prompt, conversation_id=None):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "conversation_id": conversation_id
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        resp_json = response.json()
        message = resp_json.get('message', {}).get('content', 'لم يتم استرجاع أي رد')
        return message
    except requests.exceptions.RequestException as e:
        return f"حدث خطأ عند الاتصال بـ Gemini API: {e}"

# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أنا بوت Gemini الشخصي. أرسل لي أي رسالة للتجربة.")

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = ask_gemini(user_text)
    await update.message.reply_text(reply)

# تشغيل البوت
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("بوت تلغرام Gemini يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
