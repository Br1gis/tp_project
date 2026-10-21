import datetime
import random
import time

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto, InputFile, FSInputFile, ChatPermissions
from aiogram.filters import CommandStart, Command, CommandObject, IS_NOT_MEMBER, IS_MEMBER, ChatMemberUpdatedFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functions import *
from cfg import token

import sqlite3

vip_list = [5232661152, 5131497362]

bot = Bot(token=token)
from time import strptime

router = Router()
router.message.filter(F.chat.type != 'private')

class ChangeDescription(StatesGroup):
    new_desc = State()

class ChangeAvatar(StatesGroup):
    new_avatar = State()

class ChangeTag(StatesGroup):
    new_tag = State()

@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def hello_handler(event: ChatMemberUpdated):
    await event.answer(f'Ку дарова, @{event.from_user.username}')


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer('Привет)')

@router.message(Command('kiss'))
async def kiss(message: Message, command: CommandObject):
    usertokiss = command.args
    if usertokiss is None:
        await message.reply('Ты хоть кого целуешь то напиши')
    elif usertokiss == f'@{message.from_user.username}':
        await message.reply_photo(photo='AgACAgIAAxkBAAO-alZ6cioAAfNklFAbaL-No8iEMDYnAALuHGsbLkWxSvroR15lUimZAQADAgADeAADPQQ', caption=f'@{message.from_user.username} поцеловал(а) сам себя...')
    else:
        await message.reply_photo(
            photo='AgACAgIAAxkBAAO-alZ6cioAAfNklFAbaL-No8iEMDYnAALuHGsbLkWxSvroR15lUimZAQADAgADeAADPQQ',
            caption=f'@{message.from_user.username} поцеловал(а) {usertokiss} <3')


@router.message(Command('handshake'))
async def handshake(message: Message, command: CommandObject):
    usertoshake = command.args
    if usertoshake is None:
        await message.reply('Ты хоть кому руку жмёшь напиши')
    elif usertoshake == f'@{message.from_user.username}':
        photo = open('handshakephoto.jpg', 'rb').read()
        imgfile = BufferedInputFile(file=photo, filename=f"{usertoshake}hand{message.from_user.username}.jpg")
        await message.reply_photo(photo=imgfile, caption=f'@{message.from_user.username} пожал свою же руку...?')
    else:
        photo = open('handshakephoto.jpg', 'rb').read()
        imgfile = BufferedInputFile(file=photo, filename=f"{usertoshake}hand{message.from_user.username}.jpg")
        await message.reply_photo(photo=imgfile, caption=f'@{message.from_user.username} и {usertoshake} пожали руки')

@router.message(Command('pat'))
async def patpat(message: Message, command: CommandObject):
    usertoshake = command.args
    if usertoshake is None:
        await message.reply('Ты хоть кого гладишь напиши')
    elif usertoshake == f'@{message.from_user.username}':
        photo = open('patpatphoto.png', 'rb').read()
        imgfile = BufferedInputFile(file=photo, filename=f"{usertoshake}pat{message.from_user.username}.png")
        await message.reply_photo(photo=imgfile, caption=f'@{message.from_user.username} погладил сам себя...?')
    else:
        photo = open('patpatphoto.png', 'rb').read()
        imgfile = BufferedInputFile(file=photo, filename=f"{usertoshake}pat{message.from_user.username}.png")
        await message.reply_photo(photo=imgfile, caption=f'@{message.from_user.username} погладил по головке {usertoshake}')

@router.message(Command('punch'))
async def punch(message: Message, command: CommandObject):
    usertopunch = command.args
    if usertopunch is None:
        await message.reply('Ты хоть кого бьешь напиши')
    elif usertopunch == f'@{message.from_user.username}':
        photo = open('punchphoto.jpg', 'rb').read()
        imgfile = BufferedInputFile(file=photo, filename=f"{usertopunch}punch{message.from_user.username}.jpg")
        await message.reply_photo(photo=imgfile, caption=f'@{message.from_user.username} ударил сам себя...?')
    else:
        photo = open('punchphoto.jpg', 'rb').read()
        imgfile = BufferedInputFile(file=photo, filename=f"{usertopunch}punch{message.from_user.username}.jpg")
        await message.reply_photo(photo=imgfile, caption=f'@{message.from_user.username} со всего размаху оформил по лицу {usertopunch}')

