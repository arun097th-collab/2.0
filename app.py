from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread
import os

# =========================
# TELEGRAM CONFIG
# =========================


API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"

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
# STORE FILE DATA
# =========================

movies = {}

# =========================
# BOT START
# =========================

@bot.on_message(filters.video | filters.document)
async def upload_file(client, message):

    file = message.video or message.document

    file_id = file.file_id
    file_name = file.file_name or "Video"
    file_size = round(file.file_size / 1024 / 1024, 2)

    movies[file_id] = {
        "name": file_name,
        "size": file_size
    }

    link = f"{BASE_URL}/watch/{file_id}"

    await message.reply_text(
        f"""
✅ Uploaded Successfully

🎬 File : {file_name}

🔗 Link :
{link}
"""
    )

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return "Bot Running Successfully"

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    if file_id not in movies:
        return "Invalid Link"

    data = movies[file_id]

    file_name = data["name"]
    file_size = data["size"]

    # TELEGRAM FILE LINK
    direct_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"

    html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{file_name}</title>

<style>

*{{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Arial;
}}

body{{
background:#050018;
color:white;
display:flex;
justify-content:center;
align-items:center;
min-height:100vh;
padding:20px;
}}

.box{{
width:100%;
max-width:500px;
background:#120329;
padding:30px;
border-radius:25px;
text-align:center;
box-shadow:0 0 30px rgba(0,0,0,.5);
}}

h1{{
font-size:24px;
margin-bottom:15px;
word-break:break-word;
}}

.size{{
color:#aaa;
margin-bottom:25px;
}}

.btn{{
display:block;
width:100%;
padding:16px;
margin-top:15px;
border-radius:14px;
text-decoration:none;
font-weight:bold;
font-size:17px;
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

<h1>{file_name}</h1>

<div class="size">
📦 {file_size} MB
</div>

<a
class="btn download"
href="{direct_link}">
⬇ Download
</a>

<a
class="btn mx"
href="intent:{direct_link}#Intent;type=video/*;package=com.mxtech.videoplayer.ad;end">
▶ Open In MX Player
</a>

<a
class="btn vlc"
href="intent:{direct_link}#Intent;type=video/*;package=org.videolan.vlc;end">
▶ Open In VLC
</a>

</div>

</body>
</html>
"""

    return render_template_string(html)

# =========================
# START FLASK
# =========================

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

# =========================
# START BOT
# =========================

bot.run()
