import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
logging.basicConfig(level=logging.INFO)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
print("TOKEN:", TOKEN)

LINKS = [
    ("🌐 WEBSITE", "https://bio.site/lotusprivate.com"),
    ("🌐 SPONSORLAR", "https://bio.site/lotussiteler.com"),
    ("📣 TELEGRAM ANA KANAL", "https://t.me/lotusprivate"),
    ("📣 ÇEKİLİŞ KANALI", "https://t.me/lotusprivatelive"),
]

WELCOME_TEXT = (
    "✨ *Lotus Private'a Hoş Geldin!* ✨\n\n"
    "Aşağıdaki bağlantılardan web sitelerimize ve Telegram kanallarımıza ulaşabilirsin 👇\n\n"
    "🌐 *Web Sitelerimiz*\n"
    "• Lotus Private\n"
    "• Sponsorlar\n\n"
    "📣 *Telegram Kanallarımız*\n"
    "• Ana Kanal\n"
    "• Çekiliş Kanalı\n\n"
    "💎 Keyifli vakit geçirmen dileğiyle."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, url=url)] for name, url in LINKS]
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN bulunamadı. Render/Terminal env var olarak eklemelisin.")

    threading.Thread(target=run_web_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()

