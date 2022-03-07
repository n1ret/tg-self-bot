import asyncio
import logging
import random
from configparser import ConfigParser
from datetime import datetime
from time import sleep
from re import match

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageIdInvalid, ReactionInvalid

#logging config
logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.INFO
)

#config
app = Client(input('Введите имя сессии: '))
prefix = '.'
enableLogDeletedByFreeze = False

#self bot logic
#bot global var
enable = False
enableMirrorsChats = []
enableFullMirrorsChats = []
freezedChats = {}

#help
@app.on_message(filters.command("help", prefixes=prefix) & filters.me)
def f(_, msg):
    logging.info('Help command used')
    commandList = {
        'Print by symbol': 'pr <simbol> <message>',
        'eHack pentagon': 'hackPen',
        'Emoji mood up': 'emoji',
        'Mirror any user': 'mirror <message>',
        'Toggle mirror in the chat': 'toggleMirror',
        'Toggle mirror to all messages in the chat': 'fullMirror',
        'Delete messages with current text': 'clear <num last msg> <message>',
        'Del not your messages': 'freeze <id user freezed | any>',
        'Get id chat or last message': 'getId <chat/last>',
        'Repeat message': 'rep <repeat count> <delay seconds> <message>',
        'Spam message': 'spam <message>',
        'React at messages': 'react <count of msgs | all> <reaction> [channel name]',
        'Stop any command': 'stop'
    }
    spl = msg.text.split(maxsplit=1)
    msgHelpText = '**Name** - __Format__\n\n'
    for name in commandList:
        form = commandList[name]
        if name[0] != 'e' or len(spl) > 1:
            if name[0] == 'e':
                name = name[1:]
            #add name to msg
            msgHelpText += f'**{name}** - '
            #add format to msg
            msgHelpText += f'__{prefix}{form}__\n'

    msg.edit(msgHelpText, parse_mode='markdown')


#pr
@app.on_message(filters.command("pr", prefixes=prefix) & filters.me)
def f(_, msg):
    logging.info('Command pr started')
    spl = msg.text.split(" ", maxsplit=2)
    if len(spl) == 3:
        orig_text = spl[2]
        text = orig_text
        tbp = ""
        typing_symbol = spl[1]
        while tbp != orig_text:
            try:
                msg.edit(tbp + typing_symbol)
                sleep(0.1)
                tbp = tbp + text[0]
                text = text[1:]

                msg.edit(tbp)
                sleep(0.1)
            except FloodWait as e:
                sleep(e.x)
            except MessageIdInvalid:
                break
    else:
        msg.delete()

    logging.info('Command pr done')


#freeze
@app.on_message(filters.command("freeze", prefixes=prefix) & filters.me)
def f(_, msg):
    global freezedChats
    spl = msg.text.split(maxsplit=1)
    if len(spl) == 2:
        if not match(r"^(any|\d+)$", spl[1]):
            msg.edit("Please give user_id or \"any\"")
        else:
            chatName = msg.chat.username or msg.chat.title or msg.chat.first_name
            if msg.chat.id not in freezedChats:
                freezedChats[msg.chat.id] = []
            if spl[1] in freezedChats[msg.chat.id]:
                freezedChats[msg.chat.id].remove(spl[1])
                if not freezedChats[msg.chat.id]:
                    freezedChats.pop(msg.chat.id)
                logging.info(f"Freeze disabled in {chatName} for {spl[1]}")
                msg.edit("Freeze disabled")
            else:
                freezedChats[msg.chat.id].append(spl[1])
                logging.info(f"Freeze enabled in {chatName} for {spl[1]}")
                msg.edit("Freeze enabled")
    else:
        msg.edit("Argument must be user id or \"any\"")
    sleep(1)
    msg.delete()


#getId
@app.on_message(filters.command("getId", prefixes=prefix) & filters.me)
def f(_, msg):
    spl = msg.text.split(maxsplit=1)
    if len(spl) == 2:
        if spl[1] == "chat":
            msg.edit(msg.chat.id)
        elif spl[1] == "last":
            m = app.get_history(msg.chat.id, limit=2)[1]
            if m.from_user:
                msg.edit(m.from_user.id)
            else:
                msg.edit("Последнее сообщение отправлено каналом")
                sleep(2)
                msg.delete()
        else:
            msg.delete()
    else:
        msg.delete()


