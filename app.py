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
# STORAGE
# =========================

movies = {}

# =========================
# HOME
# =========================

@app.route("/")
def home():

    return """
    <h1 style='font-family:Arial;text-align:center;margin-top:50px'>
    ✅ Telegram Streaming Bot Running
    </h1>
    """

# =========================
# UPLOAD MOVIE
# =========================

@bot.on_message(filters.video | filters.document)
async def upload_movie(client, message):

    file = message.video or message.document

    file_id = file.file_id
    file_name = file.file_name or "Movie"
    file_size = round(file.file_size / (1024 * 1024), 2)

    movies[file_id] = {
        "name": file_name,
        "size": file_size
    }

    watch_link = f"https://YOUR-RENDER-URL.onrender.com/watch/{file_id}"

    await message.reply_text(

f"""
✅ Movie Added Successfully

🎬 Watch Link:
{watch_link}
"""

    )

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    movie = movies.get(file_id)

    if not movie:
        return "Movie Not Found"

    file_name = movie["name"]
    file_size = movie["size"]

    direct_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"

    html = f"""

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{file_name}</title>

<script src="https://cdn.tailwindcss.com"></script>

<style>

body{{
background:#050018;
font-family:Arial;
color:white;
}}

.box{{
max-width:500px;
margin:auto;
margin-top:50px;
padding:25px;
background:#120329;
border-radius:20px;
text-align:center;
}}

video{{
width:100%;
border-radius:15px;
margin-top:20px;
}}

.btn{{
display:block;
padding:14px;
margin-top:15px;
border-radius:12px;
font-weight:bold;
text-decoration:none;
}}

.download{{
background:#6c4cff;
color:white;
}}

.mx{{
background:#00b894;
color:white;
}}

.vlc{{
background:#ff9800;
color:white;
}}

</style>

</head>

<body>

<div class="box">

<h1 style="font-size:22px;font-weight:bold">
{file_name}
</h1>

<p style="margin-top:10px;color:#aaa">
Size : {file_size} MB
</p>

<video controls autoplay>

<source
src="{direct_link}"
type="video/mp4">

</video>

<a
class="btn download"
href="{direct_link}">
⬇ Download
</a>

<a
class="btn mx"
href="intent:{direct_link}#Intent;package=com.mxtech.videoplayer.ad;end">
▶ Play In MX Player
</a>

<a
class="btn vlc"
href="intent:{direct_link}#Intent;package=org.videolan.vlc;end">
▶ Play In VLC
</a>

</div>

</body>
</html>

"""

    return render_template_string(html)

# =========================
# START
# =========================

if __name__ == "__main__":

    Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=10000
        )
    ).start()

    bot.run()
