from telethon import TelegramClient, events
import requests
import asyncio
import os

# 🔑 Credenziali MTProto
api_id =    111       # es. 123456
api_hash = ""    # es. 'abcdef123456...'
channel_username = 'Reapers Esports'  # es. 'ilFattoQuotidiano'
channel_id = -1002637946764
topic_ids = [3,4,5]



MapTopicToForumUrl = {
    3: "https://discord.com/api/webhooks/1390015892045299793/bHqTucXHQcXhvPRo2gjPT8SBUxNa8XCwKZefNMFDtMsrfWIo23fZrPeVFmhMye4kM2Ma", #basi_box
    4: "https://discord.com/api/webhooks/1390016160954716200/kZRy5NcycG8LoNEOjmzuEnFJl-ziYtYlN6E67RfUKwv7262kF3EGtsBOeOq3olfK300U", #basi_diamante
    5: "https://discord.com/api/webhooks/1390016362218389575/ART3yl07sCs8Wspgb-ML5F7yGJzHL_iIdIzi7p9zcusK_FTDBKwgl7kHtwBx8pvK5XwG" #basi_ring
}

MapTopicToForumName = {
    3: "basi_box",
    4: "basi_diamante",
    5: "basi_ring"

}

# 🔗 Webhook Discord
discord_webhook_url = 'https://discord.com/api/webhooks/1389682913540575396/HXNxOXLpieNLFROXWEYjLcNyAVQxeAEs1rxMcStka3rgNC8hTUcArraEYCqW_jAWd8j8'

# ⚙️ Avvio client Telegram
client = TelegramClient("session_name", api_id, api_hash)

# @client.on(events.NewMessage(chats=channel_id))
# async def forward_to_discord(event):
#     msg = event.message
#     text = msg.message or "[Messaggio senza testo]"
#     sender = await event.get_sender()
#     sender_name = getattr(sender, 'first_name', 'Sconosciuto')

#     # ✉️ Contenuto del messaggio da inviare
#     content = f"**{sender_name}** ha scritto:\n{text}"

#     # Invia a Discord
#     requests.post(discord_webhook_url, json={"content": content})
#     print(f"[→] Inoltrato: {text}")

@client.on(events.NewMessage(chats=channel_id))
async def forward_topic_messages(event):
    msg = event.message
    thread_id = msg.reply_to_msg_id if msg.reply_to_msg_id else None

    if thread_id not in MapTopicToForumUrl: #al max MapTopicToForumUrl.keys()
        return  # ignora se non è uno dei topic monitorati

    sender = await event.get_sender()
    sender_name = getattr(sender, 'first_name', 'Sconosciuto')
    text = msg.message or "[Messaggio vuoto]"

    redirect_url = MapTopicToForumUrl[thread_id]
    redirect_name = MapTopicToForumName[thread_id]

    # Inoltra il messaggio su Discord
    content = f"{text}"
    if msg.photo:
        # Scarica la foto in una cartella temporanea
        file_path = f"temp_{msg.id}.jpg"
        await msg.download_media(file_path)

        # Invia il messaggio + immagine come file
        with open(file_path, 'rb') as image:
            files = {'file': image}
            data = {'content': content}
            response = requests.post(redirect_url, data=data, files=files)

        os.remove(file_path)  # pulizia
        print(f"[📸] Foto + messaggio inoltrati dal topic {thread_id}")
    else:
        # Solo testo
        requests.post(redirect_url, json={"content": content})
        print(f"[→] Messaggio senza immagine inoltrato dal topic {thread_id}")


async def main():
    await client.start()
    print(f"✅ In ascolto sul gruppo {channel_id} - Reapers Esports...")
    await client.run_until_disconnected()

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("\n🛑 Arrestato con Ctrl+C.")