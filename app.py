from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread
import asyncio

# =========================
# CONFIG
# =========================

API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"

RENDER_URL = "https://two-0-uzcf.onrender.com"


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
# STORE FILES
# =========================

movies = {}

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return "Bot Running Successfully"

# =========================
# UPLOAD FILE
# =========================

@bot.on_message(filters.video | filters.document)
async def upload_movie(client, message):

    file = message.video or message.document

    file_id = file.file_id
    file_name = file.file_name or "Movie"

    # GET REAL FILE
    tg_file = await bot.get_messages(
        chat_id=message.chat.id,
        message_ids=message.id
    )

    if tg_file.video:
        file_path = tg_file.video.file_id
    else:
        file_path = tg_file.document.file_id

    # SAVE
    movies[file_id] = {
        "name": file_name,
        "path": file_path
    }

    # LINK
    link = f"{RENDER_URL}/watch/{file_id}"

    await message.reply_text(
        f"""
✅ Uploaded Successfully

🎬 Watch Link:
{link}
"""
    )

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<path:file_id>")
def watch(file_id):

    movie = movies.get(file_id)

    if not movie:
        return "❌ File Not Found"

    # STREAM LINK
    stream_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{movie['path']}"

    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{movie['name']}</title>

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
max-width:900px;
border-radius:20px;
background:black;
margin-top:20px;
}}

.btns{{
display:flex;
gap:15px;
justify-content:center;
flex-wrap:wrap;
margin-top:25px;
}}

.btn{{
padding:14px 25px;
border-radius:12px;
background:#6c4cff;
color:white;
text-decoration:none;
font-weight:bold;
}}

.mx{{
background:#00b894;
}}

</style>

</head>

<body>

<h1>{movie['name']}</h1>

<video controls autoplay>

<source
src="{stream_link}"
type="video/mp4">

</video>

<div class="btns">

<a
class="btn"
href="{stream_link}">
⬇ Download
</a>

<a
class="btn mx"
href="intent:{stream_link}#Intent;package=com.mxtech.videoplayer.ad;end">
▶ MX Player
</a>

</div>

</body>
</html>
"""

    return render_template_string(html)

# =========================
# RUN FLASK
# =========================

def run_flask():
    app.run(
        host="0.0.0.0",
        port=10000
    )

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    Thread(target=run_flask).start()

    bot.run()
