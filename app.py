from pyrogram import Client, filters
from flask import Flask, render_template_string
from threading import Thread

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
# STORE
# =========================

movies = {}

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return "Bot Running"

# =========================
# UPLOAD
# =========================

@bot.on_message(filters.video | filters.document)
async def upload_movie(client, message):

    file = message.video or message.document

    file_id = file.file_id
    file_name = file.file_name or "Movie"

    # SAVE
    movies[file_id] = {
        "name": file_name
    }

    # LINK
    link = f"{RENDER_URL}/watch/{file_id}"

    await message.reply_text(
        f"✅ Uploaded\n\n🎬 Link:\n{link}"
    )

# =========================
# WATCH PAGE
# =========================

@app.route("/watch/<path:file_id>")
def watch(file_id):

    movie = movies.get(file_id)

    if not movie:
        return "❌ File Not Found"

    try:

        # GET REAL FILE PATH
        tg_file = bot.get_file(file_id)

        file_path = tg_file.file_path

        # REAL STREAM LINK
        stream_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    except Exception as e:
        return f"ERROR : {e}"

    html = f"""
    <!DOCTYPE html>
    <html>

    <head>

    <meta name="viewport"
    content="width=device-width, initial-scale=1.0">

    <style>

    body{{
    background:#050018;
    color:white;
    font-family:Arial;
    text-align:center;
    padding:20px;
    }}

    video{{
    width:100%;
    max-width:900px;
    border-radius:20px;
    background:black;
    }}

    .btn{{
    display:inline-block;
    margin:10px;
    padding:14px 25px;
    border-radius:12px;
    text-decoration:none;
    color:white;
    font-weight:bold;
    background:#6c4cff;
    }}

    </style>

    </head>

    <body>

    <h1>{movie["name"]}</h1>

    <video controls autoplay>

    <source
    src="{stream_link}"
    type="video/mp4">

    </video>

    <br>

    <a class="btn"
    href="{stream_link}">
    ⬇ Download
    </a>

    <a class="btn"
    href="intent:{stream_link}#Intent;package=com.mxtech.videoplayer.ad;end">
    ▶ MX Player
    </a>

    </body>
    </html>
    """

    return render_template_string(html)

# =========================
# RUN FLASK
# =========================

def run_flask():
    app.run(
        host="0.0.0.0",
        port=10000
    )

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    Thread(target=run_flask).start()

    bot.run()
