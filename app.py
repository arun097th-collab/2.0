from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread
import os

API_ID = 21295053
API_HASH = "297598578931dcc642c2519414079f8e"
BOT_TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"

RENDER_URL = "https://two-0-uzcf.onrender.com"

# PUBLIC CHANNEL USERNAME
CHANNEL_USERNAME = "cm4umovies"

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

        # COPY TO CHANNEL
        copied = await message.copy(CHANNEL_USERNAME)

        # MESSAGE ID
        msg_id = copied.id

        # TELEGRAM POST LINK
        tg_link = f"https://t.me/{CHANNEL_USERNAME}/{msg_id}"

        # WEBSITE LINK
        web_link = f"{RENDER_URL}/watch/{msg_id}"

        await message.reply_text(

            f"✅ Uploaded Successfully\n\n"
            f"🎬 Stream Link:\n{web_link}\n\n"
            f"📢 Telegram Post:\n{tg_link}"

        )

    except Exception as e:

        await message.reply_text(f"ERROR : {e}")

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<msg_id>")
def watch(msg_id):

    # TELEGRAM POST
    tg_embed = f"https://t.me/{CHANNEL_USERNAME}/{msg_id}?embed=1"

    html = f"""

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

iframe{{
width:100%;
height:700px;
border:none;
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

.tg{{
background:#229ED9;
}}

</style>

</head>

<body>

<div class="container">

<h2>🎬 CM4U STREAM</h2>

<!-- TELEGRAM EMBED -->

<iframe src="{tg_embed}"></iframe>

<!-- OPEN TELEGRAM -->

<a class="btn tg"
href="https://t.me/{CHANNEL_USERNAME}/{msg_id}">
📢 Open In Telegram
</a>

</div>

</body>

</html>

"""

    return render_template_string(html)

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
# START
# =========================

if __name__ == "__main__":

    Thread(target=run_flask).start()

    print("✅ CM4U BOT STARTED")

    bot.run()