#hackPen
@app.on_message(filters.command("hackPen", prefixes=prefix) & filters.me)
async def f(_, msg):
    logging.info('Command hack used')
    points = '.'
    percent = 0
    while percent <= 100:
        await msg.edit('Взлом zone-51 ' + str(percent) + '%' + points)
        percent = percent + random.randint(10, 13)
        if points == '.':
            points = '..'
        elif points == '..':
            points = '...'
        elif points == '...':
            points = '.'
        sleep(0.05)
    await msg.edit('Zone-51 взломана')
    percent = 0
    points = '👽'
    await asyncio.sleep(3)
    while percent <= 100:
        try:
            await msg.edit(
                'Получение сведений о инопрешельцах ' + str(percent) +
                '%' + points)
            percent = percent + random.randint(9, 15)
            if points == '👽':
                points = '👽👽'
            elif points == '👽👽':
                points = '👽👽👽'
            elif points == '👽👽👽':
                points = '👽'
            await asyncio.sleep(0.05)
        except FloodWait as f:
            await asyncio.sleep(f.x)
    await msg.edit('Сведенья о инопрешеленцах получены')
    await asyncio.sleep(1)
    await msg.edit('**РЕН ТВ** >>  __Пасаси__')
    await asyncio.sleep(0.5)
    await msg.delete()


#emoji
@app.on_message(filters.command("emoji", prefixes=prefix) & filters.me)
async def f(_, msg):
    logging.info('Command emoji used')
    em = '😞🙁😏😀😄😅🤣😂'
    for _ in range(10):
        for i in em:
            await msg.edit(i, parse_mode=None)
            await asyncio.sleep(0.5)
    await msg.delete()


#mirror
@app.on_message(filters.command("mirror", prefixes=prefix) & ~filters.me)
def f(_, msg):
    global enableMirrorsChats
    spl = msg.text.split(maxsplit=1)
    if (
        len(spl) == 2 and spl[1][0] != prefix and
        msg.chat.id in enableMirrorsChats
    ):
        msg.delete()
        name = msg.from_user.username or msg.from_user.first_name
        logging.info(f"Command mirror used by {name}")
        app.send_message(msg.chat.id, spl[1])


@app.on_message(filters.command("toggleMirror", prefixes=prefix) & filters.me)
def f(_, msg):
    global enableMirrorsChats
    chatName = msg.chat.username or msg.chat.title or msg.chat.first_name
    if msg.chat.id not in enableMirrorsChats:
        enableMirrorsChats.append(msg.chat.id)
        logging.info(f"Mirror enabled in {chatName}")
        msg.edit("Mirror enabled")
    else:
        enableMirrorsChats.remove(msg.chat.id)
        logging.info(f"Mirror disabled in {chatName}")
        msg.edit("Mirror disabled")
    sleep(0.5)
    msg.delete()


#fullMirror
@app.on_message(filters.command("fullMirror", prefixes=prefix) & filters.me)
def f(_, msg):
    global enableFullMirrorsChats
    chatName = msg.chat.username or msg.chat.title or msg.chat.first_name
    if msg.chat.id not in enableFullMirrorsChats:
        enableFullMirrorsChats.append(msg.chat.id)
        logging.info(f"Full mirror enabled in {chatName}")
        msg.edit("Full mirror enabled")
    else:
        enableFullMirrorsChats.remove(msg.chat.id)
        logging.info(f"Full mirror disabled in {chatName}")
        msg.edit("Full mirror disabled")
    sleep(0.5)
    msg.delete()


#clear
@app.on_message(filters.command("clear", prefixes=prefix) & filters.me)
def f(_, msg):
    msg.delete()
    spl = msg.text.split(maxsplit=2)
    if 2 <= len(spl) <= 3:
        chatName = msg.chat.username or msg.chat.title or msg.chat.first_name
        msgs = app.iter_history(msg.chat.id, limit=int(spl[1]))
        d = 0
        deleteMsgs = []
        if len(spl) == 3:
            for i in msgs:
                if i.text == spl[2]:
                    d += 1
                    deleteMsgs.append(i.message_id)
            logging.info(
                f"From {chatName} deleted {d} messages with text: {spl[2]}")
        if len(spl) == 2:
            for i in msgs:
                d += 1
                deleteMsgs.append(i.message_id)
            logging.info(f"From {chatName} deleted {d} messages")
        app.delete_messages(msg.chat.id, deleteMsgs)


