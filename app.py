from pyrogram import Client, filters
from flask import Flask
from threading import Thread
import requests
import os

API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"


RENDER_URL = "https://two-0-uzcf.onrender.com"

# PUBLIC CHANNEL USERNAME
CHANNEL = "@cm4umovies"

bot = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

app = Flask(__name__)

@app.route("/")
def home():
    return "CM4U STREAM RUNNING"

# =========================
# SAVE MOVIE
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    try:

        # FORWARD TO CHANNEL
        forwarded = await message.forward(CHANNEL)

        # MESSAGE ID
        msg_id = forwarded.id

        # LINK
        link = f"{RENDER_URL}/watch/{msg_id}"

        await message.reply_text(
            f"✅ Uploaded Successfully\n\n🎬 {link}"
        )

    except Exception as e:

        await message.reply_text(f"ERROR : {e}")

# =========================
# WATCH
# =========================

@app.route("/watch/<msg_id>")
def watch(msg_id):

    try:

        # GET MESSAGE
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

        data = requests.get(url).json()

        file_id = None

        for update in data["result"]:

            msg = update.get("channel_post")

            if msg and str(msg["message_id"]) == str(msg_id):

                if "video" in msg:
                    file_id = msg["video"]["file_id"]

                elif "document" in msg:
                    file_id = msg["document"]["file_id"]

        if not file_id:
            return "❌ File Not Found"

        # GET FILE
        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
            params={"file_id": file_id}
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

        return f"""

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{{
background:#050018;
color:white;
font-family:Arial;
padding:20px;
text-align:center;
}}

video{{
width:100%;
border-radius:20px;
background:black;
}}

.btn{{
display:block;
margin-top:15px;
padding:15px;
border-radius:15px;
text-decoration:none;
color:white;
font-weight:bold;
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

<a class="btn download" href="{stream_link}">
⬇ Download
</a>

<a class="btn mx" href="{mx}">
▶ MX Player
</a>

<a class="btn vlc" href="{vlc}">
▶ VLC Player
</a>

</body>

</html>

"""

    except Exception as e:
        return f"ERROR : {e}"

# =========================
# RUN
# =========================

def run_flask():

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )

if __name__ == "__main__":

    Thread(target=run_flask).start()

    print("✅ BOT STARTED")

    bot.run()
