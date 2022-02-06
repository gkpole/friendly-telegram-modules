from .. import loader, utils
from asyncio import sleep
import random
import io, inspect
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import os
from gtts import gTTS
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from asyncio.exceptions import TimeoutError
import json
import base64
import requests
from telethon.tl.patched import Message
from telethon.tl import types
from typing import List, Union
from time import gmtime
import telethon

def get_message_media(message: Message): #хуита fsq
    data = None
    if message and message.media:
        data = message.photo or message.sticker or message.video or message.video_note or message.gif or message.web_preview
    return data
def get_entities(entities: types.TypeMessageEntity): #хуита fsq
    # coded by @droox
    r = []
    if entities:
        for entity in entities:
            entity = entity.to_dict()
            entity["type"] = entity.pop("_").replace("MessageEntity", "").lower()
            r.append(entity)
    return r
def get_message_text(message: Message, reply: bool = False): #хуита fsq
    return (
        "📷 Фото"
        if message.photo and reply
        else message.file.emoji + " Стикер"
        if message.sticker and reply
        else "📹 Видеосообщение"
        if message.video_note and reply
        else "📹 Видео"
        if message.video and reply
        else "🖼 GIF"
        if message.gif and reply
        else "📊 Опрос"
        if message.poll
        else "📍 Местоположение"
        if message.geo
        else "👤 Контакт"
        if message.contact
        else f"🎵 Голосовое сообщение: {strftime(message.voice.attributes[0].duration)}"
        if message.voice
        else f"🎧 Музыка: {strftime(message.audio.attributes[0].duration)} | {message.audio.attributes[0].performer} - {message.audio.attributes[0].title}"
        if message.audio
        else f"💾 Файл: {message.file.name}"
        if type(message.media) == types.MessageMediaDocument and not get_message_media(message)
        else f"{message.media.emoticon} Дайс: {message.media.value}"
        if type(message.media) == types.MessageMediaDice
        else f"Service message: {message.action.to_dict()['_']}"
        if type(message) == types.MessageService
        else ""
    )
def strftime(time: Union[int, float]): #хуита
    t = gmtime(time)
    return (
        (
            f"{t.tm_hour:02d}:"
            if t.tm_hour > 0
            else ""
        ) + f"{t.tm_min:02d}:{t.tm_sec:02d}"
    )
    
