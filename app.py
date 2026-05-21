from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread
import requests
import os

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
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================
# FLASK
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running ✅"

# =========================
# VIDEO UPLOAD HANDLER (FIXED)
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    try:

        # SAFE MEDIA PICK
        media = None

        if message.video:
            media = message.video
        elif message.document and "video" in (message.document.mime_type or ""):
            media = message.document

        if not media:
            await message.reply_text("❌ Only video supported")
            return

        file_id = media.file_id

        # FIXED LINK
        link = f"{BASE_URL}/watch/{file_id}"

        await message.reply_text(
            f"🎬 Upload Successful!\n\n🔗 Watch Link:\n{link}"
        )

    except Exception as e:
        await message.reply_text(f"ERROR: {e}")

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    try:

        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        ).json()

        if not file_info["ok"]:
            return "File Not Found ❌"

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

body {{
margin:0;
background:black;
overflow:hidden;
font-family:Arial;
}}

video {{
width:100%;
height:100vh;
object-fit:cover;
}}

.top {{
position:absolute;
top:10px;
left:10px;
right:10px;
display:flex;
justify-content:space-between;
z-index:10;
}}

.btn {{
color:white;
padding:10px 14px;
text-decoration:none;
border-radius:10px;
background:rgba(255,255,255,0.15);
backdrop-filter:blur(10px);
}}

</style>
</head>

<body

oncontextmenu="return false"
onkeydown="return false">

<div class="top">
<a class="btn" href="{stream}">Download</a>
<a class="btn" href="{mx}">MX</a>
<a class="btn" href="{vlc}">VLC</a>
</div>

<video controls autoplay>
<source src="{stream}" type="video/mp4">
</video>

</body>
</html>
""")

    except Exception as e:
        return f"ERROR: {e}"

# =========================
# RUN
# =========================

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run).start()
    print("Bot Started 🚀")
    bot.run()
