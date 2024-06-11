import logging
import typing
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
bot = Bot('6531518226:AAHNU6j8mGG3BEvME8FUMzLzF4YXZezRRJ0')
# bot = Bot(token='5836836441:AAHwBHr-iffFgjlUidhKr5XmL1FGpRILcvU')
dp = Dispatcher(bot)

def panel():
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton('Оформить карту', callback_data='karta'),
        types.InlineKeyboardButton('Задать вопрос', callback_data='savol'),
        types.InlineKeyboardButton('Посмотреть оферту', callback_data='oferta'),
        types.InlineKeyboardButton('Контакты', callback_data='kontakt')
    )
def davlatlar():
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton('Карта в Беларуси', callback_data='belarusia'),
        types.InlineKeyboardButton('Карта в Киргизии', callback_data='kirgizia'),
        types.InlineKeyboardButton('Карта в Казахстане', callback_data='qazaxistan'),
        types.InlineKeyboardButton('Срочный выпуск', callback_data='vipusk'),
        types.InlineKeyboardButton('Образец доверенности', callback_data='doverennost'),
        types.InlineKeyboardButton('Назад', callback_data='home1')
    )
@dp.callback_query_handler(lambda c: c.data == "home1")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Нужна пластиковая карта Visa или Mastercard иностранного банка? Поможем оформить удаленно. 

Стоимость услуг:

• Карта Киргизии
Есть мобильное приложение и онлайн-банкинг.
VISA Gold – 37 500 руб.

• Карта Казахстана
Есть мобильное приложение и онлайн-банкинг.
VISA Signature – 40 500 руб.


• Карта Беларуси
Есть мобильное приложение и онлайн -банкинг, доступен исходящий SWIFT через e-mail, работает Apple Pay / Google Pay.
VISA Gold  – 35 500 руб.
В стоимость включено обслуживание на 3 года.
МИР - 5000 руб. (удобно использовать для моментального пополнения с российской карты МИР и перевода на валютную VISA/MasterCard)

Без исходящего SWIFT, есть Apple Pay/Google Pay:
MasterCard Standard – 27 500 руб.

• Срочный выпуск пластиковой карты VISA Gold в Киргизии – 42 500 руб.

Карты оформляются только по доверенности!""", reply_markup=panel())
    await callback_query.message.delete()
def belarus():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('VISA GOLD', callback_data='visa_gold'),
        types.InlineKeyboardButton('Мир', callback_data='mir'),
        types.InlineKeyboardButton('MC Standard', callback_data='standard'),
        types.InlineKeyboardButton('Назад', callback_data='home2'),        
    )
@dp.callback_query_handler(lambda c: c.data == "home2")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Для получения пластиковой карты Вам необходимо:
    1. Прислать скан заграничного паспорта.
    2. Прислать скан российского паспорта (требуется только при оформлении карты в Беларуси).
    3. Написать Ваш номер телефона, email.
    4. Написать ИНН (только для Киргизии).
    5. Оплатить услугу.
    6. Оформить нотариальную доверенность (для Киргизии и Беларуси).
        

    Готовы оформить заявку?""", reply_markup=davlatlar())
    await callback_query.message.delete()
def rasm():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Загружаю', callback_data='zagruzka'),
        types.InlineKeyboardButton('На главный', callback_data='glavniy')       
    )
@dp.callback_query_handler(lambda c: c.data == 'zagruzka')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""После получения фотографии паспорта мы сразу же приступаем к работе. 

В ближайшее время мы пришлем ссылку для проведения оплаты.

Ждем скан паспорта.""")
@dp.callback_query_handler(lambda c: c.data == 'standard')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Напишите свой номер телефона и email.

Также загрузите в чат скан загранпаспорта и российского паспорта (2-ую и 3-ью страницы, а также страницу с пропиской) в хорошем качестве: без бликов, теней, пальцев и посторонних предметов, отступ от края паспорта до границы фотографии не менее 5мм (приложить как файл). 

Как тут👇""")
    file_path = "rasm.jpg"

    with open(file_path, "rb") as file:
        await bot.send_photo(callback_query.from_user.id, file, reply_markup=rasm())    
@dp.callback_query_handler(lambda c: c.data == 'mir')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Напишите свой номер телефона и email.

