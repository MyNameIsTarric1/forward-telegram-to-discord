from telethon import TelegramClient, events
import requests
import asyncio

# 🔑 Credenziali MTProto
api_id =  1111          # es. 123456
api_hash =  ""   # es. 'abcdef123456...'
channel_username = 'Reapers Esports'  # es. 'ilFattoQuotidiano'


# CON QUESTA FUNZIONE PRENDI L'ID DEL CANALE TELEGRAM

async def main():
	async with TelegramClient('session_name', api_id, api_hash) as client:
		async for dialog in client.iter_dialogs():
			entity = dialog.entity
			name = dialog.name
			if name == channel_username:
				chat_id = dialog.id
				chat_type = type(entity).__name__
				print(f"[{chat_type}] {name} — ID: {chat_id}")

			

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("\n🛑 Arrestato con Ctrl+C.")