# requirements:
# pip install pyrogram tgcrypto flask

from pyrogram import Client, filters
from flask import Flask, render_template_string, request

# =========================
# TELEGRAM CONFIG
# =========================
API_ID = 12345678
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

# =========================
# CHANNEL USERNAME
# =========================
CHANNEL = "your_channel_username"

# =========================
# BOT START
# =========================
bot = Client(
    "moviebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================
# WEBSITE
# =========================
app = Flask(name)

# =========================
# STORE FILES
# =========================
movies = {}

# =========================
# UPLOAD MOVIE
# =========================
@bot.on_message(filters.video | filters.document)
async def upload_movie(client, message):

    file_id = message.video.file_id if message.video else message.document.file_id
    file_name = message.video.file_name if message.video else message.document.file_name

    movies[file_id] = file_name

    watch_link = f"https://yourdomain.com/watch/{file_id}"

    await message.reply_text(
        f"✅ Movie Uploaded\n\n🎬 Watch Link:\n{watch_link}"
    )

# =========================
# WEBSITE PLAYER PAGE
# =========================
@app.route("/watch/<file_id>")
def watch(file_id):

    file_name = movies.get(file_id, "Movie")

    video_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{file_name}</title>

        <style>
        body {{
            background:#000;
            color:white;
            font-family:Arial;
            text-align:center;
        }}

        video {{
            width:90%;
            margin-top:20px;
        }}

        .btn {{
            display:inline-block;
            margin:10px;
            padding:12px 25px;
            background:red;
            color:white;
            text-decoration:none;
            border-radius:10px;
        }}
        </style>
    </head>

    <body>

        <h1>{file_name}</h1>

        <video controls>
            <source src="{video_link}" type="video/mp4">
        </video>

        <br>

        <a class="btn" href="{video_link}">
            Download
        </a>

        <a class="btn"
        href="intent:{video_link}#Intent;package=com.mxtech.videoplayer.ad;end">
            Open In MX Player
        </a>

    </body>
    </html>
    '''

    return render_template_string(html)

# =========================
# RUN FLASK
# =========================
if name == "main":

    from threading import Thread

    Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()

    bot.run()
