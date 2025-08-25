import logging
from uuid import uuid4
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_CHAT_ID, SERVICES
from models import Cart, format_price
from keyboards import (
    start_keyboard, brand_keyboard, models_keyboard, body_keyboard,
    services_keyboard, cart_keyboard, admin_order_keyboard, edit_cart_keyboard
)
from utils import (
    welcome_text, brand_selection_text, model_selection_text, body_selection_text,
    services_selection_text, cart_text, order_summary_text, admin_order_text,
    cart_empty_text, service_added_text, service_removed_text,
    order_confirmed_text, order_rejected_text
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Botni ishga tushirish"""
    # Foydalanuvchi ma'lumotlarini saqlash
    user = update.effective_user
    context.user_data["user_info"] = {
        "user_id": user.id,
        "full_name": user.full_name,
        "username": user.username
    }
    
    # Yangi savatcha yaratish
    context.user_data["cart"] = Cart()
    
    await update.message.reply_text(
        welcome_text(),
        reply_markup=start_keyboard(),
        parse_mode="Markdown"
    )


async def boshlash_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Boshlash tugmasi bosilganda"""
    await update.message.reply_text(
        brand_selection_text(),
        reply_markup=brand_keyboard(),
        parse_mode="Markdown"
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha callback query larni boshqarish"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    cart: Cart = context.user_data.get("cart", Cart())
    context.user_data["cart"] = cart
    
    # Brend tanlash
    if data.startswith("brand|"):
        brand = data.split("|", 1)[1]
        cart.brand = brand
        cart.model = ""
        cart.body = ""
        cart.items.clear()
        
        await query.edit_message_text(
            model_selection_text(brand),
            reply_markup=models_keyboard(brand),
            parse_mode="Markdown"
        )
        return
    
    # Model tanlash
    if data.startswith("model|"):
        model = data.split("|", 1)[1]
        cart.model = model
        cart.body = ""
        cart.items.clear()
        
        await query.edit_message_text(
            body_selection_text(model),
            reply_markup=body_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    # Kuzov turi tanlash
    if data.startswith("body|"):
        body = data.split("|", 1)[1]
        cart.body = body
        context.user_data["page"] = 0
        
        await query.edit_message_text(
            services_selection_text(body),
            reply_markup=services_keyboard(body, page=0, selected_services=cart.items),
            parse_mode="Markdown"
        )
        return
    
    # Sahifa navigatsiyasi
    if data.startswith("page|"):
        page = int(data.split("|", 1)[1])
        context.user_data["page"] = page
        
        await query.edit_message_reply_markup(
            reply_markup=services_keyboard(cart.body, page, selected_services=cart.items)
        )
        return
    
    # Xizmat tanlash/olib tashlash
    if data.startswith("svc|"):
        service_key = data.split("|", 1)[1]
        service = SERVICES[service_key]
        
        if service_key in cart.items:
            cart.remove_item(service_key)
            message = service_removed_text(service["name"])
            # Xizmat olib tashlanganda xabar ko'rsatish
            await query.answer(message, show_alert=True)
        else:
            cart.add_item(service_key)
            price = service["prices"][cart.body]
            message = service_added_text(service["name"], price)
            # Xizmat qo'shilganda xabar ko'rsatish
            await query.answer(message, show_alert=True)
        
        # Klaviatura yangilash - tanlangan xizmatlar ko'rinishini yangilash
        current_page = context.user_data.get("page", 0)
        await query.edit_message_reply_markup(
            reply_markup=services_keyboard(cart.body, current_page, selected_services=cart.items)
        )
        
        # Savatcha holatini qisqa xabar sifatida ko'rsatish
        if cart.items:
            cart_status = f"🧺 Savatchada: {len(cart.items)} ta xizmat • Umumiy: {format_price(cart.total())}"
            await query.answer(cart_status, show_alert=False)
        
        return
    
    # Savatcha ko'rish
    if data == "cart|show":
        if not cart.items:
            await query.message.reply_text(
                cart_empty_text(),
                parse_mode="Markdown"
            )
        else:
            await query.message.reply_text(
                cart_text(cart),
                reply_markup=cart_keyboard(),
                parse_mode="Markdown"
            )
        return
    
    # Savatchani qaytadan boshlash
    if data == "cart|restart":
        cart.clear()
        await query.edit_message_text(
            brand_selection_text(),
            reply_markup=brand_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    # Savatchani tahrirlash
    if data == "cart|edit":
        await query.edit_message_reply_markup(reply_markup=edit_cart_keyboard())
        return
    
    # Savatchani tahrirlash - brend
    if data == "edit|brand":
        cart.model = ""
        cart.body = ""
        cart.items.clear()
        await query.edit_message_text(
            brand_selection_text(),
            reply_markup=brand_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    # Savatchani tahrirlash - model
    if data == "edit|model":
        cart.body = ""
        cart.items.clear()
        await query.edit_message_text(
            model_selection_text(cart.brand),
            reply_markup=models_keyboard(cart.brand),
            parse_mode="Markdown"
        )
        return
    
    # Savatchani tahrirlash - kuzov
    if data == "edit|body":
        cart.items.clear()
        await query.edit_message_text(
            body_selection_text(cart.model),
            reply_markup=body_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    # Savatchani tahrirlash - xizmatlar
    if data == "edit|services":
        context.user_data["page"] = 0
        await query.edit_message_text(
            services_selection_text(cart.body),
            reply_markup=services_keyboard(cart.body, page=0, selected_services=cart.items),
            parse_mode="Markdown"
        )
        return
    
    # Buyurtmani yakunlash
    if data == "cart|finish":
        if not cart.items:
            await query.answer("Avval kamida 1 ta xizmat tanlang.", show_alert=True)
            return
        
        order_id = str(uuid4())[:8]
        context.user_data["order_id"] = order_id
        
        # Mijozga buyurtma xulosasi
        await query.message.reply_text(
            order_summary_text(cart, order_id),
            parse_mode="Markdown"
        )
        
        # Adminga buyurtma yuborish
        user_info = context.user_data.get("user_info", {})
        admin_text = admin_order_text(cart, order_id, user_info)
        admin_kb = admin_order_keyboard(order_id, user_info["user_id"])
        
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_text,
            reply_markup=admin_kb,
            parse_mode="Markdown"
        )
        return
    
    # Admin buyurtma tasdiqlash/bekor qilish
    if data.startswith("admin|"):
        _, action, order_id, user_id = data.split("|")
        user_id = int(user_id)
        
        if action == "ok":
            # Buyurtma tasdiqlandi
            await update.effective_message.edit_reply_markup(reply_markup=None)
            await update.effective_message.reply_text(f"✅ Buyurtma {order_id} tasdiqlandi.")
            
            # Mijozga xabar
            await context.bot.send_message(
                chat_id=user_id,
                text=order_confirmed_text(order_id),
                parse_mode="Markdown"
            )
        else:
            # Buyurtma rad etildi
            await update.effective_message.edit_reply_markup(reply_markup=None)
            await update.effective_message.reply_text(f"❌ Buyurtma {order_id} bekor qilindi.")
            
            # Mijozga xabar
            await context.bot.send_message(
                chat_id=user_id,
                text=order_rejected_text(order_id),
                parse_mode="Markdown"
            )
        return
    
    # Orqaga qaytish
    if data.startswith("back|"):
        target = data.split("|", 1)[1]
        
        if target == "brands":
            await query.edit_message_text(
                brand_selection_text(),
                reply_markup=brand_keyboard(),
                parse_mode="Markdown"
            )
        elif target == "models":
            await query.edit_message_text(
                model_selection_text(cart.brand),
                reply_markup=models_keyboard(cart.brand),
                parse_mode="Markdown"
            )
        elif target == "body":
            await query.edit_message_text(
                body_selection_text(cart.model),
                reply_markup=body_keyboard(),
                parse_mode="Markdown"
            )
        elif target == "services":
            page = context.user_data.get("page", 0)
            await query.edit_message_text(
                services_selection_text(cart.body),
                reply_markup=services_keyboard(cart.body, page, selected_services=cart.items),
                parse_mode="Markdown"
            )
        return
    
    # Hech narsa qilmaslik
    if data == "noop":
        return


async def fallback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Boshqa barcha xabarlarni boshqarish"""
    text = (update.message.text or "").strip()
    
    if text == "🚗 Boshlash" or text.lower() == "boshlash":
        return await boshlash_handler(update, context)
    
    await update.message.reply_text(
        "Tugmalar orqali harakat qiling. /start ni bosing yoki \"🚗 Boshlash\" tugmasini tanlang."
    )
