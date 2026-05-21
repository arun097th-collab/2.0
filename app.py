from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread
import requests
import os

# =========================
# TELEGRAM CONFIG
# =========================

API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"

# =========================
# DOMAIN
# =========================

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
# HOME
# =========================

@app.route("/")
def home():
    return """

    <html>

    <head>

    <title>CM4U</title>

    <style>

    body{
        margin:0;
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
        background:#050018;
        color:white;
        font-family:Arial;
    }

    .box{
        background:rgba(255,255,255,0.08);
        backdrop-filter:blur(18px);
        padding:40px;
        border-radius:25px;
        border:1px solid rgba(255,255,255,0.1);
        box-shadow:0 0 30px rgba(108,76,255,0.4);
        text-align:center;
    }

    h1{
        font-size:35px;
    }

    p{
        color:#bbb;
    }

    </style>

    </head>

    <body>

    <div class="box">

    <h1>CM4U.xo.je. official website</h1>

    <p>Glass UI Streaming Server Active</p>

    </div>

    </body>

    </html>

    """

# =========================
# BOT MESSAGE
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    try:

        media = message.video or message.document

        file_id = media.file_id

        # GENERATE LINK
        link = f"{RENDER_URL}/watch/{file_id}"

        await message.reply_text(
            f"✅ Uploaded Successfully\n\n🎬 Link:\n{link}"
        )

    except Exception as e:

        await message.reply_text(f"ERROR : {e}")

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
            return "❌ File Not Found"

        file_path = file_info["result"]["file_path"]

        stream_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        mx = f"intent:{stream_link}#Intent;type=video/*;package=com.mxtech.videoplayer.ad;end"
        vlc = f"intent:{stream_link}#Intent;type=video/*;package=org.videolan.vlc;end"

        return render_template_string(f"""
<!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Premium Stream</title>

<style>

body{{
margin:0;
background:linear-gradient(135deg,#050018,#14003b,#240046);
font-family:Arial;
color:white;
text-align:center;
padding:15px;
}}

.container{{
max-width:950px;
margin:auto;
background:rgba(255,255,255,0.08);
backdrop-filter:blur(20px);
border-radius:25px;
padding:20px;
border:1px solid rgba(255,255,255,0.1);
box-shadow:0 0 40px rgba(108,76,255,0.35);
}}

video{{
width:100%;
border-radius:18px;
background:black;
}}

.btn{{
display:block;
margin-top:12px;
padding:14px;
border-radius:12px;
color:white;
text-decoration:none;
font-weight:bold;
}}

.download{{background:#6c4cff;}}
.mx{{background:#00b894;}}
.vlc{{background:#ff3838;}}

.adbox{{
margin:10px 0;
display:flex;
justify-content:center;
}}

</style>

</head>

<body>

<div class="container">

<h2>CM4U.xo.je. official website </h2>

<!-- 🔥 TOP AD -->
<div class="adbox">
<script>
  atOptions = {{
    'key' : '5cf28619f37f1ae9afd5de4731cf2976',
    'format' : 'iframe',
    'height' : 60,
    'width' : 468,
    'params' : {{}}
  }};
</script>
<script src="https://www.highperformanceformat.com/5cf28619f37f1ae9afd5de4731cf2976/invoke.js"></script>
</div>

<script async="async" data-cfasync="false" src="https://pl29465338.effectivecpmnetwork.com/d88ed5a99ceb47c15d7d9de634ed832c/invoke.js"></script>
<div id="container-d88ed5a99ceb47c15d7d9de634ed832c"></div>

<script src="https://pl29465340.effectivecpmnetwork.com/c4/79/3b/c4793b9d80232e17ab5b1bcc7edb640f.js"></script>

<!-- VIDEO -->
<video controls autoplay>
<source src="{stream_link}" type="video/mp4">
</video>

<!-- 🔥 BOTTOM AD -->
<div class="adbox">
<script>
  atOptions = {{
    'key' : '5cf28619f37f1ae9afd5de4731cf2976',
    'format' : 'iframe',
    'height' : 60,
    'width' : 468,
    'params' : {{}}
  }};
</script>
<script src="https://www.highperformanceformat.com/5cf28619f37f1ae9afd5de4731cf2976/invoke.js"></script>
</div>
<!-- 🔥 BOTTOM AD -->
<div class="adbox">
<script>
  atOptions = {{
    'key' : '5cf28619f37f1ae9afd5de4731cf2976',
    'format' : 'iframe',
    'height' : 60,
    'width' : 468,
    'params' : {{}}
  }};
</script>
<script src="https://www.highperformanceformat.com/5cf28619f37f1ae9afd5de4731cf2976/invoke.js"></script>
</div>

<!-- BUTTONS -->
<a class="btn download" href="{stream_link}">⬇ Download</a>
<a class="btn mx" href="{mx}">▶ MX Player</a>
<a class="btn vlc" href="{vlc}">▶ VLC Player</a>

</div>
<!-- POPUNDER AD -->
<script src="https://pl29465339.effectivecpmnetwork.com/4d/32/27/4d3227fddc75659508c78f4db2d6497e.js"></script>

</body>

</html>
""")

    except Exception as e:
        return f"ERROR: {e}"

# =========================
# RUN FLASK
# =========================

def run_flask():

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )

# =========================
# START BOT
# =========================

if __name__ == "__main__":

    Thread(target=run_flask).start()

    print("✅ Premium Stream Bot Started")

    bot.run()
