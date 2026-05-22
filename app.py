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

CHANNEL_ID = -1003502272528

RENDER_URL = "https://two-0-uzcf.onrender.com"

# =========================
# BOT CREATE
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

    return "<h1>CM4U STREAM BOT RUNNING</h1>"

# =========================
# SAVE VIDEO
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    try:

        # CHANNEL MA FORWARD
        copied = await message.copy(
            chat_id=CHANNEL_ID
        )

        file_id = (
            copied.video.file_id
            if copied.video
            else copied.document.file_id
        )

        # LINK
        link = f"{RENDER_URL}/watch/{file_id}"

        await message.reply_text(
            f"✅ Uploaded Successfully\n\n🎬 Link:\n{link}"
        )

    except Exception as e:

        await message.reply_text(
            f"ERROR : {e}"
        )

# =========================
# WATCH
# =========================

@app.route("/watch/<path:file_id>")
def watch(file_id):

    try:

        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
            params={
                "file_id": file_id
            }
        ).json()

        if not file_info.get("ok"):

            return f"Telegram Error : {file_info}"

        file_path = file_info["result"]["file_path"]

        stream_link = (
            f"https://api.telegram.org/file/bot"
            f"{BOT_TOKEN}/{file_path}"
        )

        mx = (
            f"intent:{stream_link}"
            "#Intent;type=video/*;"
            "package=com.mxtech.videoplayer.ad;end"
        )

        vlc = (
            f"intent:{stream_link}"
            "#Intent;type=video/*;"
            "package=org.videolan.vlc;end"
        )

        return render_template_string(f"""

<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>CM4U STREAM</title>

<style>

body{{
margin:0;
padding:15px;
background:#050018;
font-family:Arial;
color:white;
text-align:center;
}}

video{{
width:100%;
border-radius:15px;
background:black;
}}

.btn{{
display:block;
padding:15px;
margin-top:12px;
border-radius:12px;
text-decoration:none;
font-weight:bold;
color:white;
}}

.download{{background:#6c4cff;}}
.mx{{background:#00b894;}}
.vlc{{background:#ff3838;}}

</style>

</head>

<body>

<h2>🎬 CM4U STREAM</h2>

<video controls autoplay>

<source src="{stream_link}">

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

""")

    except Exception as e:

        return f"ERROR : {e}"

# =========================
# RUN FLASK
# =========================

def run_flask():

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )

# =========================
# START
# =========================

if __name__ == "__main__":

    Thread(
        target=run_flask
    ).start()

    print("✅ BOT STARTED")

    bot.run()
