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
# DOMAIN
# =========================

RENDER_URL = "https://two-0-uzcf.onrender.com"

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
    return """

    <html>

    <head>

    <title>Stream Bot</title>

    <style>

    body{
        margin:0;
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
        background:#050018;
        color:white;
        font-family:Arial;
    }

    .box{
        background:rgba(255,255,255,0.08);
        backdrop-filter:blur(18px);
        padding:40px;
        border-radius:25px;
        border:1px solid rgba(255,255,255,0.1);
        box-shadow:0 0 30px rgba(108,76,255,0.4);
        text-align:center;
    }

    h1{
        font-size:35px;
    }

    p{
        color:#bbb;
    }

    </style>

    </head>

    <body>

    <div class="box">

    <h1>🎬 Stream Bot Running</h1>

    <p>Glass UI Streaming Server Active</p>

    </div>

    </body>

    </html>

    """

# =========================
# BOT MESSAGE
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    try:

        media = message.video or message.document

        file_id = media.file_id

        # GENERATE LINK
        link = f"{RENDER_URL}/watch/{file_id}"

        await message.reply_text(
            f"✅ Uploaded Successfully\n\n🎬 Link:\n{link}"
        )

    except Exception as e:

        await message.reply_text(f"ERROR : {e}")

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    try:

        # TELEGRAM FILE INFO
        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        ).json()

        if not file_info["ok"]:
            return "❌ File Not Found"

        file_path = file_info["result"]["file_path"]

        # STREAM LINK
        stream_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        # MX PLAYER LINK
        mx = f"intent:{stream_link}#Intent;type=video/*;package=com.mxtech.videoplayer.ad;end"

        # VLC PLAYER LINK
        vlc = f"intent:{stream_link}#Intent;type=video/*;package=org.videolan.vlc;end"

        # PREMIUM GLASS UI
        html = f"""

        <!DOCTYPE html>
        <html>

        <head>

        <meta charset="UTF-8">

        <meta name="viewport"
        content="width=device-width, initial-scale=1.0">

        <title>Premium Stream</title>

        <style>

        *{{
            margin:0;
            padding:0;
            box-sizing:border-box;
        }}

        body{{
            background:
            linear-gradient(135deg,#050018,#14003b,#240046);
            min-height:100vh;
            font-family:Arial;
            display:flex;
            justify-content:center;
            align-items:center;
            padding:20px;
            overflow:auto;
        }}

        .container{{
            width:100%;
            max-width:950px;

            background:rgba(255,255,255,0.08);

            backdrop-filter:blur(20px);

            border:1px solid rgba(255,255,255,0.1);

            border-radius:30px;

            padding:25px;

            box-shadow:
            0 0 40px rgba(108,76,255,0.35);
        }}

        h1{{
            text-align:center;
            color:white;
            margin-bottom:25px;
            font-size:30px;
        }}

        video{{
            width:100%;
            border-radius:20px;
            background:black;
            outline:none;
            box-shadow:
            0 0 25px rgba(0,0,0,0.5);
        }}

        .buttons{{
            margin-top:25px;
        }}

        .btn{{
            display:block;
            width:100%;
            text-align:center;
            padding:18px;
            margin-top:15px;
            border-radius:18px;
            text-decoration:none;
            color:white;
            font-size:18px;
            font-weight:bold;
            transition:0.3s;
        }}

        .btn:hover{{
            transform:scale(1.03);
        }}

        .download{{
            background:
            linear-gradient(45deg,#6c4cff,#8f6bff);
            box-shadow:
            0 0 20px rgba(108,76,255,0.5);
        }}

        .mx{{
            background:
            linear-gradient(45deg,#00b894,#00d2a0);
            box-shadow:
            0 0 20px rgba(0,184,148,0.4);
        }}

        .vlc{{
            background:
            linear-gradient(45deg,#ff3838,#ff5e57);
            box-shadow:
            0 0 20px rgba(255,56,56,0.4);
        }}

        .footer{{
            text-align:center;
            color:#bbb;
            margin-top:25px;
            font-size:14px;
        }}

        </style>

        </head>

        <body>

        <div class="container">

        <h1>🎬 Premium Video Stream</h1>

        <video controls autoplay>

        <source src="{stream_link}" type="video/mp4">

        </video>

        <div class="buttons">

        <a class="btn download"
        href="{stream_link}">
        ⬇ Download Video
        </a>

        <a class="btn mx"
        href="{mx}">
        ▶ Play In MX Player
        </a>

        <a class="btn vlc"
        href="{vlc}">
        ▶ Play In VLC Player
        </a>

        </div>

        <div class="footer">

        ⚡ Fast Streaming • Secure Access • Glass UI

        </div>

        </div>

        </body>

        </html>

        """

        return render_template_string(html)

    except Exception as e:

        return f"ERROR : {e}"

# =========================
# RUN FLASK
# =========================

def run_flask():

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )

# =========================
# START BOT
# =========================

if __name__ == "__main__":

    Thread(target=run_flask).start()

    print("✅ Premium Stream Bot Started")

    bot.run()
