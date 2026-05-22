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
# CHANNEL ID
# =========================

CHANNEL_ID = "-1003502272528"

# =========================
# SAVE MOVIE
# =========================

@bot.on_message(filters.video | filters.document)
async def save_movie(client, message):

    try:

        # COPY TO CHANNEL
        saved = await client.copy_message(

            chat_id=int(CHANNEL_ID),

            from_chat_id=message.chat.id,

            message_id=message.id

        )

        # MESSAGE ID
        msg_id = saved.id

        # LINK
        link = f"{RENDER_URL}/watch/{msg_id}"

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

@app.route("/watch/<int:msg_id>")
def watch(msg_id):

    try:

        # GET MESSAGE
        msg = bot.get_messages(

            int(CHANNEL_ID),

            msg_id

        )

        # CHECK
        if not msg:
            return "❌ Message Not Found"

        media = msg.video or msg.document

        if not media:
            return "❌ Media Not Found"

        # TELEGRAM LINK
        tg_link = (

            f"https://t.me/c/"

            f"{str(CHANNEL_ID)[4:]}/"

            f"{msg_id}"

        )

        # MX PLAYER
        mx = (

            f"intent:{tg_link}"

            "#Intent;package=com.mxtech.videoplayer.ad;end"

        )

        # VLC PLAYER
        vlc = (

            f"intent:{tg_link}"

            "#Intent;package=org.videolan.vlc;end"

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
padding:20px;
background:
linear-gradient(135deg,#050018,#14003b,#240046);
font-family:Arial;
color:white;
display:flex;
justify-content:center;
align-items:center;
min-height:100vh;
}}

.container{{
width:100%;
max-width:650px;
background:rgba(255,255,255,0.08);
backdrop-filter:blur(18px);
padding:30px;
border-radius:25px;
text-align:center;
border:1px solid rgba(255,255,255,0.1);
}}

h1{{
margin-bottom:25px;
}}

.btn{{
display:block;
width:100%;
padding:18px;
margin-top:15px;
border-radius:16px;
text-decoration:none;
font-weight:bold;
font-size:18px;
color:white;
transition:.3s;
}}

.btn:hover{{
transform:scale(1.03);
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
margin:18px 0;
display:flex;
justify-content:center;
}}

</style>

</head>

<body>

<div class="container">

<h1>🎬 CM4U STREAM</h1>

<!-- TOP AD -->

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

<!-- DOWNLOAD -->

<a class="btn download"
href="{tg_link}"
target="_blank">

⬇ DOWNLOAD MOVIE

</a>

<!-- MX PLAYER -->

<a class="btn mx"
href="{mx}">

▶ PLAY IN MX PLAYER

</a>

<!-- VLC PLAYER -->

<a class="btn vlc"
href="{vlc}">

▶ PLAY IN VLC PLAYER

</a>

<!-- BOTTOM AD -->

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

</div>

<!-- POPUNDER -->

<script src="https://pl29465339.effectivecpmnetwork.com/4d/32/27/4d3227fddc75659508c78f4db2d6497e.js"></script>

</body>

</html>

""")

    except Exception as e:

        return f"ERROR : {e}"
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

    print("✅ CM4U STREAM BOT STARTED")

    bot.run()
