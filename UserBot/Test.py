from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageIdInvalid
from configparser import ConfigParser
from time import sleep
import random

config = ConfigParser()
config.read('config.ini')
app = Client(config['session']['name'])

# prefix set
prefix = config['session']['prefix']


@app.on_message(filters.command("pr", prefixes=prefix) & filters.me)
def pr(_, msg):
    spl = msg.text.split(" ", maxsplit=2)
    if len(spl) == 3:
        orig_text = spl[2]
        text = orig_text
        tbp = ""
        typing_symbol = spl[1]
        while tbp != orig_text:
            try:
                msg.edit(tbp + typing_symbol)
                sleep(0.05)
                tbp = tbp + text[0]
                text = text[1:]

                msg.edit(tbp)
                sleep(0.05)
            except FloodWait as e:
                sleep(e.x)
            except MessageIdInvalid:
                break
    else:
        msg.delete()


@app.on_message(filters.command("hack", prefixes=prefix) & filters.me)
def hack(_, msg):
    points = '.'
    percent = 0
    while percent <= 100:
        msg.edit('Взлом zone-51 ' + str(percent) + '%' + points)
        percent = percent + random.randint(10, 13)
        if points == '.':
            points = '..'
        elif points == '..':
            points = '...'
        elif points == '...':
            points = '.'
        sleep(0.05)
    msg.edit('Zone-51 взломана')
    percent = 0
    points = '👽'
    sleep(3)
    while percent <= 100:
        try:
            msg.edit('Получение сведений о инопрешельцах ' + str(percent) + '%' + points)
            percent = percent + random.randint(9, 15)
            if points == '👽':
                points = '👽👽'
            elif points == '👽👽':
                points = '👽👽👽'
            elif points == '👽👽👽':
                points = '👽'
            sleep(0.05)
        except FloodWait as e:
            sleep(e.x)
    msg.edit('Сведенья о инопрешеленцах получены')
    sleep(1)
    msg.edit('РЕН ТВ>Пасаси')
    sleep(0.5)
    msg.delete()


@app.on_message(filters.command("rep", prefixes=prefix) & filters.me)
def rep(_, msg):
    spl = msg.text.split(" ", maxsplit=3)
    if len(spl) == 4:
        msg.delete()
        for x in range(int(spl[1])):
            sleep(float(spl[2]))
            while True:
                try:
                    app.send_message(msg.chat.id, spl[3])
                    break
                except FloodWait as f:
                    sleep(f)
        m = app.send_message(msg.chat.id, 'Done')
        sleep(2)
        m.delete()
    else:
        msg.delete()


@app.on_message(filters.command('spam', prefixes=prefix) & filters.me)
def spam(_, msg):
    spl = msg.text.split(" ", maxsplit=1)
    if len(spl) == 2:
        msg.delete()
        while True:
            try:
                app.send_message(msg.chat.id, spl[1])
            except FloodWait:
                break
    else:
        msg.delete()


app.run()
