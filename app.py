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

# CHANNEL USERNAME
CHANNEL_ID = "@cm4umovies"

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
        background:#050018;
        color:white;
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
        font-family:Arial;
    }

    h1{
        font-size:40px;
    }

    </style>

    </head>

    <body>

    <h1>🎬 CM4U STREAM SERVER</h1>

    </body>

    </html>

    """

# =========================
# SAVE MOVIE
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    try:

        # CHANNEL MA COPY
        copied = await message.copy(
            chat_id=CHANNEL_ID
        )

        # MESSAGE ID
        message_id = copied.id

        # LINK
        link = f"{RENDER_URL}/watch/{message_id}"

        await message.reply_text(

            f"✅ Uploaded Successfully\n\n🎬 Link:\n{link}"

        )

    except Exception as e:

        await message.reply_text(

            f"ERROR : {e}"

        )

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<int:message_id>")
def watch(message_id):

    try:

        # GET MESSAGE
        msg = bot.get_messages(
            CHANNEL_ID,
            message_id
        )

        # MEDIA
        media = msg.video or msg.document

        # FILE ID
        file_id = media.file_id

        # TELEGRAM FILE INFO
        file_info = requests.get(

            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",

            params={
                "file_id": file_id
            }

        ).json()

        # CHECK
        if not file_info.get("ok"):

            return f"Telegram Error : {file_info}"

        # FILE PATH
        file_path = file_info["result"]["file_path"]

        # STREAM LINK
        stream_link = (

            f"https://api.telegram.org/file/bot"
            f"{BOT_TOKEN}/{file_path}"

        )

        # MX PLAYER
        mx = (

            f"intent:{stream_link}"
            "#Intent;type=video/*;"
            "package=com.mxtech.videoplayer.ad;end"

        )

        # VLC PLAYER
        vlc = (

            f"intent:{stream_link}"
            "#Intent;type=video/*;"
            "package=org.videolan.vlc;end"

        )

        return render_template_string(f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>CM4U STREAM</title>

<style>

body{{
margin:0;
padding:15px;
background:
linear-gradient(135deg,#050018,#14003b,#240046);
font-family:Arial;
color:white;
text-align:center;
}}

.container{{
max-width:900px;
margin:auto;
}}

h2{{
margin-bottom:15px;
}}

video{{
width:100%;
border-radius:18px;
background:black;
}}

.btn{{
display:block;
margin-top:14px;
padding:15px;
border-radius:14px;
text-decoration:none;
font-weight:bold;
color:white;
}}

.download{{
background:#6c4cff;
}}

.mx{{
background:#00b894;
}}

.vlc{{
background:#ff3838;
}}

.adbox{{
margin:15px 0;
display:flex;
justify-content:center;
}}

</style>

</head>

<body>

<div class="container">

<h2>🎬 CM4U STREAM</h2>

<!-- TOP BANNER -->

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

<!-- VIDEO -->

<video controls autoplay preload="metadata">

<source src="{stream_link}">

</video>

<!-- BOTTOM BANNER -->

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

<a class="btn download"
href="{stream_link}">
⬇ Download
</a>

<a class="btn mx"
href="{mx}">
▶ MX Player
</a>

<a class="btn vlc"
href="{vlc}">
▶ VLC Player
</a>

</div>

<!-- POPUNDER -->

<script src="https://pl29465339.effectivecpmnetwork.com/4d/32/27/4d3227fddc75659508c78f4db2d6497e.js"></script>

</body>

</html>

""")

    except Exception as e:

        return f"ERROR : {e}"

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

    print("✅ CM4U STREAM BOT STARTED")

    bot.run()
