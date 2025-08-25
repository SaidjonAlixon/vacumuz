from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import BRANDS, BODY_TYPES, SERVICES, SERVICE_GROUPS
from models import chunk_buttons, format_price
from typing import List


def start_keyboard():
    """Boshlash tugmasi"""
    return ReplyKeyboardMarkup([[KeyboardButton("🚗 Boshlash")]], resize_keyboard=True)


def brand_keyboard():
    """Brend tanlash tugmalari"""
    options = [(f"🚗 {brand}", f"brand|{brand}") for brand in BRANDS.keys()]
    button_chunks = chunk_buttons(options, row=2)
    
    # Har bir qator uchun InlineKeyboardButton yaratish
    buttons = []
    for row in button_chunks:
        row_buttons = []
        for text, data in row:
            row_buttons.append(InlineKeyboardButton(text, callback_data=data))
        buttons.append(row_buttons)
    
    return InlineKeyboardMarkup(buttons)


def models_keyboard(brand: str):
    """Model tanlash tugmalari"""
    models = BRANDS.get(brand, [])
    options = [(f"🚙 {model}", f"model|{model}") for model in models]
    button_chunks = chunk_buttons(options, row=2)
    
    # Har bir qator uchun InlineKeyboardButton yaratish
    buttons = []
    for row in button_chunks:
        row_buttons = []
        for text, data in row:
            row_buttons.append(InlineKeyboardButton(text, callback_data=data))
        buttons.append(row_buttons)
    
    # Orqaga qaytish tugmasi
    buttons.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back|brands")])
    
    return InlineKeyboardMarkup(buttons)


def body_keyboard():
    """Kuzov turi tanlash tugmalari"""
    options = [
        (f"🚗 {BODY_TYPES['sedan']}", "body|sedan"),
        (f"🚙 {BODY_TYPES['suv']}", "body|suv"),
        (f"🚐 {BODY_TYPES['minivan']}", "body|minivan"),
    ]
    button_chunks = chunk_buttons(options, row=1)
    
    # Har bir qator uchun InlineKeyboardButton yaratish
    buttons = []
    for row in button_chunks:
        row_buttons = []
        for text, data in row:
            row_buttons.append(InlineKeyboardButton(text, callback_data=data))
        buttons.append(row_buttons)
    
    buttons.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back|models")])
    
    return InlineKeyboardMarkup(buttons)


def services_keyboard(body: str, page: int = 0, selected_services: List[str] = None):
    """Xizmatlar tanlash tugmalari"""
    if selected_services is None:
        selected_services = []
        
    # Sahifa bo'yicha guruhni olish
    group = SERVICE_GROUPS[page]
    service_keys = [k for k, v in SERVICES.items() if v["group"] == group]
    
    buttons = []
    for key in service_keys:
        service = SERVICES[key]
        name = service["name"]
        price = service["prices"][body]
        price_text = format_price(price)
        
        # Xizmat tanlanganmi tekshirish
        is_selected = key in selected_services
        status_icon = "✅" if is_selected else "🔘"
        
        # Xizmat tanlanganmi tekshirish uchun callback_data
        callback_data = f"svc|{key}"
        
        buttons.append([InlineKeyboardButton(f"{status_icon} {name} • {price_text}", callback_data=callback_data)])
    
    # Sahifa navigatsiyasi
    pager = []
    if page > 0:
        pager.append(InlineKeyboardButton("⬅️", callback_data=f"page|{page-1}"))
    
    pager.append(InlineKeyboardButton(f"📄 {group}", callback_data="noop"))
    
    if page < len(SERVICE_GROUPS) - 1:
        pager.append(InlineKeyboardButton("➡️", callback_data=f"page|{page+1}"))
    
    buttons.append(pager)
    
    # Savatcha va yakunlash tugmalari
    cart_count = len(selected_services)
    cart_text = f"🧺 Savatcha ({cart_count})" if cart_count > 0 else "🧺 Savatcha"
    
    buttons.append([
        InlineKeyboardButton(cart_text, callback_data="cart|show"),
        InlineKeyboardButton("✅ Yakunlash", callback_data="cart|finish")
    ])
    
    # Orqaga qaytish
    buttons.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back|body")])
    
    return InlineKeyboardMarkup(buttons)


def cart_keyboard():
    """Savatcha tugmalari"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Qaytadan boshlash", callback_data="cart|restart"),
            InlineKeyboardButton("✏️ Tahrirlash", callback_data="cart|edit")
        ],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back|services")]
    ])


def admin_order_keyboard(order_id: str, user_id: int):
    """Admin buyurtma tasdiqlash tugmalari"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"admin|ok|{order_id}|{user_id}"),
            InlineKeyboardButton("❌ Bekor qilish", callback_data=f"admin|no|{order_id}|{user_id}")
        ]
    ])


def edit_cart_keyboard():
    """Savatchani tahrirlash tugmalari"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚗 Brend", callback_data="edit|brand"),
            InlineKeyboardButton("🚙 Model", callback_data="edit|model")
        ],
        [
            InlineKeyboardButton("🚐 Kuzov", callback_data="edit|body"),
            InlineKeyboardButton("🔧 Xizmatlar", callback_data="edit|services")
        ],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="cart|show")]
    ])