Также загрузите в чат скан загранпаспорта и российского паспорта (2-ую и 3-ью страницы, а также страницу с пропиской) в хорошем качестве: без бликов, теней, пальцев и посторонних предметов, отступ от края паспорта до границы фотографии не менее 5мм (приложить как файл). 

Как тут👇""")
    file_path = "rasm.jpg"

    with open(file_path, "rb") as file:
        await bot.send_photo(callback_query.from_user.id, file, reply_markup=rasm())    
@dp.callback_query_handler(lambda c: c.data == 'visa_gold')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Напишите свой номер телефона и email.

Также загрузите в чат скан загранпаспорта и российского паспорта (2-ую и 3-ью страницы, а также страницу с пропиской) в хорошем качестве: без бликов, теней, пальцев и посторонних предметов, отступ от края паспорта до границы фотографии не менее 5мм (приложить как файл). 

Как тут👇""")
    file_path = "rasm.jpg"

    with open(file_path, "rb") as file:
        await bot.send_photo(callback_query.from_user.id, file, reply_markup=rasm())    
def kirgizia():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton('VISA GOLD', callback_data='kirgizia_visa_gold'),    
        types.InlineKeyboardButton('Назад', callback_data='home3')    
    )
@dp.callback_query_handler(lambda c: c.data == "home3")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Для получения пластиковой карты Вам необходимо:
    1. Прислать скан заграничного паспорта.
    2. Прислать скан российского паспорта (требуется только при оформлении карты в Беларуси).
    3. Написать Ваш номер телефона, email.
    4. Написать ИНН (только для Киргизии).
    5. Оплатить услугу.
    6. Оформить нотариальную доверенность (для Киргизии и Беларуси).
        

    Готовы оформить заявку?""", reply_markup=davlatlar())
    await callback_query.message.delete()
@dp.callback_query_handler(lambda c: c.data == 'kirgizia_visa_gold')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Напишите свой номер телефона, email и ИНН.

Также загрузите в чат скан загранпаспорта в хорошем качестве: без бликов, теней, пальцев и посторонних предметов, отступ от края паспорта до границы фотографии не менее 5мм (приложить как файл). 

Как тут👇""")
    file_path = "rasm.jpg"

    with open(file_path, "rb") as file:
        await bot.send_photo(callback_query.from_user.id, file, reply_markup=rasm())    
def srocniyvipusk():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Оформит карту', callback_data='srochniy'),    
        types.InlineKeyboardButton('Назад', callback_data='home4')    
    )
@dp.callback_query_handler(lambda c: c.data == "home4")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Для получения пластиковой карты Вам необходимо:
    1. Прислать скан заграничного паспорта.
    2. Прислать скан российского паспорта (требуется только при оформлении карты в Беларуси).
    3. Написать Ваш номер телефона, email.
    4. Написать ИНН (только для Киргизии).
    5. Оплатить услугу.
    6. Оформить нотариальную доверенность (для Киргизии и Беларуси).
        

    Готовы оформить заявку?""", reply_markup=davlatlar())
    await callback_query.message.delete()
@dp.callback_query_handler(lambda c: c.data == 'srochniy')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Напишите свой номер телефона, email и ИНН.

Также загрузите в чат скан загранпаспорта в хорошем качестве: без бликов, теней, пальцев и посторонних предметов, отступ от края паспорта до границы фотографии не менее 5мм (приложить как файл). 

Как тут👇""")
    file_path = "rasm.jpg"

    with open(file_path, "rb") as file:
        await bot.send_photo(callback_query.from_user.id, file, reply_markup=rasm())    
def qazaxstan():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Хочу VISA Signature', callback_data='qazaxstan_visa_gold'),    
        types.InlineKeyboardButton('Назад', callback_data='home5')    
    )
@dp.callback_query_handler(lambda c: c.data == "home5")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Для получения пластиковой карты Вам необходимо:
    1. Прислать скан заграничного паспорта.
    2. Прислать скан российского паспорта (требуется только при оформлении карты в Беларуси).
    3. Написать Ваш номер телефона, email.
    4. Написать ИНН (только для Киргизии).
    5. Оплатить услугу.
    6. Оформить нотариальную доверенность (для Киргизии и Беларуси).
        

    Готовы оформить заявку?""", reply_markup=davlatlar())
    await callback_query.message.delete()
@dp.callback_query_handler(lambda c: c.data == 'qazaxstan_visa_gold')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Напишите свой номер телефона, email и ИНН.

Также загрузите в чат скан загранпаспорта в хорошем качестве: без бликов, теней, пальцев и посторонних предметов, отступ от края паспорта до границы фотографии не менее 5мм (приложить как файл). 

Как тут👇""")
    file_path = "rasm.jpg"

    with open(file_path, "rb") as file:
        await bot.send_photo(callback_query.from_user.id, file, reply_markup=rasm())   

