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


#==================Обработчик текстовых сообщений=====================


@router.message(F.text.contains('@brigisbutbot'))
async def answers_handler(message: Message):
    print(message.text)
    command = message.text.replace('@brigisbutbot', '').replace(' ', '').lower()
    print(command)
    if command == 'ава':
        profots = await message.from_user.get_profile_photos()
        photousa = dict(profots.photos[0][-1]).get('file_id')
        print(profots)
        await message.reply_photo(photousa, caption='Во твоя последняя фота')
    elif command == 'мяу':
        await message.reply('МЯУ МЯУ НИГГА')

#==========ЗОНА ОБРАБОТКИ CALLBACK ЗАПРОСОВ=============

@router.callback_query(F.data.contains('change_desc'))
async def change_desc_call(callback_query: CallbackQuery, state: FSMContext):
    calldata = callback_query.data.split(':')[1]
    type_of_data = callback_query.data.split(':')[2]

    usname = callback_query.data.split(':')[1]
    if usname == callback_query.from_user.username:
        await state.set_state(ChangeDescription.new_desc)
        await callback_query.message.answer(f'@{callback_query.from_user.username}, Введи новое описание: ')
    else:
        await callback_query.answer('Ты тоже не наглей окда')



@router.message(ChangeDescription.new_desc)
async def set_new_desc(message: Message, state: FSMContext):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    await state.update_data(new_desc=message.text)
    data = await state.get_data()
    print(data)
    sql.execute('UPDATE users SET desc = ? WHERE username = ?', (data['new_desc'], message.from_user.username))
    db.commit()
    sql.close()
    await message.reply("*Успешно*", parse_mode='markdown')
    await state.clear()



@router.callback_query(F.data.contains('buytag'))
async def change_tag_call(callback_query: CallbackQuery, state: FSMContext):
    calldata = callback_query.data.split(':')[1]
    db = sqlite3.connect('base.db')
    sql = db.cursor()

    usname = callback_query.data.split(':')[1]
    if usname == callback_query.from_user.username:
        sql.execute('SELECT balance FROM users WHERE username = ?', (callback_query.from_user.username,))
        balance = sql.fetchone()[0]
        if balance >= 5000:
            await state.set_state(ChangeTag.new_tag)
            await callback_query.message.answer(f'@{callback_query.from_user.username}, Введи свой новый тег: ')
        else:
            await callback_query.answer('Маловато пока баблишка')
    else:
        await callback_query.answer('Ты тоже не наглей окда')
    sql.close()


@router.message(ChangeTag.new_tag)
async def set_new_tag(message: Message, state: FSMContext):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    await state.update_data(new_tag=message.text)
    data = await state.get_data()
    print(data)
    sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (5000, message.from_user.username))
    db.commit()
    sql.close()
    await bot.set_chat_member_tag(chat_id = message.chat.id, user_id = message.from_user.id, tag = data['new_tag'])
    await message.reply("*Поздравляю с покупкой брадок*", parse_mode='markdown')
    await state.clear()


@router.callback_query(F.data.contains('buyenerg'))
async def buy_energetic(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usname = callback_query.data.split(':')[1]
    if usname == callback_query.from_user.username:
        sql.execute('SELECT level FROM users WHERE username = ?', (usname,))
        user_lvl = sql.fetchone()[0]
        max_stam = 50 + 10 * (user_lvl - 1)
        sql.execute('SELECT stamina FROM users WHERE username = ?', (usname,))
        cur_stam = sql.fetchone()[0]
        if cur_stam == max_stam:
            await callback_query.answer('Да ты и так полон сил брадок')
        else:
            if max_stam - cur_stam >= 10:
                sql.execute('SELECT balance FROM users WHERE username = ?', (callback_query.from_user.username,))
                balance = sql.fetchone()[0]
                if balance >= 200:
                    await callback_query.message.answer(f'@{usname}, выпив нашего вкуснейшего энергоса, ты восстановил 10 стамины')
                    sql.execute('UPDATE users SET stamina = stamina + ? WHERE username = ?', (10, usname,))
                    db.commit()
                    sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (200, usname,))
                    db.commit()
                else:
                    await callback_query.answer('Не хватает тебе пока на энергосик, миста/мисис бомж')
            else:
                sql.execute('SELECT balance FROM users WHERE username = ?', (callback_query.from_user.username,))
                balance = sql.fetchone()[0]
                if balance >= 200:
                    await callback_query.message.answer(f'@{usname}, выпив нашего вкуснейшего энергоса, ты восстановил стамину до предела')
                    sql.execute('UPDATE users SET stamina = stamina + ? WHERE username = ?', ((max_stam - cur_stam), usname,))
                    db.commit()
                    sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (200, usname,))
                    db.commit()
                else:
                    await callback_query.answer('Не хватает тебе пока на энергосик, миста/мисис бомж')
    else:
        await callback_query.answer('Ты тоже не наглей окда')

