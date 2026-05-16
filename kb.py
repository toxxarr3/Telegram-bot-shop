from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, callback_query
import db

back=[InlineKeyboardButton(text="<-Назад", callback_data="main")]
backtocats=[InlineKeyboardButton(text="<--|Назад к категориям", callback_data="show_cats")]

def mainkb():
    kb=[[InlineKeyboardButton(text="Категории", callback_data="show_cats")],
         [InlineKeyboardButton(text="Корзина", callback_data="show_cart")],
         [InlineKeyboardButton(text="Ваши заказы", callback_data="show_orders")]]
    keyboard=InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def catskb(): #all cats
    kb=[back]
    cats=db.allcats()
    for c in cats:
        c=str(c)
        kb.append([InlineKeyboardButton(text=c, callback_data=f"cat_{c}")])
    keyboard=InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def show_cat(cat): #prods in 1 cat
    kb=[backtocats]
    prods=db.prodsincat(cat)
    for p in prods:
        kb.append([InlineKeyboardButton(text=str(p), callback_data=f"prod_{str(p)}")])
    keyboard=InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def nocartkb():
    kb=[back]
    keyboard=InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def cartkb():
    kb=[[InlineKeyboardButton(text="Очистить корзину", callback_data="clear_cart")], [InlineKeyboardButton(text="Заказать", callback_data="input_address")], back]
    keyboard=InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def prodkb(prod):
    kb=[[InlineKeyboardButton(text=f"Добавить {prod} в корзину", callback_data=f"add_{prod}")], backtocats]
    keyboard=InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard