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

BASE_URL = "https://two-0-uzcf.onrender.com"

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
    return "🎬 Stream Bot Running"

# =========================
# UPLOAD HANDLER
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    try:

        media = message.video if message.video else message.document

        if not media:
            await message.reply_text("❌ Only video supported")
            return

        file_id = media.file_id

        link = f"{BASE_URL}/watch/{file_id}"

        await message.reply_text(
            f"🎬 Upload Successful\n\n🔗 Watch Link:\n{link}"
        )

    except Exception as e:
        await message.reply_text(f"ERROR: {e}")

# =========================
# WATCH PAGE (GLASS UI)
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    try:

        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        ).json()

        if not file_info["ok"]:
            return "❌ File Not Found"

        file_path = file_info["result"]["file_path"]

        stream = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        mx = f"intent:{stream}#Intent;type=video/*;package=com.mxtech.videoplayer.ad;end"
        vlc = f"intent:{stream}#Intent;type=video/*;package=org.videolan.vlc;end"

        return render_template_string(f"""
<!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glass Stream</title>

<style>

*{{
margin:0;
padding:0;
box-sizing:border-box;
}}

body{{
height:100vh;
width:100%;
overflow:hidden;
font-family:Arial;
background:linear-gradient(135deg,#050018,#12002b,#240046);
display:flex;
justify-content:center;
align-items:center;
}}

.container{{
width:95%;
max-width:1000px;
background:rgba(255,255,255,0.08);
backdrop-filter:blur(20px);
border-radius:25px;
border:1px solid rgba(255,255,255,0.1);
padding:20px;
box-shadow:0 0 40px rgba(108,76,255,0.4);
}}

h1{{
text-align:center;
color:white;
margin-bottom:15px;
}}

video{{
width:100%;
border-radius:18px;
background:black;
}}

.buttons{{
margin-top:15px;
display:flex;
flex-wrap:wrap;
gap:10px;
justify-content:center;
}}

.btn{{
padding:12px 18px;
border-radius:12px;
text-decoration:none;
color:white;
font-weight:bold;
backdrop-filter:blur(10px);
transition:0.3s;
}}

.btn:hover{{
transform:scale(1.05);
}}

.download{{background:rgba(108,76,255,0.6);}}
.mx{{background:rgba(0,184,148,0.6);}}
.vlc{{background:rgba(255,56,56,0.6);}}

.footer{{
text-align:center;
color:#bbb;
margin-top:10px;
font-size:13px;
}}

</style>

</head>

<body>

<div class="container">

<h1>🎬 Premium Glass Stream</h1>

<video controls autoplay controlsList="nodownload">
<source src="{stream}" type="video/mp4">
</video>

<div class="buttons">

<a class="btn download" href="{stream}">⬇ Download</a>
<a class="btn mx" href="{mx}">▶ MX Player</a>
<a class="btn vlc" href="{vlc}">▶ VLC Player</a>

</div>

<div class="footer">
⚡ Secure • Fast • Glass UI Stream
</div>

</div>

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
    print("🚀 Bot Started")
    bot.run()