@router.callback_query(F.data.contains('buyburger'))
async def buy_energetic(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usname = callback_query.data.split(':')[1]
    if usname == callback_query.from_user.username:
        sql.execute('SELECT level FROM users WHERE username = ?', (usname,))
        user_lvl = sql.fetchone()[0]
        max_stam = 50 + 10 * (user_lvl - 1)
        sql.execute('SELECT stamina FROM users WHERE username = ?', (usname,))
        cur_stam = sql.fetchone()[0]
        if cur_stam == max_stam:
            await callback_query.answer('Да ты и так полон сил брадок')
        else:
            if max_stam - cur_stam >= 15:
                sql.execute('SELECT balance FROM users WHERE username = ?', (callback_query.from_user.username,))
                balance = sql.fetchone()[0]
                if balance >= 200:
                    await callback_query.message.answer(f'@{usname}, схавав вкуснейший бургер из собачка, ты восстановил 15 стамины (да не ссы, не из собачка)')
                    sql.execute('UPDATE users SET stamina = stamina + ? WHERE username = ?', (15, usname,))
                    db.commit()
                    sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (300, usname,))
                    db.commit()
                else:
                    await callback_query.answer('Не хватает тебе пока на энергосик, миста/мисис бомж')
            else:
                sql.execute('SELECT balance FROM users WHERE username = ?', (callback_query.from_user.username,))
                balance = sql.fetchone()[0]
                if balance >= 200:
                    await callback_query.message.answer(f'@{usname}, схавав вкуснейший бургер из собачка, ты восстановил стамину до предела (да не ссы, не из собачка)')
                    sql.execute('UPDATE users SET stamina = stamina + ? WHERE username = ?', ((max_stam - cur_stam), usname,))
                    db.commit()
                    sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (300, usname,))
                    db.commit()
                else:
                    await callback_query.answer('Не хватает тебе пока на энергосик, миста/мисис бомж')
    else:
        await callback_query.answer('Ты тоже не наглей окда')


@router.callback_query(F.data.contains('change_avatar'))
async def change_avatar_call(callback_query: CallbackQuery, state: FSMContext):
    try:
        usid = int(callback_query.data.split(':')[1])
        if usid == callback_query.from_user.id:
            await state.set_state(ChangeAvatar.new_avatar)
            await callback_query.message.answer(f'@{callback_query.from_user.username}, Пришли новую аву: ')
        else:
            await callback_query.answer('Ты тоже не наглей окда')
    except:
        usname = callback_query.data.split(':')[1]
        if usname == callback_query.from_user.username:
            await state.set_state(ChangeAvatar.new_avatar)
            await callback_query.message.answer(f'@{callback_query.from_user.username}, Пришли новую аву: ')
        else:
            await callback_query.answer('Ты тоже не наглей окда')

@router.message(ChangeAvatar.new_avatar)
async def set_new_avatar(message: Message, state: FSMContext):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    await state.update_data(new_avatar=message.photo[-1].file_id)
    data = await state.get_data()
    file_info = await bot.get_file(data['new_avatar'])
    downloaded_file = await bot.download_file(file_info.file_path)
    sql.execute('UPDATE users SET photo = ? WHERE username = ?', (downloaded_file.read(), message.from_user.username))
    db.commit()
    sql.close()
    await message.reply("*Успешно*", parse_mode='markdown')
    await state.clear()

@router.callback_query(F.data.contains('declinemarry'))
async def decline_marriage_call(callback_query: CallbackQuery):
    usname1 = str(callback_query.data.split(':')[1]).replace('@', '')
    usname2 = str(callback_query.data.split(':')[2]).replace('@', '')
    if usname1 == callback_query.from_user.username:
        await callback_query.message.delete()
        await callback_query.message.edit_text(f'@{usname2}, к сожалу тя отшили')
    else:
        await callback_query.answer('Ты тоже не наглей окда')

