from pyrogram import Client, filters
from flask import Flask, render_template_string
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
# BOT
# =========================

bot = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================
# FLASK
# =========================

app = Flask(__name__)

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return "Bot Running Successfully"

# =========================
# BOT MESSAGE
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    media = message.video or message.document

    file_id = media.file_id

    RENDER_URL = "https://two-0-uzcf.onrender.com"

   
link = f"{DOMAIN}/watch/{file_id}"

    await message.reply_text(
        f"✅ Uploaded Successfully\n\n🎬 Link:\n{link}"
    )

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    try:

        file = bot.get_messages("me", 1)

        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        ).json()

        if not file_info["ok"]:
            return "File Not Found"

        file_path = file_info["result"]["file_path"]

        stream_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        mx = f"intent:{stream_link}#Intent;type=video/*;package=com.mxtech.videoplayer.ad;end"

        vlc = f"intent:{stream_link}#Intent;type=video/*;package=org.videolan.vlc;end"

        html = f"""

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
            background:#050018;
            color:white;
            font-family:Arial;
            text-align:center;
            padding:20px;
        }}

        h1{{
            font-size:22px;
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
            width:90%;
            max-width:400px;
            margin:15px auto;
            padding:16px;
            border-radius:14px;
            text-decoration:none;
            font-size:18px;
            font-weight:bold;
            color:white;
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

        <h1>Secure Video Access</h1>

        <video controls autoplay>

            <source src="{stream_link}" type="video/mp4">

        </video>

        <a class="btn download"
        href="{stream_link}">
        ⬇ Download
        </a>

        <a class="btn mx"
        href="{mx}">
        ▶ Play In MX Player
        </a>

        <a class="btn vlc"
        href="{vlc}">
        ▶ Play In VLC
        </a>

        </body>
        </html>

        """

        return render_template_string(html)

    except Exception as e:
        return f"ERROR : {e}"

# =========================
# RUN
# =========================

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":

    Thread(target=run_flask).start()

    print("Bot Started")

    bot.run()