@dp.callback_query_handler(lambda c: c.data == 'doverennost')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Напишите свой номер телефона, email и ИНН.

Также загрузите в чат скан загранпаспорта в хорошем качестве: без бликов, теней, пальцев и посторонних предметов, отступ от края паспорта до границы фотографии не менее 5мм (приложить как файл). 

Как тут👇""")
    file_path1 = "Довереность_AVO_Беларусь.pdf"

    with open(file_path1, "rb") as file1:
        await bot.send_document(callback_query.from_user.id, file1)    
           
    file_path2 = "Довереность_AVO_Киргизия_USD_и_EUR.pdf"

    with open(file_path2, "rb") as file2:
        await bot.send_document(callback_query.from_user.id, file2)    

def savol():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Банк открытия счёта', callback_data='bank_open'),
        types.InlineKeyboardButton('Пополнение счёта', callback_data='bank_p'),
        types.InlineKeyboardButton('Гарантии', callback_data='garantia'),
        types.InlineKeyboardButton('Валюта счёта', callback_data='bank_v'),
        types.InlineKeyboardButton('Защита перс данных', callback_data='protection'),
        types.InlineKeyboardButton('Позвать специалиста', callback_data='special')
    )
@dp.callback_query_handler(lambda c: c.data == 'protection')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Политика обработки и защиты персональных данных 👇""")
    file_path3 = "AVO.cards_политика_конф.pdf"

    with open(file_path3, "rb") as file3:
        await bot.send_document(callback_query.from_user.id, file3)    
def kontakt():
     return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('На главный', callback_data='glavniy'),
     )
def bank_open():
     return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Назад', callback_data='home6'),
        types.InlineKeyboardButton('На главный', callback_data='glavniy'),
     )
@dp.callback_query_handler(lambda c: c.data == "home6")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Мы помогаем с оформлением карт Visa и Mastercard для того, чтобы Вы свободно могли путешествовать, оплачивать покупки по всему миру и в интернете.

    Мы подготовили для Вас ответы на самые распространенные вопросы.

    А если у Вас остались вопросы - пишите прямо в этот чат. Мы ответим с 9 до 22 часов по МСК.""", reply_markup=savol())
    await callback_query.message.delete()
def bank_p():
     return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Назад', callback_data='home7'),
        types.InlineKeyboardButton('На главный', callback_data='glavniy'),
     )
@dp.callback_query_handler(lambda c: c.data == "home7")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Мы помогаем с оформлением карт Visa и Mastercard для того, чтобы Вы свободно могли путешествовать, оплачивать покупки по всему миру и в интернете.

    Мы подготовили для Вас ответы на самые распространенные вопросы.

    А если у Вас остались вопросы - пишите прямо в этот чат. Мы ответим с 9 до 22 часов по МСК.""", reply_markup=savol())
    await callback_query.message.delete()
def garantia():
     return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Назад', callback_data='home8'),
        types.InlineKeyboardButton('На главный', callback_data='glavniy'),
     )
@dp.callback_query_handler(lambda c: c.data == "home8")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Мы помогаем с оформлением карт Visa и Mastercard для того, чтобы Вы свободно могли путешествовать, оплачивать покупки по всему миру и в интернете.

    Мы подготовили для Вас ответы на самые распространенные вопросы.

    А если у Вас остались вопросы - пишите прямо в этот чат. Мы ответим с 9 до 22 часов по МСК.""", reply_markup=savol())
    await callback_query.message.delete()
def bank_v():
     return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Назад', callback_data='home9'),
        types.InlineKeyboardButton('На главный', callback_data='glavniy'),
     )
@dp.callback_query_handler(lambda c: c.data == "home9")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Мы помогаем с оформлением карт Visa и Mastercard для того, чтобы Вы свободно могли путешествовать, оплачивать покупки по всему миру и в интернете.

    Мы подготовили для Вас ответы на самые распространенные вопросы.

    А если у Вас остались вопросы - пишите прямо в этот чат. Мы ответим с 9 до 22 часов по МСК.""", reply_markup=savol())
    await callback_query.message.delete()