@router.callback_query(F.data.contains('agreemarry'))
async def agree_marriage_call(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usname1 = str(callback_query.data.split(':')[1]).replace('@', '')
    usname2 = str(callback_query.data.split(':')[2]).replace('@', '')
    print(f'я тут, {usname1} {usname2}')
    if usname1 == callback_query.from_user.username:
        sql.execute('UPDATE users SET partner = ? WHERE username = ?', (usname1, usname2))
        db.commit()
        sql.execute('UPDATE users SET partner = ? WHERE username = ?', (usname2, usname1))
        db.commit()
        await callback_query.message.delete()
        await callback_query.message.answer(f'💍 Поздравляем молодоженов @{usname2} и @{usname1}')
    else:
        await callback_query.answer('Ты тоже не наглей окда')
    sql.close()

@router.callback_query(F.data.contains('agreedivorce'))
async def agree_divorce_call(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usname1 = str(callback_query.data.split(':')[1]).replace('@', '')
    usname2 = str(callback_query.data.split(':')[2]).replace('@', '')
    if usname2 == callback_query.from_user.username:
        sql.execute('UPDATE users SET partner = ? WHERE username = ?', ('нема', usname1,))
        db.commit()
        sql.execute('UPDATE users SET partner = ? WHERE username = ?', ('нема', usname2,))
        db.commit()
        await callback_query.message.delete()
        await callback_query.message.answer(f'💔 @{usname1}, @{usname2} разводится с тобой')
    else:
        await callback_query.answer('Ты тоже не наглей окда')
    sql.close()

@router.callback_query(F.data.contains('canceldivorce'))
async def cancel_divorce_call(callback_query: CallbackQuery):
    usname1 = str(callback_query.data.split(':')[1]).replace('@', '')
    if usname1 == callback_query.from_user.username:
        await callback_query.message.delete()
    else:
        await callback_query.answer('Ты тоже не наглей окда')

@router.callback_query(F.data.contains('declineduel'))
async def decline_duel_call(callback_query: CallbackQuery):
    usname1 = str(callback_query.data.split(':')[1]).replace('@', '')
    if usname1 == callback_query.from_user.username:
        await callback_query.message.edit_text(f'<b>Дуэль с @{usname1} не состоялась</b>', parse_mode='html')
    else:
        await callback_query.answer('Ты тоже не наглей окда')

@router.callback_query(F.data.contains('agreeduel'))
async def agree_duel_call(callback_query: CallbackQuery):
    usname1 = str(callback_query.data.split(':')[1]).replace('@', '')
    usname2 = str(callback_query.data.split(':')[2]).replace('@', '')
    bet = int(callback_query.data.split(':')[3])
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    if usname1 == callback_query.from_user.username:
        await callback_query.message.delete()
        members_of_duel = [usname1, usname2]
        winner = random.choice(members_of_duel)
        if winner == usname1:
            sql.execute('UPDATE users SET balance = balance + ? WHERE username = ?', (bet, usname1))
            db.commit()
            sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (bet, usname2))
            db.commit()
            photo = open('duelphoto.jpg', 'rb').read()
            imgfile = BufferedInputFile(file=photo, filename = f"{usname1}vs{usname2}.jpg")
            await callback_query.message.answer_photo(imgfile, caption = f'@{usname2} и @{usname1} скрестили шпаги, и победителем стал @{usname1}\n\n<b>Выигрыш:</b> {bet}', parse_mode='html')
        if winner == usname2:
            sql.execute('UPDATE users SET balance = balance + ? WHERE username = ?', (bet, usname2))
            db.commit()
            sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (bet, usname1))
            db.commit()
            photo = open('duelphoto.jpg', 'rb').read()
            imgfile = BufferedInputFile(file=photo, filename = f"{usname1}vs{usname2}.jpg")
            await callback_query.message.answer_photo(imgfile, caption = f'@{usname2} и @{usname1} скрестили шпаги, и победителем стал @{usname2}\n\n<b>Выигрыш:</b> {bet}', parse_mode='html')
    else:
        await callback_query.answer('Ты тоже не наглей окда')
    sql.close()


