from config import BODY_TYPES, SERVICES
from models import format_price


def cart_text(cart) -> str:
    """Savatcha matnini formatlash"""
    lines = [
        "🚗 **Buyurtma ma'lumotlari**",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🏷️ **Brend:** {cart.brand}",
        f"🚙 **Model:** {cart.model}",
        f"🚐 **Kuzov turi:** {BODY_TYPES.get(cart.body, '')}",
        "",
        "🔧 **Tanlangan xizmatlar:**"
    ]
    
    if not cart.items:
        lines.append("— Hali xizmat tanlanmadi")
    else:
        for i, key in enumerate(cart.items, 1):
            service = SERVICES[key]
            price = service["prices"][cart.body]
            price_text = format_price(price)
            lines.append(f"{i}. {service['name']} — {price_text}")
        
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"💰 **Umumiy summa: {format_price(cart.total())}**")
    
    return "\n".join(lines)


def order_summary_text(cart, order_id: str) -> str:
    """Buyurtma xulosasi matni"""
    lines = [
        "📋 **Buyurtma xulosasi**",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🆔 **Buyurtma ID:** `{order_id}`",
        f"🏷️ **Brend:** {cart.brand}",
        f"🚙 **Model:** {cart.model}",
        f"🚐 **Kuzov turi:** {BODY_TYPES.get(cart.body, '')}",
        "",
        "🔧 **Xizmatlar:**"
    ]
    
    for i, key in enumerate(cart.items, 1):
        service = SERVICES[key]
        price = service["prices"][cart.body]
        price_text = format_price(price)
        lines.append(f"{i}. {service['name']} — {price_text}")
    
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"💰 **Umumiy summa: {format_price(cart.total())}**")
    lines.append("")
    lines.append("✅ Buyurtma adminga yuborildi. Tasdiqni kuting.")
    
    return "\n".join(lines)


def admin_order_text(cart, order_id: str, user_info: dict) -> str:
    """Admin uchun buyurtma matni"""
    lines = [
        "🆕 **Yangi buyurtma**",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🆔 **Buyurtma ID:** `{order_id}`",
        f"👤 **Mijoz:** {user_info.get('full_name', 'Noma lum')}",
        f"📱 **Username:** @{user_info.get('username', 'Noma lum')}",
        f"🆔 **User ID:** `{user_info.get('user_id', 'Noma lum')}`",
        "",
        f"🏷️ **Brend:** {cart.brand}",
        f"🚙 **Model:** {cart.model}",
        f"🚐 **Kuzov turi:** {BODY_TYPES.get(cart.body, '')}",
        "",
        "🔧 **Xizmatlar:**"
    ]
    
    for i, key in enumerate(cart.items, 1):
        service = SERVICES[key]
        price = service["prices"][cart.body]
        price_text = format_price(price)
        lines.append(f"{i}. {service['name']} — {price_text}")
    
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"💰 **Umumiy summa: {format_price(cart.total())}**")
    
    return "\n".join(lines)


def welcome_text() -> str:
    """Xush kelibsiz matni"""
    return """🚗 **Avtomobil Detailing Xizmatlari**

Assalomu alaykum! Botga hush kelibsiz 👋

Bu bot orqali siz:
• Avtomobilingiz brendi va modelini tanlashingiz
• Kuzov turini belgilashingiz  
• Kerakli xizmatlarni tanlashingiz
• Narxlarni ko'rishingiz
• Buyurtma berishingiz mumkin

Boshlash uchun "🚗 Boshlash" tugmasini bosing."""


def brand_selection_text() -> str:
    """Brend tanlash matni"""
    return "🏷️ **Brend tanlang:**\n\nQuyidagi brendlardan birini tanlang:"


def model_selection_text(brand: str) -> str:
    """Model tanlash matni"""
    return f"✅ **Brend:** {brand}\n\n🚙 **Model tanlang:**\n\n{brand} brendining modellaridan birini tanlang. Model tanlaganingizdan so'ng kuzov turi avtomatik aniqlanadi:"




def services_selection_text(body_type: str, brand: str = "", model: str = "") -> str:
    """Xizmatlar tanlash matni"""
    body_name = BODY_TYPES.get(body_type, '')
    
    lines = [f"✅ **Kuzov turi:** {body_name}"]
    
    if brand and model:
        lines.append(f"🚗 **Mashina:** {brand} {model}")
    
    lines.extend([
        "",
        "🔧 **Xizmatlarni tanlang:**",
        "",
        "Kerakli xizmatlarni tanlang (bo'limlar bo'yicha sahifalangan):"
    ])
    
    return "\n".join(lines)


def cart_empty_text() -> str:
    """Bo'sh savatcha matni"""
    return "🧺 **Savatcha bo'sh**\n\nHali hech qanday xizmat tanlanmadi. Xizmatlarni tanlash uchun orqaga qayting."


def service_added_text(service_name: str, price: int) -> str:
    """Xizmat qo'shilgan matni"""
    return f"✅ **{service_name}** qo'shildi\n💰 Narx: {format_price(price)}"


def service_removed_text(service_name: str) -> str:
    """Xizmat olib tashlangan matni"""
    return f"❌ **{service_name}** olib tashlandi"


def order_confirmed_text(order_id: str) -> str:
    """Buyurtma tasdiqlangan matni"""
    return f"✅ **Buyurtma tasdiqlandi!**\n\n🆔 Buyurtma ID: `{order_id}`\n\nRahmat! Buyurtmangiz qabul qilindi."


def order_rejected_text(order_id: str) -> str:
    """Buyurtma rad etilgan matni"""
    return f"❌ **Buyurtma rad etildi**\n\n🆔 Buyurtma ID: `{order_id}`\n\nKechirasiz, buyurtmangiz rad etildi."
