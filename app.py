from pyrogram import Client, filters
from flask import Flask
from threading import Thread
import requests
import os

# =========================
# TELEGRAM CONFIG
# =========================

API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"


# =========================
# WEBSITE DOMAIN
# =========================
RENDER_URL = "https://two-0-uzcf.onrender.com"

# =========================
# START BOT
# =========================

bot = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================
# FLASK APP
# =========================

app = Flask(__name__)

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    return """

    <html>

    <head>

    <title>Stream Bot</title>

    <meta name="viewport"
    content="width=device-width, initial-scale=1.0">

    <style>

    body{
        background:#050018;
        color:white;
        font-family:Arial;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
        margin:0;
        text-align:center;
    }

    h1{
        font-size:35px;
    }

    </style>

    </head>

    <body>

    <div>

    <h1>✅ Bot Running Successfully</h1>

    </div>

    </body>

    </html>

    """

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"

    response = requests.get(url).json()

    if not response["ok"]:

        return "❌ File Not Found"

    file_path = response["result"]["file_path"]

    stream_link = (
        f"https://api.telegram.org/file/bot"
        f"{BOT_TOKEN}/{file_path}"
    )

    mx = (
        f"intent:{stream_link}"
        f"#Intent;type=video/*;"
        f"package=com.mxtech.videoplayer.ad;end"
    )

    vlc = (
        f"intent:{stream_link}"
        f"#Intent;type=video/*;"
        f"package=org.videolan.vlc;end"
    )

    return f"""

    <!DOCTYPE html>

    <html>

    <head>

    <meta charset="UTF-8">

    <meta name="viewport"
    content="width=device-width, initial-scale=1.0">

    <title>Video Player</title>

    <style>

    body{{
        margin:0;
        padding:20px;
        background:#050018;
        color:white;
        font-family:Arial;
        text-align:center;
    }}

    h1{{
        margin-bottom:20px;
    }}

    video{{
        width:100%;
        max-width:900px;
        border-radius:20px;
        background:black;
    }}

    .btn{{
        display:block;
        margin:15px auto;
        width:90%;
        max-width:350px;
        padding:15px;
        border-radius:14px;
        text-decoration:none;
        color:white;
        font-size:18px;
        font-weight:bold;
    }}

    .download{{
        background:#6c4cff;
    }}

    .mx{{
        background:#00b894;
    }}

    .vlc{{
        background:#ff3838;
    }}

    </style>

    </head>

    <body>

    <h1>🎬 Video Player</h1>

    <video controls autoplay>

        <source src="{stream_link}" type="video/mp4">

    </video>

    <a class="btn download"
    href="{stream_link}">
    ⬇ Download
    </a>

    <a class="btn mx"
    href="{mx}">
    ▶ MX Player
    </a>

    <a class="btn vlc"
    href="{vlc}">
    ▶ VLC Player
    </a>

    </body>

    </html>

    """

# =========================
# BOT MESSAGE
# =========================

@bot.on_message(filters.video | filters.document)
async def generate_link(client, message):

    media = message.video or message.document

    file_id = media.file_id

    link = f"{DOMAIN}/watch/{file_id}"

    await message.reply_text(

        f"✅ Link Generated Successfully\n\n🎬 {link}"

    )

# =========================
# RUN FLASK
# =========================

def run_web():

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )

# =========================
# START BOTH
# =========================

if __name__ == "__main__":

    Thread(target=run_web).start()

    print("✅ Website Started")

    bot.run()