def oferta():
     return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('На главный', callback_data='glavniy'),
     )

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply(f"""Нужна пластиковая карта Visa или Mastercard иностранного банка? Поможем оформить удаленно. 

Стоимость услуг:

• Карта Киргизии
Есть мобильное приложение и онлайн-банкинг.
VISA Gold – 37 500 руб.

• Карта Казахстана
Есть мобильное приложение и онлайн-банкинг.
VISA Signature – 40 500 руб.


• Карта Беларуси
Есть мобильное приложение и онлайн -банкинг, доступен исходящий SWIFT через e-mail, работает Apple Pay / Google Pay.
VISA Gold  – 35 500 руб.
В стоимость включено обслуживание на 3 года.
МИР - 5000 руб. (удобно использовать для моментального пополнения с российской карты МИР и перевода на валютную VISA/MasterCard)

Без исходящего SWIFT, есть Apple Pay/Google Pay:
MasterCard Standard – 27 500 руб.

• Срочный выпуск пластиковой карты VISA Gold в Киргизии – 42 500 руб.

Карты оформляются только по доверенности!""", reply_markup=panel())

vote_cb = CallbackData('vote', 'action')
filename = ""
@dp.callback_query_handler(lambda c: c.data == 'oferta')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Публичная договор-оферта 👇🏻""")
    file_path = "Оферта_AVO.cards_.pdf"

    with open(file_path, "rb") as file:
        await bot.send_document(callback_query.from_user.id, file, reply_markup=oferta())    
@dp.callback_query_handler(lambda c: c.data == 'special')
async def callback_vote_action(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Время консультаций в чат-боте: ежедневно с 09:00 до 22:00 по Москве.
Пожалуйста, напишите, свой вопрос.""")
@dp.callback_query_handler(lambda c: c.data == "glavniy")
async def ru_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"""Нужна пластиковая карта Visa или Mastercard иностранного банка? Поможем оформить удаленно. 

Стоимость услуг:

• Карта Киргизии
Есть мобильное приложение и онлайн-банкинг.
VISA Gold – 37 500 руб.

• Карта Казахстана
Есть мобильное приложение и онлайн-банкинг.
VISA Signature – 40 500 руб.
s

• Карта Беларуси
Есть мобильное приложение и онлайн -банкинг, доступен исходящий SWIFT через e-mail, работает Apple Pay / Google Pay.
VISA Gold  – 35 500 руб.
В стоимость включено обслуживание на 3 года.
МИР - 5000 руб. (удобно использовать для моментального пополнения с российской карты МИР и перевода на валютную VISA/MasterCard)

Без исходящего SWIFT, есть Apple Pay/Google Pay:
MasterCard Standard – 27 500 руб.

• Срочный выпуск пластиковой карты VISA Gold в Киргизии – 42 500 руб.

Карты оформляются только по доверенности!""", reply_markup=panel())  

    await callback_query.message.delete()