@router.callback_query(F.data.contains('moneytop'))
async def money_top_call(callback_query: CallbackQuery):
    usname = callback_query.data.split(':')[1]
    if usname == callback_query.from_user.username:
        await callback_query.message.edit_text(f'*Топ по деньгам:*', parse_mode='markdown', reply_markup= await get_money_top())
    else:
        await callback_query.answer('Ты тоже не наглей окда')

@router.callback_query(F.data.contains('leveltop'))
async def lvl_top_call(callback_query: CallbackQuery):
    usname = callback_query.data.split(':')[1]
    if usname == callback_query.from_user.username:
        await callback_query.message.edit_text(f'*Топ по уровню:*', parse_mode='markdown', reply_markup= await get_level_top())
    else:
        await callback_query.answer('Ты тоже не наглей окда')

@router.callback_query(F.data.contains('darkshop'))
async def darkshop(callback_query: CallbackQuery):
    usname = callback_query.data.split(':')[1]
    if usname == callback_query.from_user.username:
        await callback_query.message.edit_text(f'*Вот что тебе доступно, выбирай быстрее*', parse_mode='markdown', reply_markup=await get_hackupgrades(callback_query.from_user.id))
    else:
        await callback_query.answer('Ты тоже не наглей окда')

@router.callback_query(F.data.contains('hackmenu'))
async def hackmenu(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usname = callback_query.data.split(':')[1]
    if usname == callback_query.from_user.username:
        sql.execute('SELECT hack_skill FROM users WHERE username = ?', (usname,))
        hskill = sql.fetchone()[0]
        photofile = FSInputFile('hackmenuphoto.jpg')
        hackphoto = InputMediaPhoto(media = photofile, caption=f'*Твой навык взлома: *{hskill}\n\n*Кого взломаем сегодня?*', parse_mode='markdown')
        await callback_query.message.edit_media(media=hackphoto, reply_markup=await get_corps(callback_query.from_user.id))
    else:
        await callback_query.answer('Ты тоже не наглей окда')
    sql.close()

@router.callback_query(F.data.contains('ipage'))
async def item_page(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usid = callback_query.data.split(':')[1]
    item_id = callback_query.data.split(':')[2]
    print(usid, callback_query.from_user.id)
    if int(usid) == callback_query.from_user.id:
        sql.execute('SELECT * FROM darkshop WHERE item_id = ?', (item_id,))
        item = sql.fetchone()
        print(item)
        item_page_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Купить', callback_data=f'buydarkitem:{callback_query.from_user.username}:{item_id}')],
            [InlineKeyboardButton(text='Назад', callback_data=f'darkshop:{callback_query.from_user.username}')],
        ])
        await callback_query.message.edit_text(f'{item[0]}\n\n<i>{item[2]}</i>\n\n<b>Цена:</b> {item[1]}', parse_mode='HTML', reply_markup=item_page_buttons)
    else:
        await callback_query.answer('Ты тоже не наглей окда')
    sql.close()

@router.callback_query(F.data.contains('cpage'))
async def corp_page(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usid = callback_query.data.split(':')[1]
    corp_id = callback_query.data.split(':')[2]
    print(usid, callback_query.from_user.id)
    if int(usid) == callback_query.from_user.id:
        sql.execute('SELECT * FROM corps WHERE corp_id = ?', (corp_id,))
        item = sql.fetchone()
        corp_page_buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Взломать', callback_data=f'starthack:{callback_query.from_user.username}:{corp_id}')],
            [InlineKeyboardButton(text='Назад', callback_data=f'hackmenu:{callback_query.from_user.username}')],
        ])
        imgfile = BufferedInputFile(item[5], filename = f'{corp_id}:{usid}.png')
        corpimg = InputMediaPhoto(media = imgfile, caption = f'*{item[0]}*\n\n_{item[1]}_\n\n*Уровень защиты: *{item[2]}', parse_mode='markdown')
        await callback_query.message.edit_media(media=corpimg, reply_markup=corp_page_buttons)
    else:
        await callback_query.answer('Ты тоже не наглей окда')
    sql.close()