@router.message(Command('coinflip'))
async def coinflip(message: Message, command: CommandObject):
    userside = command.args.lower()
    if userside == 'орел':
        userside = userside.replace('е', 'ё')
    if userside in ['орёл', 'решка']:
        botside = random.choice(['орёл', 'решка'])
        if userside == botside:
            await message.reply(f'*Твой выбор:* {userside}\n*Выпало:* {botside}\n*Ты победил(а)*', parse_mode='markdown')
        else:
            await message.reply(f'*Твой выбор:* {userside}\n*Выпало:* {botside}\n*Ты проиграл(а)*', parse_mode='markdown')
    else:
        await message.reply('У тебя была одна задача... Давай подскажу: либо орёл, либо решка')


@router.message(Command('dice'))
async def dice(message: Message, command: CommandObject):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    try:
        userchoice = command.args.lower().split()[0]
        userbet = command.args.lower().split()[1]
        try:
            userbet = int(userbet)
            for balance in sql.execute('SELECT balance FROM users WHERE user_id = ?', (message.from_user.id,)):
                if int(balance[0]) < userbet:
                    await message.answer('Маловато у тебя деньжат для таких ставок')
                elif userbet <= 0:
                    await message.reply('Ты давай тут не шали')
                else:
                    sent_message = await message.answer_dice()
                    dice_value = sent_message.dice.value
                    if int(dice_value) % 2 == 0:
                        result = 'чет'
                    else:
                        result = 'нечет'
                    if result == userchoice.replace('ё', 'е'):
                        await message.reply(f'*Твой выбор:* {userchoice}\n*Выпало:* {dice_value}\n*Ты победил(а)*',
                                            parse_mode='markdown')
                        sql.execute('UPDATE users SET balance = ? WHERE user_id = ?', (int(balance[0])+userbet, message.from_user.id))
                        db.commit()
                        break
                    else:
                        await message.reply(f'*Твой выбор:* {userchoice}\n*Выпало:* {dice_value}\n*Ты проиграл(а)*',
                                            parse_mode='markdown')
                        sql.execute('UPDATE users SET balance = ? WHERE user_id = ?',
                                    (int(balance[0]) - userbet, message.from_user.id))
                        db.commit()
                        break
        except:
            await message.reply('Фигню ты какую то мне вместо ставки написал. Она должна быть целым числом')
    except:
        await message.reply('Не так написал, вот как надо: /dice <чёт/нечёт> <ставка>')
    sql.close()


@router.message(Command('give'))
async def give_money(message: Message, command: CommandObject):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    try:
        usertogive = command.args.split()[0].replace('@', '')
        amount = int(command.args.split()[1])
        #print(amount, usertogive)
        sql.execute('SELECT balance FROM users WHERE user_id = ?', (message.from_user.id,))
        balance = sql.fetchone()[0]
        #print(balance)
        sql.execute('SELECT balance FROM users WHERE username = ?', (usertogive,))
        balance2 = sql.fetchone()[0]
        #print(balance2)
        if amount > int(balance):
            await message.reply('У тебя самого столько нет XD')
        elif amount <= 0:
            await message.reply('Давай тут не шали')
        else:
            sql.execute('UPDATE users SET balance = ? WHERE user_id = ?',(int(balance) - amount, message.from_user.id,))
            db.commit()
            sql.execute('UPDATE users SET balance = ? WHERE username = ?', (int(balance2) + amount, usertogive,))
            db.commit()
            await message.reply(f'💵 *Успешно перевел {amount} деняг*', parse_mode='markdown')

    except Exception as e:
        print(e)
        await message.reply('Ну давай снова помогу: /give <пользователь> <кол-во бабла>')
    sql.close()