@dp.callback_query_handler(lambda c: c.data)
async def callback_vote_action(callback_query: types.CallbackQuery):
    if callback_query.data == "karta":
        await bot.send_message(callback_query.from_user.id , f"""Для получения пластиковой карты Вам необходимо:
    1. Прислать скан заграничного паспорта.
    2. Прислать скан российского паспорта (требуется только при оформлении карты в Беларуси).
    3. Написать Ваш номер телефона, email.
    4. Написать ИНН (только для Киргизии).
    5. Оплатить услугу.
    6. Оформить нотариальную доверенность (для Киргизии и Беларуси).
        

    Готовы оформить заявку?""", reply_markup=davlatlar()) 
    

    elif callback_query.data == "belarusia":
        await bot.send_message(callback_query.from_user.id ,f"""Беларусь

    Срок выпуска 14 раб. дней без учета доставки в Москву. 

    - Счет в долларах или евро.
    - Карта именная, эмбоссированная.
    - Мобильный банк подключается к белорусской сим-карте.
    - Карта поддерживается Apple Pay / Google Pay.
    - Пополнение возможно через SWIFT перевод.
    - Моментальное пополнение через системы МИР и QIWI.
    - Есть исходящие SWIFT платежи через e-mail (кроме карт MasterСard Standart).

    VISA Gold – 35 500 руб.
    3 года обслуживания входят в стоимость.
    МИР - 5000 руб. (удобно для моментального пополнения)

    MasterСard Standard – 27 500 руб. (нет исходящих SWIFT, российская sim карта).""", reply_markup=belarus())
    elif callback_query.data == "kirgizia":
        await bot.send_message(callback_query.from_user.id, f"""Киргизия

    Срок выпуска 14 раб. дней без учета доставки в Москву. 

    - Счет долларовый.
    - Карта именная и эмбоссированная. 
    - Карта поддерживается Apple Pay / Google Pay.
    - Пополнение возможно через SWIFT перевод.
    - Моментальное пополнение через Tinkoff, Сбер, Альфа, QIWI.
    - Нет исходящих SWIFT платежей.
    - Есть исх. SWIFT- платежи в евро.
    - Мобильный банк подключается к российской сим-карте.

    VISA Gold -  37 500 руб.""", reply_markup=kirgizia())
    elif callback_query.data == "qazaxistan":
        await bot.send_message(callback_query.from_user.id, f"""Казахстан

    Срок выпуска до 17 рабочих дней без учета доставки в Москву.

    - Без доверенности. 
    - Карта мультивалютная - доллар, евро, рубль, тенге.
    - Карта именная и эмбоссированная.
    - Мобильный банк подключается к казахстанской сим-карте.  
    - Карта поддерживается Apple Pay / Google Pay.
    - Нет исходящих SWIFT платежей.

    VISA Signature. Цена 40 500 р.""", reply_markup=qazaxstan())
    elif callback_query.data == "vipusk":
        await bot.send_message(callback_query.from_user.id, f"""Если  необходимо срочно открыть счет, то для Вас создали особенную услугу – оформление  дебетовой карты за 7 рабочих дней в банке Киргизии. 

    Срочная VISA Gold - 42 500 руб.""", reply_markup=srocniyvipusk())
    elif callback_query.data == "savol":
        await bot.send_message(callback_query.from_user.id, f"""Мы помогаем с оформлением карт Visa и Mastercard для того, чтобы Вы свободно могли путешествовать, оплачивать покупки по всему миру и в интернете.

    Мы подготовили для Вас ответы на самые распространенные вопросы.

    А если у Вас остались вопросы - пишите прямо в этот чат. Мы ответим с 9 до 22 часов по МСК.""", reply_markup=savol())
    
    elif callback_query.data == "bank_open":
        await bot.send_message(callback_query.from_user.id, f"""Банк открытия счета будет выбираться из тех, в которых сейчас быстрее всего открываются счета для граждан РФ. 
    Мы выбираем только самые крупные и надежные банки Киргизии/Казахстана/Беларуси. 

    Для оформления карты потребуется нотариальная доверенность.
    Вы передадите ее в наш офис в Москве. Мы самостоятельно доставим доверенность в банк, откроем на Ваше имя счет, выпустим карту и отправим ее в наш офис в Москве.    """, reply_markup=bank_open())
    elif callback_query.data == "bank_p":
        await bot.send_message(callback_query.from_user.id, f"""Пополняйте карту SWIFT-переводом или с помощью Qiwi, МИР, Сбербанк, Альфа, Тинькофф.""", reply_markup=bank_p())
    elif callback_query.data == "garantia":
        await bot.send_message(callback_query.from_user.id, f"""Наш сервис – официальное юридическое лицо. Работаем по оферте. Транзакции по оплате наших услуг происходят через платежную систему Сloudpayments. Чек об оплате вы получаете на e-mail после оплаты. Если счет не будет открыт в течение гарантийных сроков – мы возвращаем полную стоимость оплаченных услуг.""", reply_markup=garantia())
    elif callback_query.data == "bank_v":
        await bot.send_message(callback_query.from_user.id, f"""Карту возможно выпустить в Долларах США.""", reply_markup=bank_v())
    elif callback_query.data == "kontakt":
        await bot.send_message(callback_query.from_user.id, f"""• Время консультаций в чат-боте:
    ежедневно с 9:00 до 22:00.

    • Время работы офиса:
    пн-пт с 11:00 до 18:00.
    Адрес: г. Москва,
    Дубнинская ул., 83.
    • Тел: +7 (495) 477-59-76.""", reply_markup=kontakt())
        # with open("rasm.jpg"):
        #     await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=filename)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)