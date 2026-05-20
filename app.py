from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread

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
# UPLOAD VIDEO / FILE
# =========================

@bot.on_message(filters.video | filters.document)
async def upload_movie(client, message):

    file = message.video or message.document

    file_id = file.file_id
    file_name = file.file_name or "Movie"

    # REAL TELEGRAM FILE
    tg_file = await bot.get_file(file_id)

    # REAL FILE PATH
    real_file_path = tg_file.file_path

    # SAVE
    movies[file_id] = {
        "name": file_name,
        "path": real_file_path
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
    )

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<path:file_id>")
def watch(file_id):

    movie = movies.get(file_id)

    if not movie:
        return "❌ File Not Found"

    # REAL STREAM LINK
    stream_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{movie['path']}"

    html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{movie['name']}</title>

<style>

*{{
margin:0;
padding:0;
box-sizing:border-box;
}}

body{{
background:#050018;
font-family:Arial;
color:white;
padding:20px;
text-align:center;
}}

.container{{
max-width:900px;
margin:auto;
}}

video{{
width:100%;
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
padding:14px 24px;
border-radius:12px;
background:#6c4cff;
color:white;
text-decoration:none;
font-weight:bold;
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

<div class="container">

<h1>{movie['name']}</h1>

<video controls autoplay>

<source
src="{stream_link}"
type="video/mp4">

</video>

<div class="btns">

<a
class="btn"
href="{stream_link}"
download>
⬇ Download
</a>

<a
class="btn mx"
href="intent:{stream_link}#Intent;action=android.intent.action.VIEW;type=video/*;package=com.mxtech.videoplayer.ad;end">
▶ MX Player
</a>

<a
class="btn vlc"
href="intent:{stream_link}#Intent;action=android.intent.action.VIEW;type=video/*;package=org.videolan.vlc;end">
▶ VLC Player
</a>

</div>

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
