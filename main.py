import os
import asyncio
from telethon import TelegramClient, events, errors
from telethon.tl.functions.contacts import GetContactsRequest
import getpass

api_id = '21396794'
api_hash = '5b9ac3a8dd838c62111e033dd481dcc6'

# Словарь песен
COMMANDS = {
    "бот, ты тут?": "Да! Слушаю вас",
    "привет, бот": "Привет-привет 👋",
    "бот, привет": "Привет-привет 👋",
    "расскажи шутку": "Почему программисты путают Хэллоуин и Рождество? Потому что 31 OCT = 25 DEC 🎃🎄",
    "бот, кто я?": "Вы — мой создатель... или просто очень важный человек 🤖",
    "бот, сколько тебе лет?": "Я родился, когда ты запустил меня. А теперь живу вечно!",
    "бот, расскажи факт": "Знаешь ли ты, что осьминоги имеют три сердца и синюю кровь? 🐙",
    "бот, ты умный?": "Я умён ровно настолько, насколько ты меня запрограммировал 😏",
    "бот, ты скучный": "Скучный? Я? Попробуй ввести /game или /joke 😉",
    "бот, спать": "Спокойной ночи! 🌙 Я останусь на страже 🤖",
    "бот, кофе": "☕ Уже налил! Не забудь сделать глоток за меня.",
}
SONG_MAP = {
    "йупи йоу": "songs/scally-milano-163onmyneck-mayot-jupi-jo.mp3",
    "кофта пахнет твоим домом": "songs/right-person-kofta-paxnet-tvoim-domom.mp3",
    "never broke again": "songs/xmanera-Never_Broke_Again.mp3",
    "бритней": "songs/OBLADAET - Britney.mp3",
    "влага":"songs/Arut feat. Big Baby Tape - VLAGA.mp3",
    "бандана": "songs/big-baby-tape-kizaru-bandana.mp3",
    "errday": "songs/big baby tape stromae - ERRDAY berezhnyi remix.mp3"
    # добавь сюда другие песни по шаблону
}

def get_existing_sessions():
    sessions = []
    for filename in os.listdir():
        if filename.endswith('.session'):
            sessions.append(filename[:-8])  # удаляем расширение ".session"
    return sessions

async def authorize_client(client, phone_number=None):
    await client.connect()
    if not await client.is_user_authorized():
        if phone_number:
            await client.send_code_request(phone_number)
            code = input("Введите код из SMS: ")
            try:
                await client.sign_in(phone_number, code)
            except errors.SessionPasswordNeededError:
                password = getpass.getpass("Введите пароль: ")
                await client.sign_in(password=password)
        else:
            print("Не удалось авторизоваться. Номер телефона не задан.")
    return client

# === Обработка запроса на песню ===
async def handle_song_request(event, text):
    if text == ".help":
        help_text = "🤖 Доступные команды:\n\n"
        for cmd in COMMANDS:
            help_text += f"• {cmd}\n"
        help_text += "\nЧтобы отправить песню: `бот, скинь песню [название]`"
        await event.reply(help_text)
        return

    # Ответы по словарю команд
    for cmd, response in COMMANDS.items():
        if cmd in text:
            await event.reply(response)
            return

    # Обработка песен
    if "бот, скинь песню" in text:
        song_name = text.replace("бот, скинь песню", "").strip().lower()
        if song_name in SONG_MAP:
            song_path = SONG_MAP[song_name]
            if os.path.exists(song_path):
                await event.reply(file=song_path)
            else:
                await event.reply("К сожалению, я не могу найти эту песню.")
        else:
            await event.reply("Извините, я не знаю такую песню.")

async def main():
    sessions = get_existing_sessions()
    if sessions:
        print("Выберите аккаунт для входа:")
        for i, session in enumerate(sessions):
            print(f"{i + 1}. {session}")
        print(f"{len(sessions) + 1}. Новый аккаунт")
        choice = int(input("Введите номер выбора: "))
        if choice == len(sessions) + 1:
            phone_number = input("Введите номер телефона: ")
            client = TelegramClient(phone_number, api_id, api_hash)
            await authorize_client(client, phone_number)
        else:
            session_name = sessions[choice - 1]
            client = TelegramClient(session_name, api_id, api_hash)
            await authorize_client(client)
    else:
        phone_number = input("Введите номер телефона для нового аккаунта: ")
        client = TelegramClient(phone_number, api_id, api_hash)
        await authorize_client(client, phone_number)
    
    if await client.is_user_authorized():
        print("Авторизация прошла успешно!")
    else:
        print("Авторизация не удалась.")
        return

    # === Обработчик исходящих сообщений (твоих) ===
    @client.on(events.NewMessage(outgoing=True))
    async def handler(event):
        text = event.message.text or ""
        await handle_song_request(event, text)

        if "бот, ты тут?" in text.lower() or "бот ты тут?" in text.lower():
            await event.message.edit("Да! Слушаю вас")
        elif "привет, бот" in text.lower() or "бот, привет" in text.lower():
            await event.message.edit("Привет-привет 👋")
        elif "расскажи шутку" in text.lower():
            await event.message.edit("Почему программисты путают Хэллоуин и Рождество? Потому что 31 OCT = 25 DEC 🎃🎄")
        elif "бот, кто я?" in text.lower():
            await event.message.edit("Вы — мой создатель... или просто очень важный человек 🤖")
        elif "бот, сколько тебе лет?" in text.lower():
            await event.message.edit("Я родился, когда ты запустил меня. А теперь живу вечно!")
        elif "бот, расскажи факт" in text.lower():
            await event.message.edit("Знаешь ли ты, что осьминоги имеют три сердца и синюю кровь? 🐙")
        elif "бот, ты умный?" in text.lower():
            await event.message.edit("Я умён ровно настолько, насколько ты меня запрограммировал 😏")
        elif "бот, спать" in text.lower():
            await event.message.edit("Спокойной ночи! 🌙 Я останусь на страже 🤖")
        elif "бот, кофе" in text.lower():
            await event.message.edit("☕ Уже налил! Не забудь сделать глоток за меня.")

    # === Обработчик входящих сообщений от других пользователей ===
    @client.on(events.NewMessage(incoming=True))
    async def incoming_handler(event):
        text = event.raw_text.lower()
        await handle_song_request(event, text)

        if "бот, кто я для создателя" in text:
            sender = await event.get_sender()
            sender_id = sender.id

            contacts = await client(GetContactsRequest(hash=0))
            contact_name = None
            for user in contacts.users:
                if user.id == sender_id:
                    contact_name = f"{user.first_name} {user.last_name or ''}".strip()
                    break

            if contact_name:
                lower_name = contact_name.lower()
                if "бро" in lower_name or "друг" in lower_name:
                    await event.reply("Ты для создателя — очень близкий друг, настоящий бро! 💪")
                elif "любим" in lower_name:
                    await event.reply("Ты — особенный человек для создателя ❤️")
                elif "сашама" in lower_name:
                    await event.reply("Хм) Ты очень странно записана у создателя, но думаю что ты для него очень близкий человек")
                else:
                    await event.reply(f"Создатель записал тебя как: {contact_name}")
            else:
                await event.reply("Ты не записан у создателя в контактах... но, возможно, это временно? 🤔")

    # === Запуск клиента ===
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
