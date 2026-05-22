from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread
import os

API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"


RENDER_URL = "https://two-0-uzcf.onrender.com"

# PUBLIC CHANNEL USERNAME
CHANNEL = "cm4umovies"

bot = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

app = Flask(__name__)

# =========================
# HOME
# =========================

@app.route("/")
def home():

    return "CM4U STREAM RUNNING"

# =========================
# SAVE MOVIE
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    try:

        copied = await message.copy(CHANNEL)

        msg_id = copied.id

        link = f"{RENDER_URL}/watch/{msg_id}"

        await message.reply_text(
            f"✅ Uploaded Successfully\n\n🎬 {link}"
        )

    except Exception as e:

        await message.reply_text(f"ERROR : {e}")

# =========================
# WATCH
# =========================

@app.route("/watch/<msg_id>")
def watch(msg_id):

    try:

        with bot:

           msg = bot.get_messages(CHANNEL, int(msg_id))

media = msg.video or msg.document

file_path = bot.download_media(
    media.file_id,
    file_name=f"downloads/{msg_id}"
)

        filename = os.path.basename(file_path)

        stream_link = f"{RENDER_URL}/file/{filename}"

        mx = (
            f"intent:{stream_link}"
            "#Intent;type=video/*;"
            "package=com.mxtech.videoplayer.ad;end"
        )

        vlc = (
            f"intent:{stream_link}"
            "#Intent;type=video/*;"
            "package=org.videolan.vlc;end"
        )

        return render_template_string(f"""

<!DOCTYPE html>

<html>

<head>

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

video{{
width:100%;
border-radius:20px;
background:black;
}}

.btn{{
display:block;
margin-top:15px;
padding:15px;
border-radius:15px;
text-decoration:none;
font-weight:bold;
color:white;
}}

.download{{background:#6c4cff;}}
.mx{{background:#00b894;}}
.vlc{{background:#ff3838;}}

</style>

</head>

<body>

<div class="container">

<h2>🎬 CM4U STREAM</h2>

<video controls autoplay>

<source src="{stream_link}">

</video>

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

</body>

</html>

""")

    except Exception as e:

        return f"ERROR : {e}"

# =========================
# FILE SERVER
# =========================

@app.route("/file/<filename>")
def file(filename):

    from flask import send_from_directory

    return send_from_directory(
        "downloads",
        filename,
        as_attachment=False
    )

# =========================
# RUN
# =========================

def run_flask():

    port = int(os.environ.get("PORT", 10000))

    os.makedirs("downloads", exist_ok=True)

    app.run(
        host="0.0.0.0",
        port=port
    )

# =========================
# START
# =========================

if __name__ == "__main__":

    Thread(target=run_flask).start()

    print("✅ CM4U BOT STARTED")

    bot.run()