@router.message(Command('add'))
async def add_money(message: Message, command: CommandObject):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    try:
        usertogive = command.args.split()[0].replace('@', '')
        amount = int(command.args.split()[1])
        #print(amount, usertogive)
        sql.execute('SELECT balance FROM users WHERE user_id = ?', (message.from_user.id,))
        balance = sql.fetchone()[0]
        #print(balance)
        #print(balance2)
        if str(message.from_user.id) == '5232661152':
            sql.execute('UPDATE users SET balance = balance + ? WHERE username = ?', (amount, usertogive,))
            db.commit()
            await message.reply(f'💵 *Успешно добавил {amount} деняг*', parse_mode='markdown')
        else:
            await message.reply('А тебе нельзя')

    except Exception as e:
        print(e)
        await message.reply('Ну давай снова помогу: /add <пользователь> <кол-во бабла>')
    sql.close()

@router.message(Command('take'))
async def remove_money(message: Message, command: CommandObject):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    try:
        usertogive = command.args.split()[0].replace('@', '')
        amount = int(command.args.split()[1])
        #print(amount, usertogive)
        sql.execute('SELECT balance FROM users WHERE user_id = ?', (message.from_user.id,))
        balance = sql.fetchone()[0]
        #print(balance)
        #print(balance2)
        if str(message.from_user.id) == '5232661152':
            sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (amount, usertogive,))
            db.commit()
            await message.reply(f'💵 *Успешно убрал {amount} деняг*', parse_mode='markdown')
        else:
            await message.reply('А тебе нельзя')

    except Exception as e:
        print(e)
        await message.reply('Ну давай снова помогу: /take <пользователь> <кол-во бабла>')
    sql.close()

@router.message(Command('mute'))
async def mute(message: Message, command: CommandObject):
    if message.from_user.id in vip_list:
        try:
            if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return
            mute_time = command.args.split()[0]
            mute_reason = ' '.join(command.args.split()[1:])
            dt = datetime.datetime.now() + datetime.timedelta(minutes=int(mute_time))
            mute_time_stamp = int(dt.timestamp())
            user_to_mute_id = message.reply_to_message.from_user.id
            user_to_mute = message.reply_to_message.from_user.username
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_to_mute_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=mute_time_stamp
            )
            await message.reply(f'<b>Успешно заткнул @{user_to_mute}</b>\n\n<b>Причина: </b>{mute_reason}\n\nВремя мута: {mute_time} мин', parse_mode='html')
        except Exception as e:
            await message.reply('*Что-то пошло не так*', parse_mode='markdown')
    else:
        await message.reply('А тебе нельзя')


@router.message(Command('kill'))
async def ban(message: Message, command: CommandObject):
    if message.from_user.id in vip_list:
        try:
            if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return
            user_to_ban = message.reply_to_message.from_user.username
            kill_reason = ' '.join(command.args.split()[0:])

            user_to_ban_id = message.reply_to_message.from_user.id
            await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_to_ban_id)
            await message.reply(
                f'<b>Успешно обнулил @{user_to_ban}</b>\n\n<b>Причина: </b>{kill_reason}\n\n',
                parse_mode='html')
        except Exception as e:
            await message.reply('*Что-то пошло не так*', parse_mode='markdown')
    else:
        await message.reply('А тебе нельзя')



@router.message(Command('shop'))
async def show_shop(message: Message):
    shop_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Кастомный тег - 5000💵', callback_data=f'buytag:{message.from_user.username}')],
        [InlineKeyboardButton(text='Энергос - 200💵', callback_data=f'buyenerg:{message.from_user.username}')],
        [InlineKeyboardButton(text='Гамбургер - 300💵', callback_data=f'buyburger:{message.from_user.username}')],
    ])
    await message.reply('*Добро пожаловать в магазинчик!*', parse_mode='markdown', reply_markup=shop_menu)

