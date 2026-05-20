from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread
import asyncio
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

# =========================
# STORE
# =========================

movies = {}

# =========================
# SAVE VIDEO
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    media = message.video or message.document

    file_id = media.file_id
    file_name = media.file_name or "Video"

    movies[file_id] = {
        "name": file_name
    }

    link = f"{DOMAIN}/watch/{file_id}"

    await message.reply_text(
        f"✅ Uploaded Successfully\n\n🎬 Link:\n{link}"
    )

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return "Bot Running Successfully"

# =========================
# WATCH
# =========================

@app.route("/watch/<file_id>")
def watch(file_id):

    if file_id not in movies:
        return "File Not Found"

    file_name = movies[file_id]["name"]

    async def get_link():

        file_data = await bot.get_messages(
            "me",
            1
        )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    file = loop.run_until_complete(
        bot.get_file(file_id)
    )

    file_path = file.file_path

    stream_link = (
        f"https://api.telegram.org/file/bot"
        f"{BOT_TOKEN}/{file_path}"
    )

    mx = (
        f"intent:{stream_link}"
        f"#Intent;type=video/*;"
        f"package=com.mxtech.videoplayer.ad;end"
    )

    vlc = (
        f"intent:{stream_link}"
        f"#Intent;type=video/*;"
        f"package=org.videolan.vlc;end"
    )

    return render_template_string(f"""

<!DOCTYPE html>
<html>

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
margin:0;
}}

video{{
width:100%;
max-width:900px;
border-radius:20px;
background:black;
}}

.btn{{
display:block;
margin:15px auto;
padding:15px;
width:90%;
max-width:400px;
border-radius:14px;
font-size:18px;
font-weight:bold;
text-decoration:none;
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

</style>

</head>

<body>

<h1>{file_name}</h1>

<video controls autoplay>

<source src="{stream_link}" type="video/mp4">

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

</body>
</html>

""")

# =========================
# RUN
# =========================

def run_flask():

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )

if __name__ == "__main__":

    Thread(target=run_flask).start()

    print("Bot Started")

    bot.run()
