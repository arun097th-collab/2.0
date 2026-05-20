from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread

# ====================================
# TELEGRAM CONFIG
# ====================================

API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"

# ====================================
# YOUR RENDER URL
# ====================================

RENDER_URL = "https://YOUR-APP.onrender.com"

# ====================================
# START BOT
# ====================================

bot = Client(
    "moviebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ====================================
# FLASK APP
# ====================================

app = Flask(__name__)

# ====================================
# STORE MOVIES
# ====================================

movies = {}

# ====================================
# HOME
# ====================================

@app.route("/")
def home():
    return "Bot Running Successfully"

# ====================================
# UPLOAD VIDEO / FILE
# ====================================

@bot.on_message(filters.video | filters.document)
async def upload_movie(client, message):

    file = message.video or message.document

    file_id = file.file_id
    file_name = file.file_name or "Movie"

    # STORE
    movies[file_id] = {
        "name": file_name
    }

    # WATCH LINK
    watch_link = f"{RENDER_URL}/watch/{file_id}"

    await message.reply_text(
        f"""
✅ File Uploaded Successfully

🎬 Watch Link:
{watch_link}
"""
    )

# ====================================
# WATCH PAGE
# ====================================

@app.route("/watch/<path:file_id>")
def watch(file_id):

    movie = movies.get(file_id)

    if not movie:
        return "❌ File Not Found"

    file_name = movie["name"]

    # TELEGRAM STREAM LINK
    stream_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"

    html = f"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{file_name}</title>

<style>

body{{
background:#050018;
color:white;
font-family:Arial;
padding:20px;
text-align:center;
}}

.video{{
width:100%;
max-width:900px;
border-radius:20px;
margin-top:20px;
background:black;
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
text-decoration:none;
font-weight:bold;
color:white;
background:#6c4cff;
display:inline-block;
}}

.mx{{
background:#00b894;
}}

.vlc{{
background:#ff6b00;
}}

</style>
</head>

<body>

<h1>{file_name}</h1>

<video class="video" controls autoplay>

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

<a
class="btn vlc"
href="intent:{stream_link}#Intent;package=org.videolan.vlc;end">

▶ VLC Player

</a>

</div>

</body>
</html>
"""

    return render_template_string(html)

# ====================================
# START FLASK
# ====================================

def run_flask():
    app.run(
        host="0.0.0.0",
        port=10000
    )

# ====================================
# MAIN
# ====================================

if __name__ == "__main__":

    Thread(target=run_flask).start()

    bot.run()