@router.message(Command('duel'))
async def duel(message: Message, command: CommandObject):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    try:
        list_of_args = command.args.split()
        usertoduel = list_of_args[0].replace('@', '')
        bet = int(list_of_args[1])
        if bet <= 0:
            await message.reply('Ты давай тут не шали')
        else:
            if usertoduel == message.from_user.username:
                await message.reply(f'Ты сам себя то не бей брадок')
            else:
                sql.execute('SELECT balance FROM users WHERE user_id = ?', (message.from_user.id,))
                balance1 = sql.fetchone()[0]
                sql.execute('SELECT balance FROM users WHERE username = ?', (usertoduel,))
                balance2 = sql.fetchone()[0]
                if balance1 > bet and balance2 > bet:
                    duel_menu = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text = '❌ Отказаться', callback_data = f'declineduel:{usertoduel}')],
                        [InlineKeyboardButton(text = '✅ Принять вызов', callback_data = f'agreeduel:{usertoduel}:{message.from_user.username}:{bet}')],
                    ])
                    await message.reply(f'@{usertoduel}, @{message.from_user.username} вызывает тебя на дуэль\n\n<b>Ставка: </b>{bet}', reply_markup = duel_menu, parse_mode='HTML')
                else:
                    await message.reply(f'*У кого то из вас маловато деньжат для такой ставки*', parse_mode='markdown')
    except Exception as e:
        print(e)
        await message.reply('Либо ты неправильно написал, либо такого брадка в нашей компашке нет, если что напомню: /duel <оппонент> <ставка>')
    sql.close()


@router.message(Command('marry'))
async def marry(message: Message, command: CommandObject):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    try:
        usertomarry = command.args.split()
        if len(usertomarry) > 1:
            await message.reply('Давай тут без гаремов лады?')
        else:
            usertomarry = usertomarry[0].replace('@', '')
            sql.execute('SELECT partner FROM users WHERE user_id = ?', (message.from_user.id,))
            marrystatus1 = sql.fetchone()[0]
            sql.execute('SELECT partner FROM users WHERE username = ?', (usertomarry,))
            marrystatus2 = sql.fetchone()[0]
            print(marrystatus1, marrystatus2)
            marry_choice = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='❌ Отказать', callback_data=f'declinemarry:{usertomarry}:{message.from_user.username}')],
                [InlineKeyboardButton(text='✅ Согласиться', callback_data=f'agreemarry:{usertomarry}:{message.from_user.username}')],
            ])
            if marrystatus1 == 'нема' and marrystatus2 == 'нема':
                await message.answer(f'@{usertomarry}, @{message.from_user.username} делает вам предложение руки и сердца', reply_markup=marry_choice)
            else:
                await message.reply('Кажется кто-то из вас уже в браке')
    except Exception as e:
        print(e)
        await message.reply('Ну давай снова помогу: /marry <твоя любовь всей жизни>')
    sql.close()


@router.message(Command('divorce'))
async def divorce(message: Message):
    db = sqlite3.connect('base.db')
    sql = db.cursor()

    sql.execute('SELECT partner FROM users WHERE user_id = ?', (message.from_user.id,))
    marrystatus1 = sql.fetchone()[0]
    try:
        sql.execute('SELECT partner FROM users WHERE username = ?', (marrystatus1,))
        marrystatus2 = sql.fetchone()[0]
        print(marrystatus1, marrystatus2)
        divorce_choice = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='❌ Отмена', callback_data=f'canceldivorce:{message.from_user.username}')],
            [InlineKeyboardButton(text='✅ Уверен(а)',
                                  callback_data=f'agreedivorce:{marrystatus1}:{message.from_user.username}')],
        ])
        await message.reply('*Ты уверен(а)?*', parse_mode='markdown', reply_markup=divorce_choice)


    except Exception as e:
        await message.reply('Да ты и не в браке брадок...')
        print(e)
    sql.close()