@router.callback_query(F.data.contains('starthack'))
async def start_hack_process(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usname = callback_query.data.split(':')[1]
    corp_id = callback_query.data.split(':')[2]
    print(usname, callback_query.from_user.username)
    if usname == callback_query.from_user.username:
        sql.execute('SELECT stamina FROM users WHERE username = ?', (usname,))
        user_stamina = sql.fetchone()[0]
        if user_stamina < 10:
            await callback_query.answer('Подустал ты, брадок, для взломов')
        else:
            sql.execute('SELECT * FROM corps WHERE corp_id = ?', (corp_id,))
            corp_info = sql.fetchone()
            corp_resist = corp_info[2]
            corp_reward = corp_info[3]
            corp_penalty = corp_info[4]
            sql.execute('SELECT hack_skill FROM users WHERE username = ?', (usname,))
            user_hack_skill = sql.fetchone()[0]
            attack = random.randint(0, 10) + user_hack_skill
            sql.execute('UPDATE users SET stamina = stamina - ? WHERE username = ?', (10, usname,))
            db.commit()
            if attack >= corp_resist:
                await callback_query.message.delete()
                msg = await callback_query.message.answer(f'*Terminal:*\n\nroot@Kali:~ ssh admin@{corp_info[0]}', parse_mode='markdown')
                await asyncio.sleep(1.5)
                await msg.edit_text(f'*Terminal:*\n\nroot@Kali:~ ssh admin@{corp_info[0]}\nadmin@{corp_info[0]}:~ python virus.py', parse_mode='markdown')
                await asyncio.sleep(1.5)
                await msg.edit_text(f'*Terminal:*\n\nroot@Kali:~ ssh admin@{corp_info[0]}\nadmin@{corp_info[0]}:~ python virus.py\nGetting data...', parse_mode='markdown')
                await asyncio.sleep(1.5)
                await msg.edit_text(f'*Terminal:*\n\nroot@Kali:~ ssh admin@{corp_info[0]}\nadmin@{corp_info[0]}:~ python virus.py\nGetting data...\nSuccess', parse_mode='markdown')
                await asyncio.sleep(1.5)
                await msg.edit_text(f'@{usname}, *Взлом прошёл успешно*\n\n*Удалось украсть данные ценностью* {corp_reward}💵\n\n*Выход из системы...*', parse_mode='markdown')
                sql.execute('UPDATE users SET balance = balance + ? WHERE username = ?', (corp_reward, usname,))
                db.commit()
            else:
                await callback_query.message.delete()
                msg = await callback_query.message.answer(f'*Terminal:*\n\nroot@Kali:~ ssh admin@{corp_info[0]}', parse_mode='markdown')
                await asyncio.sleep(1.5)
                await msg.edit_text(f'*Terminal:*\n\nroot@Kali:~ ssh admin@{corp_info[0]}\nadmin@{corp_info[0]}:~ python virus.py', parse_mode='markdown')
                await asyncio.sleep(1.5)
                await msg.edit_text(f'*Terminal:*\n\nroot@Kali:~ ssh admin@{corp_info[0]}\nadmin@{corp_info[0]}:~ python virus.py\nGetting data...', parse_mode='markdown')
                await asyncio.sleep(1.5)
                await msg.edit_text(f'*Terminal:*\n\nroot@Kali:~ ssh admin@{corp_info[0]}\nadmin@{corp_info[0]}:~ python virus.py\nGetting data...\nERROR', parse_mode='markdown')
                await asyncio.sleep(1.5)
                await msg.edit_text(f'@{usname}, *Чёрт, нас обнаружили*\n\n*Штраф за попытку взлома:* {corp_penalty}💵\n\n*Выход из системы...*',parse_mode='markdown')
                sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (corp_penalty, usname,))
                db.commit()
    else:
        await callback_query.answer('Ты тоже не наглей окда')
    sql.close()

