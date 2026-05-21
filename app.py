from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread
import requests
import os

# =========================
# CONFIG
# =========================

API_ID = 21295053
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"

BASE_URL = "https://your-render-url.onrender.com"

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
# FLASK APP
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Stream Bot Running"

# =========================
# UPLOAD HANDLER
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    media = message.video or message.document
    file_id = media.file_id

    link = f"{BASE_URL}/watch/{file_id}"

    await message.reply_text(
        f"🎬 Upload Successful!\n\n🔗 Watch Link:\n{link}"
    )

# =========================
# WATCH PAGE (FULL SCREEN GLASS UI)
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    try:
        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        ).json()

        if not file_info["ok"]:
            return "File Not Found"

        file_path = file_info["result"]["file_path"]

        stream = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        mx = f"intent:{stream}#Intent;type=video/*;package=com.mxtech.videoplayer.ad;end"
        vlc = f"intent:{stream}#Intent;type=video/*;package=org.videolan.vlc;end"

        return render_template_string(f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stream</title>

<style>

*{{
margin:0;
padding:0;
box-sizing:border-box;
}}

html,body{{
height:100%;
width:100%;
overflow:hidden;
background:black;
font-family:Arial;
user-select:none;
}}

video{{
width:100%;
height:100%;
object-fit:cover;
background:black;
}}

.top{{
position:absolute;
top:15px;
left:15px;
right:15px;
display:flex;
justify-content:space-between;
align-items:center;
z-index:10;
}}

.logo{{
color:white;
padding:10px 16px;
border-radius:15px;
background:rgba(255,255,255,0.08);
backdrop-filter:blur(15px);
}}

.btns{{
display:flex;
gap:10px;
}}

.btn{{
color:white;
text-decoration:none;
padding:10px 14px;
border-radius:12px;
background:rgba(255,255,255,0.1);
backdrop-filter:blur(10px);
font-size:14px;
}}

.download{{background:rgba(108,76,255,0.5);}}
.mx{{background:rgba(0,184,148,0.5);}}
.vlc{{background:rgba(255,56,56,0.5);}}

</style>
</head>

<body

oncontextmenu="return false"
onkeydown="return false">

<div class="top">
<div class="logo">🎬 STREAM</div>

<div class="btns">
<a class="btn download" href="{stream}">Download</a>
<a class="btn mx" href="{mx}">MX</a>
<a class="btn vlc" href="{vlc}">VLC</a>
</div>
</div>

<video controls autoplay controlsList="nodownload">
<source src="{stream}" type="video/mp4">
</video>

</body>
</html>
""")

    except Exception as e:
        return f"Error: {e}"

# =========================
# RUN SERVER
# =========================

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run).start()
    print("Bot Started 🚀")
    bot.run()
