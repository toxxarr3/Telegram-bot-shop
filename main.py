import asyncio, logging, kb, db
from aiogram import F, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



#--------------------->>/imports
#--------------------->>inits



dp=Dispatcher()
tk="" # Cюда вписать токен бота
bot=Bot(token=tk)
class Form(StatesGroup):
    address=State()



#--------------------->>/inits
#--------------------->>handlers



@dp.message(Command("start"))
async def comstart(message: Message):
    us=db.useridinbase(message.from_user.id)
    if us==1:
        pass
    else:
        db.adduser(userid=message.from_user.id, username=message.from_user.username)
    await message.answer("Добро пожаловать в магазин бытовых товаров!")
    await message.answer(text="Главное меню", reply_markup=kb.mainkb())

#--------------------->>callbacks

@dp.callback_query(F.data == "show_cats")
async def call_showcats(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.edit_text(text="Категории товаров:", reply_markup=kb.catskb())
    except Exception:
        await callback.message.delete()
        await callback.message.answer("Категории товаров:", reply_markup=kb.catskb())



@dp.callback_query(F.data.startswith("cat_"))
async def call_one_cat(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"Категория {str(callback.data[4:])}", reply_markup=kb.show_cat(callback.data[4:]))



@dp.callback_query(F.data=="main")
async def call_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Главное меню:", reply_markup=kb.mainkb())



@dp.callback_query(F.data.startswith("prod_"))
async def call_prodinfo(callback: CallbackQuery):
    a=db.prod_info(prodname=callback.data[5:])
    try:
        b=f"Название:\n{callback.data[5:]}\nОписание:\n{a[0]}\nЦена:\n{a[1]}"#\nphoto:\n{a[2]}"
        ph=FSInputFile(path=a[2])
        me=InputMediaPhoto(media=ph, caption=b)
        await callback.answer()
        await callback.message.edit_media(media=me, reply_markup=kb.prodkb(prod=callback.data[5:]))
    except Exception:
        b=f"Название:\n{callback.data[5:]}\nОписание:\n{a[0]}\nЦена:\n{a[1]}"
        await callback.answer()
        await callback.message.edit_text(text=b, reply_markup=kb.prodkb(prod=callback.data[5:]))



@dp.callback_query(F.data.startswith("add_"))
async def call_add_to_cart_handler(callback: CallbackQuery):
    prod_name = callback.data[4:]
    user_id = callback.from_user.id
    db.add_to_cart(user_id, prod_name)
    await callback.answer("✅ Добавлено в корзину!")
    await callback.message.edit_reply_markup(reply_markup=kb.prodkb(prod_name))



@dp.callback_query(F.data == "show_cart")
async def call_show_cart(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    cart = db.showcart(user_id)
    if not cart:
        text = "🛒 Ваша корзина пуста"
        try:
            await callback.message.edit_text(text=text, reply_markup=kb.nocartkb())
        except Exception:
            await callback.message.delete()
            await callback.message.answer(text, reply_markup=kb.nocartkb(), parse_mode="Markdown")
    else:
        text = "🛒 Ваша корзина:\n\n"
        total = 0
        for prod_name, qty in cart.items():
            prod_data = db.prod_info(prod_name)
            price = prod_data[1] if prod_data else 0
            line_sum = price * qty
            total += line_sum
            text += f"📦 {prod_name} x {qty} = `{line_sum}`₽\n"
        text += f"\n💰 *Итого:* `{total}`₽"
        try:
            await callback.message.edit_text(text=text, reply_markup=kb.cartkb())
        except Exception:
            await callback.message.delete()
            await callback.message.answer(text, reply_markup=kb.cartkb(), parse_mode="Markdown")



@dp.callback_query(F.data == "clear_cart")
async def call_clear_cart_handler(callback: CallbackQuery):
    db.clearcart(callback.from_user.id)
    await callback.answer("Корзина очищена")
    try:
        await callback.message.edit_text(text="Главное меню", reply_markup=kb.mainkb())
    except Exception:
        await callback.message.delete()
        await callback.message.answer("Главное меню", reply_markup=kb.mainkb())



@dp.callback_query(F.data=="input_address")
async def call_input_address_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.address)
    await call.answer()
    await call.message.answer("Введите ваш адрес:")



@dp.message(Form.address)
async def msg_input_address_state(message: Message, state: FSMContext):
    address= message.text
    cart=db.showcart(tgid=message.from_user.id)
    userid= db.getuserid(message.from_user.id)[0]
    total = 0
    for prod_name, qty in cart.items():
        prod_data = db.prod_info(prod_name)
        price = prod_data[1] if prod_data else 0
        line_sum = price * qty
        total+=line_sum
    price=total
    db.add_order(userid=userid, cart=cart, address=address, price=price)
    await state.clear()
    db.clearcart(tgid=message.from_user.id)
    await message.answer("✅Заказ создан, вскоре мы его обработаем!")
    await message.answer("Главное меню", reply_markup=kb.mainkb())

@dp.callback_query(F.data=="show_orders")
async def call_show_orders(callback: CallbackQuery):
    orders=db.show_orders(tgid=callback.from_user.id)
    text="Ваши заказы:\n"
    for o in orders:
        text+=f"\n---------------\n\nЗаказ: {o[0]},\nАдрес заказа: {o[1]}\nСуммарная цена: {o[2]}₽\n"
    await callback.answer()
    await callback.message.edit_text(text=text)
    await callback.message.answer(text="Главное меню", reply_markup=kb.mainkb())



#--------------------->>/callbacks



@dp.message(F.text)
async def anytext(message: Message):
    await message.answer("Пожалуйста, используйте Inline-клавиатуру")

#--------------------->>/handlers



# _______________________________
#|          run                  |
#|_______________________________|



async def runbot():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


try:
    asyncio.run(runbot())
except KeyboardInterrupt:
    print("bot stop")