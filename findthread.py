import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetForumTopics
import secret

# 🔑 Inserisci le tue credenziali
api_id = secret.api_id          # es. 123456
api_hash = secret.api_hash   # es. 'abcdef123456...'

# 🔁 Inserisci l'ID del supergruppo (es. -1001234567890)
group_id = -1002637946764

client = TelegramClient("session_name", api_id, api_hash)

async def list_topics():
    await client.start()
    
    print(f"📋 Elenco topic del gruppo {group_id}:\n")

    result = await client(GetForumTopics(
        peer=group_id,
        offset_date=None,
        offset_id=0,
        offset_topic=0,
        limit=100
    ))

    for topic in result.topics:
        print(f"🧵 ID: {topic.id} — Titolo: {topic.title} — Creato: {topic.date.strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\nTotale topic trovati: {len(result.topics)}")

asyncio.run(list_topics())