#rep
@app.on_message(filters.command("rep", prefixes=prefix) & filters.me)
def f(_, msg):
    global enable
    logging.info('Command rep started')
    spl = msg.text.split(" ", maxsplit=3)
    if len(spl) == 4:
        msg.delete()
        enable = True
        for i in range(int(spl[1])):
            while True:
                try:
                    app.send_message(msg.chat.id, spl[3])
                    break
                except FloodWait as e:
                    sleep(e.x)
            if not enable:
                break
            if i != int(spl[1]) - 1:
                sleep(float(spl[2]))
        m = app.send_message(msg.chat.id, 'Done')
        sleep(1)
        m.delete()
    else:
        msg.delete()

    logging.info('Command rep done')


#spam
@app.on_message(filters.command('spam', prefixes=prefix) & filters.me)
async def f(_, msg):
    global enable
    logging.info('Command spam started')
    spl = msg.text.split(" ", maxsplit=1)
    await msg.delete()
    if len(spl) == 2:
        enable = True
        while enable:
            try:
                await app.send_message(msg.chat.id, spl[1])
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except:
                pass

    logging.info('Command spam done')


# react
def is_not_chosen(reactions):
    for reaction in reactions:
        if reaction.chosen:
            return False
    return True


@app.on_message(filters.command('react', prefixes=prefix) & filters.me)
async def fire(_, msg):
    await msg.delete()
    global enable
    enable = True
    spl = msg.text.split(maxsplit=3)
    if len(spl) < 3:
        return
    kwargs = {}
    if spl[1] != 'all':
        kwargs['limit'] = int(spl[1])
    reaction = spl[2]
    logging.info('Reactions start')
    pk = msg.chat.id
    if len(spl) == 4:
        async for dialog in app.iter_dialogs():
            chat = dialog.chat
            if any((chat.username==spl[3], chat.title==spl[3], chat.first_name==spl[3])):
                pk = chat.id
                break
        else:
            error_msg = await app.send_message(msg.chat.id, 'Чат не найден')
            await error_msg.delete()
            return
    async for msg in app.iter_history(pk, **kwargs):
        if msg.service:
            continue
        if not enable:
            break
        
        reactions = []
        if msg.reactions:
            reactions = msg.reactions
        if is_not_chosen(reactions):
            try:
                await msg.react(reaction)
            except ReactionInvalid:
                error_msg = await app.send_message(msg.chat.id, 'Реакция не доступна')
                await asyncio.sleep(0.25)
                await error_msg.delete()
                break
            except Exception:
                logging.error(f'Message not campability for reactions: {msg}')
    logging.info('Reactions end')


#stop
@app.on_message(filters.command("stop", prefixes=prefix) & filters.me)
def f(_, msg):
    msg.delete()

    global enable
    enable = False


#any msg
@app.on_message()
async def f(_, msg):
    if not msg.from_user:
        return

    #freeze
    global freezedChats
    global enableLogDeletedByFreeze

    if msg.chat.id in freezedChats:
        if not msg.from_user.is_self and (str(msg.from_user.id) in freezedChats[msg.chat.id] or "any" in freezedChats[msg.chat.id]):
            await msg.delete()
        if enableLogDeletedByFreeze:
            chatName = msg.chat.username or msg.chat.title or msg.chat.first_name
            name = msg.from_user.username or msg.from_user.first_name
            unix = msg.date
            date = datetime.utcfromtimestamp(unix)
            with open(f"{chatName}_delMsg.log", "a+") as f:
                f.write(f"[{name}: {date} UTC]{msg.text}\n")

    #fullMirror
    global enableFullMirrorsChats
    if msg.chat.id in enableFullMirrorsChats and not msg.from_user.is_self:
        name = msg.from_user.username or msg.from_user.first_name
        logging.debug(f"Full mirror by {name}: {msg.text}")
        await msg.copy(msg.chat.id)


logging.info('Self bot starting')
app.run()