@router.callback_query(F.data.contains('buydarkitem'))
async def buy_dark_item(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usname = callback_query.data.split(':')[1]
    item_id = callback_query.data.split(':')[2]
    if usname == callback_query.from_user.username:
        sql.execute('SELECT balance FROM users WHERE username = ?', (usname,))
        user_balance = sql.fetchone()[0]
        sql.execute('SELECT price FROM darkshop WHERE item_id = ?', (item_id,))
        price = sql.fetchone()[0]
        if user_balance is None or user_balance < price:
            await callback_query.answer('*Не хватает баблишка, подкопи и приходи*', parse_mode='markdown')
        else:
            sql.execute('UPDATE users SET balance = balance - ? WHERE username = ?', (price, usname))
            db.commit()
            sql.execute('SELECT item_name FROM darkshop WHERE item_id = ?', (item_id,))
            item_name = sql.fetchone()[0]
            sql.execute('SELECT hack_power FROM darkshop WHERE item_id = ?', (item_id,))
            item_power = sql.fetchone()[0]
            sql.execute('INSERT INTO users_items VALUES (?, ?, ?)', (usname, callback_query.from_user.id, item_name))
            db.commit()
            sql.execute('UPDATE users SET hack_skill = hack_skill + ? WHERE username = ?', (item_power, usname))
            db.commit()
            await callback_query.message.edit_text('*Сделка прошла успешно*', parse_mode='markdown')
    else:
        await callback_query.answer('Ты тоже не наглей окда')
    sql.close()


@router.callback_query(F.data.contains('showprofile'))
async def show_profile(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    usname = callback_query.data.split(':')[1]
    profile_settings = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить описание', callback_data=f'change_desc:{usname}:id')],
        [InlineKeyboardButton(text='Изменить аву', callback_data=f'change_avatar:{usname}:id')],
        [InlineKeyboardButton(text='Получить награду', callback_data=f'getcash:{usname}:id')],
    ])
    for usid, name, desc, balance, photo, partner, ptime, level, exp, hack_lvl, stamina in sql.execute('SELECT * FROM users WHERE username = ?',
                                                                        (usname,)):
        imgfile = BufferedInputFile(file=photo, filename=f'{usid}.png')
        await callback_query.message.reply_photo(photo=imgfile, caption=f'👤<b>Ник:</b> {name}\n💰<b>Баланс:</b> {balance}\n🕶 <b>Уровень: </b> {level} ({exp} XP)\n♨️ <b>Стамина: </b> {stamina}\n\n📝<b>Описание:</b> {desc}\n\n❤️ <b>Партнёр:</b> {partner}', reply_markup=profile_settings, parse_mode="HTML")
        break


