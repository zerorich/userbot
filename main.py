import os
import asyncio
from telethon import TelegramClient, events, errors
import getpass

api_id = '21396794'
api_hash = '5b9ac3a8dd838c62111e033dd481dcc6'

def get_existing_sessions():
    sessions = []
    for filename in os.listdir():
        if filename.endswith('.session'):
            sessions.append(filename[:-8])  # удаляем расширение ".session"te
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

    # Обработчик для сообщений, отправленных вами (outgoing=True)
    @client.on(events.NewMessage(outgoing=True))
    # @client.on(events.NewMessage)

    async def handler(event):
        text = event.message.text or ""
        # Здесь можно добавить любую логику обработки ваших сообщений
        if ".sm" in text.lower():
            await event.message.edit("Саламалекум")
        if ".wu" in text.lower():
            await event.message.edit("Hey! What's up bro?")

    # Клиент работает до ручного завершения (например, через Ctrl+C)
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
