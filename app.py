from pyrogram import Client, filters
from flask import Flask
from threading import Thread
import os

# =====================
# CONFIG
# =====================

API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"


DOMAIN = "https://two-0-uzcf.onrender.com"

# =====================
# BOT
# =====================

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =====================
# FLASK
# =====================

app = Flask(__name__)

# =====================
# HOME
# =====================

@app.route("/")
def home():
    return "Bot Running"

# =====================
# WATCH
# =====================

@app.route("/watch/<file_id>")
def watch(file_id):

    stream = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"

    return f"""

    <html>

    <head>

    <meta name="viewport"
    content="width=device-width, initial-scale=1.0">

    <style>

    body{{
    background:#050018;
    color:white;
    font-family:Arial;
    text-align:center;
    padding:20px;
    }}

    video{{
    width:100%;
    border-radius:20px;
    }}

    a{{
    display:block;
    margin:15px auto;
    padding:15px;
    width:90%;
    max-width:350px;
    background:#6c4cff;
    color:white;
    text-decoration:none;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
    }}

    </style>

    </head>

    <body>

    <h1>Video Player</h1>

    <video controls autoplay>

    <source src="{stream}" type="video/mp4">

    </video>

    <a href="{stream}">
    ⬇ Download
    </a>

    </body>

    </html>

    """

# =====================
# BOT REPLY
# =====================

@bot.on_message(filters.video | filters.document)
async def video_handler(client, message):

    media = message.video or message.document

    file_id = media.file_id

    link = f"{DOMAIN}/watch/{file_id}"

    await message.reply_text(
        f"✅ Link Generated\n\n{link}"
    )

# =====================
# RUN
# =====================

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

bot.run()
