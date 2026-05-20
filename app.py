from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread

# =========================
# TELEGRAM CONFIG
# =========================

API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"

# =========================
# WEBSITE URL
# =========================

BASE_URL = "https://your-app-name.onrender.com"

# =========================
# BOT
# =========================

bot = Client(
    "moviebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================
# FLASK
# =========================

app = Flask(__name__)

# =========================
# STORE MOVIES
# =========================

movies = {}

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return """
    <h1 style='font-family:Arial;text-align:center;margin-top:50px'>
    ✅ Bot Running Successfully
    </h1>
    """

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    movie = movies.get(file_id)

    if not movie:
        return """
        <h1 style='color:red;text-align:center;font-family:Arial'>
        ❌ Movie Not Found
        </h1>
        """

    file_name = movie["name"]
    stream_link = movie["stream"]
    download_link = movie["download"]

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
        content="width=device-width, initial-scale=1.0">

        <title>{file_name}</title>

        <style>

        body{{
            margin:0;
            padding:20px;
            background:#050018;
            color:white;
            font-family:Arial;
            text-align:center;
        }}

        .box{{
            max-width:700px;
            margin:auto;
            background:#120329;
            padding:20px;
            border-radius:20px;
        }}

        video{{
            width:100%;
            border-radius:15px;
            margin-top:20px;
            background:black;
        }}

        .btns{{
            display:flex;
            gap:15px;
            margin-top:20px;
            flex-wrap:wrap;
            justify-content:center;
        }}

        .btn{{
            padding:14px 25px;
            border-radius:12px;
            text-decoration:none;
            color:white;
            font-weight:bold;
        }}

        .download{{
            background:#6c4cff;
        }}

        .mx{{
            background:#00b894;
        }}

        .vlc{{
            background:#ff9800;
        }}

        </style>
    </head>

    <body>

        <div class="box">

            <h1>{file_name}</h1>

            <video controls autoplay>
                <source src="{stream_link}" type="video/mp4">
            </video>

            <div class="btns">

                <a
                class="btn download"
                href="{download_link}">
                ⬇ Download
                </a>

                <a
                class="btn mx"
                href="intent:{stream_link}#Intent;package=com.mxtech.videoplayer.ad;end">
                ▶ MX Player
                </a>

                <a
                class="btn vlc"
                href="intent:{stream_link}#Intent;package=org.videolan.vlc;end">
                ▶ VLC Player
                </a>

            </div>

        </div>

    </body>
    </html>
    """

    return render_template_string(html)

# =========================
# UPLOAD MOVIE
# =========================

@bot.on_message(filters.video | filters.document)
async def upload_movie(client, message):

    media = message.video or message.document

    file_id = media.file_id
    file_name = media.file_name or "Movie"

    # TELEGRAM DIRECT LINK
    stream_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"

    # SAVE
    movies[file_id] = {
        "name": file_name,
        "stream": stream_link,
        "download": stream_link
    }

    # WEBSITE LINK
    watch_link = f"{BASE_URL}/watch/{file_id}"

    await message.reply_text(
        f"""
✅ Movie Uploaded Successfully

🎬 Watch Link:
{watch_link}
"""
    )

# =========================
# START FLASK
# =========================

def run_flask():
    app.run(
        host="0.0.0.0",
        port=10000
    )

# =========================
# START EVERYTHING
# =========================

if __name__ == "__main__":

    Thread(target=run_flask).start()

    print("✅ Bot Started")

    bot.run()