class ManyMod(loader.Module):
    """Сброник с самыми популярными и полезными модулями! by @CREATIVE_tg1"""
    strings = {
        "name": "CoolModules",
        "no_reply": "<b>[SQuotes]</b> Нет реплая",
        "processing": "<b>[SQuotes]</b> Обработка...",
        "api_processing": "<b>[SQuotes]</b> Ожидание API...",
        "api_error": "<b>[SQuotes]</b> Ошибка API",
        "loading_media": "<b>[SQuotes]</b> Отправка...",
        "no_args_or_reply": "<b>[SQuotes]</b> Нет аргументов или реплая",
        "args_error": "<b>[SQuotes]</b> При обработке аргументов произошла ошибка. Запрос был: <code>{}</code>",
        "too_many_messages": "<b>[SQuotes]</b> Слишком много сообщений. Максимум: <code>{}</code>"}
    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []
    async def client_ready(self, client: telethon.TelegramClient, db: dict):
        self.client = client
        self.db = db
        self.api_endpoint = "https://quotes.fl1yd.su/generate"
        self.settings = self.get_settings()
    #########################################################################################################
    async def helpcmcmd(self, message): #help
        """Напиши '.helpCM', чтобы узнать обо всех модулях, которые есть в этом модуле! Так-же, используй '.help CoolModules', чтобы получить больше информации о командах."""
        await message.edit("<b>Привет! Чтобы начать пользоваться данным модулем, ты должен написать:</b>\n1) <code>.terminal pip install --upgrade pip</code>\n2) <code>.terminal pip install gtts</code>\n3) <code>.terminal pip install telethon</code>\n\n<b>Модули, которые собраны в один модуль:</b>\n\n1) Spam - спамит сообщениями; <b>.spam</b>\n2) Tagall - созывает всех участников чата; <b>.tagall</b>\n3) DelMsg - удаляет все ваши сообщения; <b>.delmsg</b>\n4) Shiper - шиперит участников; <b>.shiper</b>\n5) RandNumb - выдает рандомное число; <b>.rand</b>\n6) SavePic - сохраняет самоуничтожающееся фото; <b>.зг</b>\n7) IamGhoul - спам 1000-7; <b>.ghoul</b>\n8) ModulesLink - отправляет файл на уже скаченный модуль; <b>.ml</b>\n9) HackChat - засор логов + фейк взлом чата; <b>.hack</b>\n10) Print - по символьно выводит предложение; <b>.print</b>\n11) Type - красиво и плавно выводит предложение; <b>.type</b>\n12) NedoQuotes - генерирует фотографии с надписями; <b>.nq</b>\n13)  SayText - переводит текст в голосовое сообщение; <b>.say</b>\n14) WhoIs - выводит информацию о пользователе; <b>.whois</b>\n15) RusRoul - игра русская рулетка(безопасно); <b>.rusroul</b>\n16) Wikipedia - выдает результат из википедии; <b>.wiki</b>\n17) TextS - выводит каждую букву в слове; <b>.ts</b>\n18) TextEdit - редактирует ваше сообщение через опреденное время или удаляет его; <b>.te</b>\n19) Online - делает вечный онлайн; <b>.online</b>\n20) SQuotes (Часть модуля) - создает стикер из сообщения; <b>.fsq</b>\n\n<b>by @CREATIVE_tg1</b>")

    async def spamcmd(self, message): #1
        """Модуль Spam - спамит сообщениями. Чтобы использовать, пиши: '.spam (кол-во сообщений) (текст)'."""
        args = utils.get_args_raw(message).split(" ")
        await message.delete()
        numb = int(args[0])
        text = " ".join(args[1:])
        for _ in range(numb):
            await message.respond(text)
        
    async def tagallcmd(self, message): #2
        """Модуль TagAll - созывает всех участников. Чтобы использовать, пиши '.tagall (текст созыва)'."""
        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        args = utils.get_args_raw(message)
        await message.delete()
        if not args:
            args = "Общий сбор!"
        chatId = message.chat_id
        users = [i for i in await message.client.get_participants(chatId) if i.bot == False and i.deleted == False]
        array = []
        for i in users:
           array.append(f"<a href=tg://user?id={i.id}>\u206c\u206f</a>")
        chunkss = list(chunks(array, 49))
        for i in chunkss:
            await message.respond(args + "".join(i))
            await sleep(0.2)
            
    async def delmsgcmd(self, message): #3
        """Модуль DelMsg - удаляет все твои сообщения в определенном чате. Чтобы использовать, пиши '.delmsg'."""
        msg = [msg async for msg in message.client.iter_messages(message.chat_id, from_user= "me")]
        for i in msg:
            await i.delete()
        await message.respond("Все сообщения удалены!")
    
    async def shipercmd(self, message):  #4
        """Модуль Shiper - шиперит участников. Чтобы использовать, пиши '.shiper' или '.shiper @юзернейм1 и @юзернейм2'."""
        args = utils.get_args_raw(message)
        chatId = message.chat_id
        if not args:
            rand = random.choices([i for i in await message.client.get_participants(chatId) if i.bot == False and i.deleted == False], k=2)
        else:
            args = args.split(" и ")
            rand = [await message.client.get_entity(args[0]), await message.client.get_entity(args[1])]
        randtext = random.randint(1, 6)
        if randtext == 1:
            return await message.respond(f"<a href=tg://user?id={rand[0].id}>{rand[0].first_name}</a> и <a href=tg://user?id={rand[1].id}>{rand[1].first_name}</a> любите друг друга!\nМур-Мур😻")
        if randtext == 2:
          return await message.edit(f"<a href=tg://user?id={rand[0].id}>{rand[0].first_name}</a> и <a href=tg://user?id={rand[1].id}>{rand[1].first_name}</a> любовная парочка!\nЧмок😘")
        if randtext == 3:
            return await message.edit(f"Пара дня❤️:\n<a href=tg://user?id={rand[0].id}>{rand[0].first_name}</a> и <a href=tg://user?id={rand[1].id}>{rand[1].first_name}</a>")
        if randtext == 4:
            return await message.edit(f"<a href=tg://user?id={rand[0].id}>{rand[0].first_name}</a> любит <a href=tg://user?id={rand[1].id}>{rand[1].first_name}</a> 😘")
        if randtext == 5:
            return await message.edit(f"<a href=tg://user?id={rand[0].id}>{rand[0].first_name}</a> пригласил на чай <a href=tg://user?id={rand[1].id}>{rand[1].first_name}</a> ☕❤️")
        if randtext == 6:
            return await message.edit(f"<a href=tg://user?id={rand[0].id}>{rand[0].first_name}</a> зашел к <a href=tg://user?id={rand[1].id}>{rand[1].first_name}</a>\n😏🔥")

    async def randcmd(self, message):  #5
        """Модуль RandNumb - выдает рандомное число. Чтобы использовать, пиши '.rand (от какого числа) (до какого числа)'."""
        args = utils.get_args_raw(message)
        if not args:
            numb1 = 0
            numb2 = 100
        else:
            numb1, numb2 = int(args.split(" ")[0]), int(args.split(" ")[1])
        await message.edit(str(random.randint(numb1, numb2)))
        
    async def згcmd(self, message):  #6
        """Модуль SavePic - сохраняет самоуничтожающееся фото. Чтобы использовать, пиши '.зг', реплеем на фото."""
        reply = await message.get_reply_message() 
        if not reply or not reply.media.ttl_seconds: return await message.edit("Реплаем на самоуничтожающееся фото! ")
        await message.delete() 
        new = io.BytesIO(await reply.download_media(bytes)) 
        new.name = reply.file.name 
        await message.client.send_file("me", new)

    async def ghoulcmd(self, message):  #7
        """Модуль IamGhoul - спамит 1000-7. Чтобы использовать, пиши '.ghoul'."""
        a = 1000
        await message.edit("Я гуль!")
        while a != 6:
            c = str(a)
            a = a - 7
            b = str(a)
            d = c + " - 7 = " + b
            await message.respond(d)

    async def mlcmd(self, message):  #8
        """Модуль ModulesLink - отправляет файл на уже установленный модуль. Чтобы использовать, пиши '.ml (название модуля)'."""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit('Нет аргументов.')
        await message.edit('Ищу...')
        try:
            f = ' '.join([x.strings["name"] for x in self.allmodules.modules if args.lower() == x.strings["name"].lower()])
            r = inspect.getmodule(next(filter(lambda x: args.lower() == x.strings["name"].lower(), self.allmodules.modules)))
            link = str(r).split('(')[1].split(')')[0]
            if "http" not in link:
                text = f"Модуль {f}:"
            else:
                text = f"<a href=\"{link}\">Ссылка</a> на {f}: <code>{link}</code>"
            out = io.BytesIO(r.__loader__.data)
            out.name = f + ".py"
            out.seek(0)
            await message.respond(text, file=out)
            await message.delete()
        except:
            return await message.edit("Произошла непредвиденная ошибка")

    async def hackcmd(self, message):  #9
        """Модуль HackChat - засоряет логи + фейк взлом. Чтобы использовать, пиши '.hack'."""
        i = 0
        while i <= 99:
            await message.edit("<b>Взлом чата выполнен на " + str(i) + "%</b>")
            i += 1
            await sleep(0.1)
        await sleep(0.3)
        await message.edit("<b>Чат успешно взломан! Его данные вы можете посмотреть в облаке Telegram.</b>")
    
    async def printcmd(self, message): #10
        """Модуль Print - по символьно отправляет отпреденный текст. Чтобы использовать, пиши '.print (текст)'."""
        text = list(utils.get_args_raw(message))
        a = ""
        for i in text:
            a += i
            await message.edit(a)
            await sleep(0.1)
            
    async def typecmd(self, message): #11
        """Модуль Type - красиво и плавно отправляет отпреденный текст. Чтобы использовать, пиши '.type (смайл/символ/тд) (текст)'."""
        msg = utils.get_args_raw(message).split(" ")
        text = list(" ".join(msg[1:]))
        smile = msg[0]
        a = ""
        b = ""
        for i in text:
            b = a + smile
            await message.edit(b)
            await sleep(0.2)
            a += i
            await message.edit(a)
    
    async def nqcmd(self, message): #12
        """Модуль NedoQuotes - генерирует картинку с цитатой из вашего текста. Чтобы использовать, пиши '.nq (реплей/текст)'."""
        chat = "@ShittyQuoteBot"
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not text and not reply:
            await message.edit("<b>Нет текста или реплая!</b>")
            return
        await message.edit("<b>Ван сек...</b>")
        async with message.client.conversation(chat) as conv:
            if text:
                try:
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=1389323591))
                    await message.client.send_message(chat, text)
                    response = await response
                except YouBlockedUserError:
                    await message.edit("<b>У тебя заблокирован @ShittyQuoteBot, чтобы модуль работал, разблокируй его!</b>")
                    return
            else:
                try:
                    user = await utils.get_user(reply)
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=1389323591))
                    await message.client.send_message(chat, f"{reply.raw_text} (с) {user.first_name}")
                    response = await response
                except YouBlockedUserError:
                    await message.edit("<b>У тебя заблокирован @ShittyQuoteBot, чтобы модуль работал, разблокируй его!</b>")
                    return
        if response.text:
            await message.client.send_message(message.to_id, f"<b> {response.text}</b>")
            await message.delete()
        if response.media:
            await message.client.send_file(message.to_id, response.media, reply_to=reply.id if reply else None)
            await message.delete()
        
    async def saycmd(self, message): #13
        """Модуль SayText - переводит написанное сообщение в голосовое сообщение. Чтобы использовать, пиши '.say (текст)'."""
        reply = await message.get_reply_message()
        await message.edit("<b>Сек.</b>")
        try:
            gTTS(text=f'{message.to_dict()["message"].split("say ")[1]}', lang='ru').save("say.ogg")
            await message.delete()
            if reply:
                await message.client.send_file(message.to_id, "say.ogg", voice_note=True, reply_to=reply.id)
            else:
                await message.client.send_file(message.to_id, "say.ogg", voice_note=True)
            os.system(f"rm -rf say.ogg")
        except:
            await message.edit("<b>Ошибка!</b>")
    
    async def whoiscmd(self, message): #14
        """Модуль WhoIs - выводит информацию о пользователе. Чтобы использовать, пиши '.whois (@юзернейм/реплей)'."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        await message.edit("<b>Получаю информацию о пользователе...</b>")
        try:
            if args:
                user = await message.client.get_entity(args if not args.isgidit() else int(args))
            else:
                user = await message.client.get_entity(reply.sender_id)
        except:
            user = await message.client.get_me()      
        user = await message.client(GetFullUserRequest(user.id))
        photo, caption = await get_info(user, message)
        await message.client.send_file(message.chat_id, photo, caption=caption, link_preview=False, reply_to=reply.id if reply else None)
        os.remove(photo)
        await message.delete()

    async def rusroulcmd(self, message): #15
        """Модуль RusRoul - игра русская рулетка(безопасно). Чтобы использовать, пиши '.rusroul'."""
        await message.edit("Выстрел...")
        rand = random.randint(1, 6)
        await sleep(1.5)
        if rand == 1:
            await message.edit("<b>Фух, тебе повезло, но больше так не рискуй!</b>")
        else:
            await message.edit("<b>К сожалению, ты проиграл(</b>")

    async def wikicmd(self, message): #16
        """Модуль Wikipedia - выдает результат из википедии. Чтобы использовать, пиши '.wiki (что найти - текст/реплей)'."""
        try: 
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "@just_zhenya_bot" 
            if not text and not reply: 
                await message.edit("<b>А эм... а что искать то...</b>") 
                return 
            if text: 
                await message.edit("<b>Ищу материал</b>") 
                async with message.client.conversation(chat) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=528677877)) 
                        await message.client.send_message(chat, "/wiki " + text) 
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply("<b>Удали из ЧС: @just_zhenya_bot</b>") 
                        return 
                    if not response.text: 
                        await message.edit("<Ещё раз пробуй</b>") 
                        return 
                    await message.delete() 
                    await message.client.send_message(message.to_id, response.text) 
            if reply: 
                await message.edit("<b>Сек...</b>") 
                async with message.client.conversation(chat) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=528677877)) 
                        await message.client.send_message(chat, reply) 
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply("<b>Удали из ЧС: @just_zhenya_bot</b>") 
                        return 
                    if not response.text: 
                        await message.edit("<Пробуй еще раз </b>") 
                        return 
                    await message.delete() 
                    await message.client.send_message(message.to_id, response.text) 
        except TimeoutError: 
            return await message.edit("<b>Я ничего не нашел(((</b>")

    async def tscmd(self, message): # 17
        """Модуль TextS - выводит каждую букву в слове. Чтобы использовать, пиши '.ts (текст)'."""
        text = utils.get_args_raw(message).replace(" ", "ᅠ")
        listtxt = list(text)
        for i in listtxt:
            await message.edit(i)
            await sleep(0.3)
        await message.edit(text)
        
    async def tecmd(self, message): # 18
        """Модуль TextEdit - редактирует ваше сообщение через опреденное время или удаляет его. Чтобы использовать для редактирования, пиши '.te (время в минутах) (текст до) | (текст после)' или для удаления, пиши '.te (время в минутах) (текст)'."""
        text = utils.get_args_raw(message).split(" ")
        time = int(text[0])
        text = " ".join(text[1:]).split("|")
        if len(text) == 2:
            msg1 = text[0]
            msg2 = text[1]
            await message.edit(msg1)
            await sleep(time)
            await message.edit(msg2)
        elif len(text) == 1:
            msg1 = text[0]
            await message.edit(msg1)
            await sleep(time)
            await message.delete()
        else:
            await message.edit("<b>Попробуй еще раз(</b>")
        
    async def onlinecmd(self, message): #19
        """Модуль Online - делает вечный онлайн. Чтобы использовать, пиши '.online'."""
        if not self.db.get("Eternal Online", "status"):
            self.db.set("Eternal Online", "status", True)
            await message.edit("Вечный онлайн включен.")
            while self.db.get("Eternal Online", "status"):
                await message.client(__import__("telethon").functions.account.UpdateStatusRequest(offline=False))
                await sleep(60)
        else:
            self.db.set("Eternal Online", "status", False)
            await message.edit("Вечный онлайн выключен.")
            
    async def fsqcmd(self, message: Message): #20
        """Модуль SQuotes (Часть модуля) - создает стикер из сообщения. Чтобы использовать, пиши реплеем '.fsq (текст)'."""
        args: str = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not (args or reply):
            return await utils.answer(
                message, self.strings["no_args_or_reply"])
        m = await utils.answer(
            message, self.strings["processing"])
        try:
            payload = await self.fakequote_parse_messages(args, reply)
        except (IndexError, ValueError):
            return await utils.answer(
                m, self.strings["args_error"].format(
                    message.text)
            )
        if len(payload) > self.settings["max_messages"]:
            return await utils.answer(
                m, self.strings["too_many_messages"].format(
                    self.settings["max_messages"])
            )
        payload = {
            "messages": payload,
            "quote_color": self.settings["bg_color"],
            "text_color": self.settings["text_color"]
        }
        if self.settings["debug"]:
            file = open("SQuotesDebug.json", "w")
            json.dump(
                payload, file, indent = 4,
                ensure_ascii = False,
            )
            await message.respond(
                file = file.name)
        await utils.answer(
            m, self.strings["api_processing"])
        r = await self._api_request(payload)
        if r.status_code != 200:
            return await utils.answer(
                m, self.strings["api_error"])
        quote = io.BytesIO(r.content)
        quote.name = "SQuote.webp"
        await utils.answer(m, quote)
        return await m[-1].delete()
    #########################################################################################################
    async def fakequote_parse_messages(self, args: str, reply: Message): #хуита fsq
        async def get_user(args: str):
            args_, text = args.split(), ""
            user = await self.client.get_entity(
                int(args_[0]) if args_[0].isdigit() else args_[0])
            if len(args_) < 2:
                user = await self.client.get_entity(
                    int(args) if args.isdigit() else args)
            else:
                text = args.split(maxsplit = 1)[1]
            return user, text
        if reply or reply and args:
            user = reply.sender
            name, avatar = await self.get_profile_data(user)
            text = args or ""
        else:
            messages = []
            for part in args.split("; "):
                user, text = await get_user(part)
                name, avatar = await self.get_profile_data(user)
                reply_id = reply_name = reply_text = None
                if " -r " in part:
                    user, text = await get_user(''.join(part.split(" -r ")[0]))
                    user2, text2 = await get_user(''.join(part.split(" -r ")[1]))
                    name, avatar = await self.get_profile_data(user)
                    name2, _ = await self.get_profile_data(user2)
                    reply_id = user2.id
                    reply_name = name2
                    reply_text = text2
                messages.append(
                    {
                        "text": text,
                        "media": None,
                        "entities": None,
                        "author": {
                            "id": user.id,
                            "name": name,
                            "avatar": avatar,
                            "rank": ""
                        },
                        "reply": {
                            "id": reply_id,
                            "name": reply_name,
                            "text": reply_text
                        }
                    }
                )
            return messages
        return [
            {
                "text": text,
                "media": None,
                "entities": None,
                "author": {
                    "id": user.id,
                    "name": name,
                    "avatar": avatar,
                    "rank": ""
                },
                "reply": {
                    "id": None,
                    "name": None,
                    "text": None
                }
            }
        ]
    async def get_profile_data(self, user: types.User): #хуита fsq
        avatar = await self.client.download_profile_photo(user.id, bytes)
        return telethon.utils.get_display_name(user), \
            base64.b64encode(avatar).decode() if avatar else None          
    def get_settings(self, force: bool = False): #хуита fsq
        settings: dict = self.db.get(
            "SQuotes", "settings", {}
        )
        if not settings or force:
            settings.update(
                {
                    "max_messages": 15,
                    "bg_color": "#162330",
                    "text_color": "#fff",
                    "debug": False
                }
            )
            self.db.set("SQuotes", "settings", settings)

        return settings
    async def _api_request(self, data: dict): #хуита fsq
        return await utils.run_sync(
            requests.post, self.api_endpoint, json = data)           

async def get_info(user, message): #хуита whois
    """Подробная информация о пользователе."""
    uuser = user.user
    user_photos = await message.client(GetUserPhotosRequest(user_id=uuser.id, offset=42, max_id=0, limit=100))
    user_photos_count = "У пользователя нет аватарки."
    try:
        user_photos_count = user_photos.count
    except:
        pass
    user_id = uuser.id
    first_name = uuser.first_name or "Пользователь не указал имя."
    last_name = uuser.last_name or "Пользователь не указал фамилию."
    username = "@" + uuser.username or "У пользователя нет юзернейма."
    user_bio = user.about or "У пользователя нет информации о себе."
    common_chat = user.common_chats_count
    is_bot = "Да" if uuser.bot else "Нет"
    restricted = "Да" if uuser.restricted else "Нет"
    verified = "Да" if uuser.verified else "Нет"
    photo = await message.client.download_profile_photo(user_id, str(user_id) + ".jpg", download_big=True)
    caption = (f"<b>ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ:</b>\n\n<b>Имя:</b> {first_name}\n<b>Фамилия:</b> {last_name}\n<b>Юзернейм:</b> {username}\n<b>ID:</b> <code>{user_id}</code>\n<b>Бот:</b> {is_bot}\n<b>Ограничен:</b> {restricted}\n<b>Верифицирован:</b> {verified}\n\n<b>О себе:</b> \n<code>{user_bio}</code>\n\n<b>Кол-во аватарок в профиле:</b> {user_photos_count}\n<b>Общие чаты:</b> {common_chat}\n<b>Пермалинк:</b> <a href=\"tg://user?id={user_id}\">клик</a>")
    return photo, caption