@router.callback_query(F.data.contains('getcash'))
async def get_rewardcash(callback_query: CallbackQuery):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    try:
        usid = int(callback_query.data.split(':')[1])
        if usid == callback_query.from_user.id:
            current_time = datetime.datetime.now()
            sql.execute('SELECT paytime FROM users WHERE user_id = ?', (callback_query.from_user.id,))
            user_time = sql.fetchone()[0]
            print(user_time)
            if user_time is None:
                timetowrite = datetime.datetime.now() + datetime.timedelta(hours=4)
                timetowrite = timetowrite.replace(microsecond=0)
                print(timetowrite)
                amount = random.randint(50, 200)
                await callback_query.answer(f'Ты усердно работал и получил {amount} деняг')
                sql.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, callback_query.from_user.id))
                db.commit()
                sql.execute('UPDATE users SET paytime = ? WHERE user_id = ?', (f'{timetowrite}', callback_query.from_user.id))
                db.commit()
            else:
                user_time = strptime(user_time, '%Y-%m-%d %H:%M:%S')
                user_time = datetime.datetime.fromtimestamp(time.mktime(user_time))
                if current_time >= user_time:
                    timetowrite = datetime.datetime.now() + datetime.timedelta(hours=4)
                    timetowrite = timetowrite.replace(microsecond=0)
                    print(timetowrite)
                    amount = random.randint(50, 200)
                    await callback_query.answer(f'Ты усердно работал(а) и получил(а) {amount} деняг')
                    sql.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, callback_query.from_user.id))
                    db.commit()
                    sql.execute('UPDATE users SET paytime = ? WHERE user_id = ?',
                                (f'{timetowrite}', callback_query.from_user.id))
                    db.commit()
                else:
                    await callback_query.answer('Пока рано брадок')
        else:
            await callback_query.answer('Ты тоже не наглей окда')
    except:
        usname = callback_query.data.split(':')[1]
        if usname == callback_query.from_user.username:
            sql.execute('SELECT stamina FROM users WHERE username = ?', (usname,))
            user_stamina = sql.fetchone()[0]
            if user_stamina < 10:
                await callback_query.answer('Подустал ты, брадок, для работы')
            else:
                current_time = datetime.datetime.now()
                sql.execute('SELECT paytime FROM users WHERE username = ?', (callback_query.from_user.username,))
                user_time = sql.fetchone()[0]
                print(user_time)
                if user_time is None:
                    timetowrite = datetime.datetime.now() + datetime.timedelta(hours=4)
                    timetowrite = timetowrite.replace(microsecond=0)
                    print(timetowrite)
                    sql.execute('SELECT level FROM users WHERE username = ?', (callback_query.from_user.username,))
                    user_lvl = sql.fetchone()[0]
                    amount = 0
                    if user_lvl <= 5:
                        amount = 50
                    if user_lvl >= 6 and user_lvl <= 10:
                        amount = 100
                    if user_lvl >= 11 and user_lvl <= 15:
                        amount = 150
                    if user_lvl >= 16 and user_lvl <= 19:
                        amount = 200
                    if user_lvl == 20:
                        amount = 300
                    await callback_query.answer(f'Ты усердно работал и получил {amount} деняг')
                    sql.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?',
                                (amount, callback_query.from_user.id))
                    db.commit()
                    sql.execute('UPDATE users SET paytime = ? WHERE user_id = ?',
                                (f'{timetowrite}', callback_query.from_user.id))
                    db.commit()
                    sql.execute('UPDATE users SET stamina = stamina - ? WHERE username = ?', (10, usname,))
                    db.commit()
                else:
                    user_time = strptime(user_time, '%Y-%m-%d %H:%M:%S')
                    user_time = datetime.datetime.fromtimestamp(time.mktime(user_time))
                    if current_time >= user_time:
                        timetowrite = datetime.datetime.now() + datetime.timedelta(hours=4)
                        timetowrite = timetowrite.replace(microsecond=0)
                        print(timetowrite)
                        sql.execute('SELECT level FROM users WHERE username = ?', (callback_query.from_user.username,))
                        user_lvl = sql.fetchone()[0]
                        amount = 0
                        if user_lvl <= 5:
                            amount = 50
                        if user_lvl >= 6 and user_lvl <= 10:
                            amount = 100
                        if user_lvl >= 11 and user_lvl <= 15:
                            amount = 150
                        if user_lvl >= 16 and user_lvl <= 19:
                            amount = 200
                        if user_lvl == 20:
                            amount = 300
                        await callback_query.answer(f'Ты усердно работал(а) и получил(а) {amount} деняг')
                        sql.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?',
                                    (amount, callback_query.from_user.id))
                        db.commit()
                        sql.execute('UPDATE users SET paytime = ? WHERE user_id = ?',
                                    (f'{timetowrite}', callback_query.from_user.id))
                        db.commit()
                        sql.execute('UPDATE users SET stamina = stamina - ? WHERE username = ?', (10, usname,))
                        db.commit()
                    else:
                        diff = user_time - current_time
                        hours = int(diff.total_seconds() / 3600)
                        minutes = int((diff.total_seconds() % 3600) / 60)
                        await callback_query.answer(f'Пока рано брадок, возращайся через {hours} ч {minutes} мин')
        else:
            await callback_query.answer('Ты тоже не наглей окда')
        sql.close()

@router.message()
async def all_msg_handler(message: Message):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    try:
        sql.execute('UPDATE users SET exp = exp + 1 WHERE user_id = ?', (message.from_user.id,))
        db.commit()
        sql.execute('SELECT level FROM users WHERE user_id = ?', (message.from_user.id,))
        cur_lvl = sql.fetchone()[0]
        sql.execute('SELECT exp FROM users WHERE user_id = ?', (message.from_user.id,))
        cur_exp = sql.fetchone()[0]
        sql.execute('SELECT level FROM levels WHERE need_exp = ?', (cur_exp,))
        lvl = sql.fetchone()[0]
        if lvl is not None:
            if lvl > cur_lvl:
                sql.execute('UPDATE users SET level = ? WHERE user_id = ?', (lvl, message.from_user.id,))
                db.commit()
                sql.execute('UPDATE users SET stamina = stamina + ? WHERE user_id = ?', (10, message.from_user.id,))
                db.commit()
                await message.reply(f'@{message.from_user.username}, ты апнул {lvl} лвл!')
        sql.execute('SELECT username FROM users WHERE user_id = ?', (message.from_user.id,))
        cur_username = sql.fetchone()[0]
        if message.from_user.username == cur_username:
            pass
        else:
            sql.execute('UPDATE users SET username = ? WHERE username = ?', (message.from_user.username, cur_username,))
            db.commit()
        sql.close()
    except Exception as e:
        print(e)