@router.message(Command('reg'))
async def register(message: Message):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    sql.execute('SELECT username FROM users WHERE user_id = ?', (message.from_user.id,))
    if sql.fetchone() is None:
        with open('defphoto.png', 'rb') as f:
            image_data = f.read()
        print(image_data)
        sql.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (message.from_user.id, message.from_user.username, None, 0, image_data, 'нема', None, 1, 0, 0, 50))
        db.commit()
        await message.reply('*Занёс тебя браток*', parse_mode='markdown')
    else:
        await message.reply('*Братиш, не кипишуй, ты уже есть*', parse_mode='markdown')
    sql.close()

@router.message(Command('profile'))
async def profile(message: Message, command: CommandObject):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    if command.args is None:
        profile_settings = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Изменить описание', callback_data=f'change_desc:{message.from_user.username}:id')],
            [InlineKeyboardButton(text='Изменить аву', callback_data=f'change_avatar:{message.from_user.username}:id')],
            [InlineKeyboardButton(text='Получить награду', callback_data=f'getcash:{message.from_user.username}:id')],
        ])
        for usid, name, desc, balance, photo, partner, ptime, level, exp, hack_lvl, stamina in sql.execute('SELECT * FROM users WHERE user_id = ?', (message.from_user.id,)):
            imgfile = BufferedInputFile(file=photo, filename=f'{usid}.png')
            await message.reply_photo(photo=imgfile, caption=f'👤<b>Ник:</b> {name}\n💰<b>Баланс:</b> {balance}\n🕶 <b>Уровень: </b> {level} ({exp} XP)\n♨️ <b>Стамина: </b> {stamina}\n\n📝<b>Описание:</b> {desc}\n\n❤️ <b>Партнёр:</b> {partner}', reply_markup=profile_settings, parse_mode="HTML")
            break
    else:
        user_to_check = command.args.replace('@', '').replace(' ', '')
        profile_settings = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Изменить описание', callback_data=f'change_desc:{user_to_check}:username')],
            [InlineKeyboardButton(text='Изменить аву', callback_data=f'change_avatar:{user_to_check}:username')],
            [InlineKeyboardButton(text='Получить награду', callback_data=f'getcash:{user_to_check}:username')],
        ])
        for usid, name, desc, balance, photo, partner, ptime, level, exp, hack_lvl, stamina in sql.execute('SELECT * FROM users WHERE username = ?', (user_to_check,)):
            imgfile = BufferedInputFile(file=photo, filename=f'{usid}.png')
            await message.reply_photo(photo=imgfile, caption=f'👤<b>Ник:</b> {name}\n💰<b>Баланс:</b> {balance}\n🕶 <b>Уровень: </b> {level} ({exp} XP)\n♨️ <b>Стамина: </b> {stamina}\n\n📝<b>Описание:</b> {desc}\n\n❤️ <b>Партнёр:</b> {partner}', reply_markup=profile_settings, parse_mode="HTML")
            break
    sql.close()


@router.message(Command('darknet'))
async def darknet(message: Message):
    msg_to_edit = await message.reply(f'*Подключаем VPN...*', parse_mode='markdown')
    darknet_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Взлом', callback_data=f'hackmenu:{message.from_user.username}')],
        [InlineKeyboardButton(text='Даркшоп', callback_data=f'darkshop:{message.from_user.username}')],
    ])
    await asyncio.sleep(1.5)
    await msg_to_edit.edit_text('*Заходим в tor...*', parse_mode='markdown')
    await asyncio.sleep(1.5)
    await msg_to_edit.edit_text('*Добро пожаловать в даркнет*', parse_mode='markdown', reply_markup=darknet_buttons)




@router.message(Command('top'))
async def top_list(message: Message):
    top_choice = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💵 По деньгам', callback_data=f'moneytop:{message.from_user.username}')],
        [InlineKeyboardButton(text='🔸 По уровню', callback_data=f'leveltop:{message.from_user.username}')],
    ])
    await message.reply('*Какой топ вывести?*', parse_mode='markdown', reply_markup=top_choice)


