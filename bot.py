import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---- LINKLERİN ----
LINKS = [
    ("🌐 WEBSITE", "https://bio.site/lotusprivate.com"),
    ("🌐 SPONSORLAR", "https://bio.site/lotussiteler.com"),
    ("📣 TELEGRAM ANA KANAL", "https://t.me/lotusprivate"),
    ("📣 ÇEKİLİŞ KANALI", "https://t.me/lotusprivatelive"),
]

WELCOME_TEXT = "Merhaba! Aşağıdaki bağlantılardan web sitelerimize ve kanallarımıza ulaşabilirsin 👇"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, url=url)] for name, url in LINKS]
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )

# ---- RENDER için mini web server (PORT taraması geçsin diye) ----
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_web_server():
    port = int(os.getenv("PORT", "10000"))  # Render PORT verir
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN bulunamadı. Render > Environment'da BOT_TOKEN eklemelisin.")

    # Web server ayrı thread
    threading.Thread(target=run_web_server, daemon=True).start()

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    # Botu çalıştır
    app.run_polling()

if __name__ == "__main__":
    main()
