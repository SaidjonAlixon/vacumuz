import logging
import os
from uuid import uuid4
from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes
from config import ADMIN_CHAT_ID, SERVICES, BRAND_IMAGES, MODEL_IMAGES
from models import Cart, format_price
from database import db, User, Order, OrderItem
from admin_panel import (
    admin_panel_keyboard, broadcast_keyboard, reports_keyboard,
    start_broadcast, process_broadcast_message, send_broadcast, generate_report
)
from keyboards import (
    start_keyboard, admin_start_keyboard, brand_keyboard, models_keyboard,
    services_keyboard, cart_keyboard, admin_order_keyboard, edit_cart_keyboard
)
from utils import (
    welcome_text, brand_selection_text, model_selection_text,
    services_selection_text, cart_text, order_summary_text, admin_order_text,
    cart_empty_text, service_added_text, service_removed_text,
    order_confirmed_text, order_rejected_text
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Botni ishga tushirish"""
    # Foydalanuvchi ma'lumotlarini saqlash
    user = update.effective_user
    
    # Database ga foydalanuvchini saqlash
    user_obj = User(
        user_id=user.id,
        username=user.username or "",
        full_name=user.full_name or ""
    )
    db.create_or_update_user(user_obj)
    
    # Context ga ma'lumotlarni saqlash
    context.user_data["user_info"] = {
        "user_id": user.id,
        "full_name": user.full_name,
        "username": user.username
    }
    
    # Yangi savatcha yaratish
    context.user_data["cart"] = Cart()
    
    # Admin tekshirish va tegishli keyboard yuborish
    if user.id == ADMIN_CHAT_ID:
        keyboard = admin_start_keyboard()
    else:
        keyboard = start_keyboard()
    
    await update.message.reply_text(
        welcome_text(),
        reply_markup=keyboard,
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
        
        # Brend rasmini yuborish
        image_path = BRAND_IMAGES.get(brand, "")
        if image_path:
            try:
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as photo:
                        await query.edit_message_media(
                            media=InputMediaPhoto(media=photo, caption=model_selection_text(brand)),
                            reply_markup=models_keyboard(brand)
                        )
                else:
                    await query.message.reply_text(
                        model_selection_text(brand),
                        reply_markup=models_keyboard(brand),
                        parse_mode="Markdown"
                    )
            except Exception as e:
                logger.error(f"Brend rasmi yuborishda xatolik: {e}")
                await query.message.reply_text(
                    model_selection_text(brand),
                    reply_markup=models_keyboard(brand),
                    parse_mode="Markdown"
                )
        else:
            await query.message.reply_text(
                model_selection_text(brand),
                reply_markup=models_keyboard(brand),
                parse_mode="Markdown"
            )
        return
    
    # Model tanlash - kuzov turi avtomatik aniqlanadi
    if data.startswith("model|"):
        model = data.split("|", 1)[1]
        cart.set_model(cart.brand, model)
        context.user_data["page"] = 0
        
        # Model rasmini yuborish
        image_path = MODEL_IMAGES.get(cart.brand, {}).get(model, "")
        if image_path:
            try:
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as photo:
                        await query.edit_message_media(
                            media=InputMediaPhoto(media=photo, caption=services_selection_text(cart.body, cart.brand, cart.model)),
                            reply_markup=services_keyboard(cart.body, page=0, selected_services=cart.items)
                        )
                else:
                    await query.message.reply_text(
                        services_selection_text(cart.body, cart.brand, cart.model),
                        reply_markup=services_keyboard(cart.body, page=0, selected_services=cart.items),
                        parse_mode="Markdown"
                    )
            except Exception as e:
                logger.error(f"Model rasmi yuborishda xatolik: {e}")
                await query.message.reply_text(
                    services_selection_text(cart.body, cart.brand, cart.model),
                    reply_markup=services_keyboard(cart.body, page=0, selected_services=cart.items),
                    parse_mode="Markdown"
                )
        else:
            await query.message.reply_text(
                services_selection_text(cart.body, cart.brand, cart.model),
                reply_markup=services_keyboard(cart.body, page=0, selected_services=cart.items),
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
    
    # Savatchani tahrirlash - xizmatlar
    if data == "edit|services":
        context.user_data["page"] = 0
        await query.edit_message_text(
            services_selection_text(cart.body, cart.brand, cart.model),
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
        
        # Database ga buyurtmani saqlash
        user_info = context.user_data.get("user_info", {})
        
        # Order obyektini yaratish
        order = Order(
            order_id=order_id,
            user_id=user_info["user_id"],
            brand=cart.brand,
            model=cart.model,
            body_type=cart.body,
            total_amount=cart.total(),
            status="pending"
        )
        
        # OrderItem obyektlarini yaratish
        order_items = []
        for service_key in cart.items:
            service = SERVICES[service_key]
            order_items.append(OrderItem(
                order_id=order_id,
                service_key=service_key,
                service_name=service["name"],
                price=service["prices"][cart.body]
            ))
        
        # Database ga saqlash
        if db.create_order(order, order_items):
            logger.info(f"Buyurtma saqlandi: {order_id}")
        else:
            logger.error(f"Buyurtma saqlashda xatolik: {order_id}")
        
        # Mijozga buyurtma xulosasi
        await query.message.reply_text(
            order_summary_text(cart, order_id),
            parse_mode="Markdown"
        )
        
        # Adminga buyurtma yuborish
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
    if data.startswith("admin|") and len(data.split("|")) == 4:
        _, action, order_id, user_id = data.split("|")
        user_id = int(user_id)
        
        # Database da buyurtma holatini yangilash
        new_status = "confirmed" if action == "ok" else "cancelled"
        admin_id = update.effective_user.id if action == "ok" else None
        if db.update_order_status(order_id, new_status, admin_id):
            logger.info(f"Buyurtma holati yangilandi: {order_id} -> {new_status}")
        else:
            logger.error(f"Buyurtma holatini yangilashda xatolik: {order_id}")
        
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
            await query.message.reply_text(
                brand_selection_text(),
                reply_markup=brand_keyboard(),
                parse_mode="Markdown"
            )
        elif target == "models":
            await query.message.reply_text(
                model_selection_text(cart.brand),
                reply_markup=models_keyboard(cart.brand),
                parse_mode="Markdown"
            )
        elif target == "services":
            page = context.user_data.get("page", 0)
            await query.message.reply_text(
                services_selection_text(cart.body, cart.brand, cart.model),
                reply_markup=services_keyboard(cart.body, page, selected_services=cart.items),
                parse_mode="Markdown"
            )
        return
    
    # Admin panel handlerlari (2 qismli admin| callback lar uchun)
    if data.startswith("admin|") and len(data.split("|")) == 2:
        _, action = data.split("|")
        
        if action == "panel":
            # Statistikani olish
            total_users = len(db.get_all_users())
            total_orders = len(db.get_all_orders())
            pending_orders = len([o for o in db.get_all_orders() if o.status == "pending"])
            
            text = f"""🔧 **Admin Panel**

📊 **Statistika:**
👥 Jami foydalanuvchilar: {total_users}
📋 Jami buyurtmalar: {total_orders}
⏳ Kutilayotgan buyurtmalar: {pending_orders}

**Mavjud funksiyalar:**"""
            
            await query.edit_message_text(
                text,
                reply_markup=admin_panel_keyboard(),
                parse_mode="Markdown"
            )
            return
        
        elif action == "broadcast":
            await query.edit_message_text(
                "📢 **Xabar yuborish**\n\nXabar turini tanlang:",
                reply_markup=broadcast_keyboard(),
                parse_mode="Markdown"
            )
            return
        
        elif action == "reports":
            await query.edit_message_text(
                "📊 **Hisobotlar**\n\nHisobot turini tanlang:",
                reply_markup=reports_keyboard(),
                parse_mode="Markdown"
            )
            return
        
        elif action == "orders":
            # Barcha buyurtmalarni olish
            orders = db.get_all_orders()
            
            if not orders:
                await query.edit_message_text("📋 Hozircha buyurtmalar yo'q.")
                return
            
            # Buyurtmalarni guruhlash
            pending_orders = [o for o in orders if o.status == "pending"]
            confirmed_orders = [o for o in orders if o.status == "confirmed"]
            completed_orders = [o for o in orders if o.status == "completed"]
            cancelled_orders = [o for o in orders if o.status == "cancelled"]
            
            text = f"""📊 **Buyurtmalar statistikasi**

🔄 **Kutilmoqda:** {len(pending_orders)}
✅ **Tasdiqlangan:** {len(confirmed_orders)}
🏁 **Bajarilgan:** {len(completed_orders)}
❌ **Bekor qilingan:** {len(cancelled_orders)}

📋 **Jami buyurtmalar:** {len(orders)}

**So'nggi 5 ta buyurtma:**"""
            
            for order in orders[:5]:
                user = db.get_user(order.user_id)
                username = f"@{user.username}" if user and user.username else "Noma'lum"
                text += f"\n\n🆔 **{order.order_id}**"
                text += f"\n👤 {username}"
                text += f"\n🚗 {order.brand} {order.model}"
                text += f"\n💰 {format_price(order.total_amount)}"
                text += f"\n📊 {order.status}"
                text += f"\n📅 {order.created_at[:10]}"
            
            await query.edit_message_text(text, parse_mode="Markdown")
            return
        
        elif action == "users":
            users = db.get_all_users()
            
            if not users:
                await query.edit_message_text("👥 Hozircha foydalanuvchilar yo'q.")
                return
            
            text = "👥 **Foydalanuvchilar**\n\n📊 Jami: " + str(len(users)) + " ta\n\n**So'nggi 10 ta foydalanuvchi:**"
            
            for user in users[:10]:
                text += f"\n\n👤 **{user.full_name}**"
                if user.username:
                    text += f"\n📱 @{user.username}"
                else:
                    text += "\n📱 Username yo'q"
                text += f"\n🆔 ID: `{user.user_id}`"
                text += f"\n📅 {user.created_at[:10]}"
            
            await query.edit_message_text(text, parse_mode="Markdown")
            return
        
        elif action == "close":
            await query.edit_message_text("✅ Admin panel yopildi.")
            return
    
    
    # Xabar yuborish handlerlari
    if data.startswith("broadcast|"):
        message_type = data.split("|", 1)[1]
        await start_broadcast(update, context, message_type)
        return
    
    if data == "confirm|broadcast":
        await send_broadcast(update, context)
        return
    
    if data == "cancel|broadcast":
        await query.edit_message_text(
            "❌ Xabar yuborish bekor qilindi.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Admin panel", callback_data="admin|panel")
            ]])
        )
        return
    
    # Hisobot handlerlari
    if data.startswith("report|"):
        report_type = data.split("|", 1)[1]
        await generate_report(update, context, report_type)
        return
    
    # Hech narsa qilmaslik
    if data == "noop":
        return


async def admin_orders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin buyurtmalarni ko'rish buyrug'i"""
    user_id = update.effective_user.id
    
    # Admin tekshirish
    if user_id != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
        return
    
    # Barcha buyurtmalarni olish
    orders = db.get_all_orders()
    
    if not orders:
        await update.message.reply_text("📋 Hozircha buyurtmalar yo'q.")
        return
    
    # Buyurtmalarni guruhlash
    pending_orders = [o for o in orders if o.status == "pending"]
    confirmed_orders = [o for o in orders if o.status == "confirmed"]
    completed_orders = [o for o in orders if o.status == "completed"]
    cancelled_orders = [o for o in orders if o.status == "cancelled"]
    
    text = f"""📊 **Buyurtmalar statistikasi**

🔄 **Kutilmoqda:** {len(pending_orders)}
✅ **Tasdiqlangan:** {len(confirmed_orders)}
🏁 **Bajarilgan:** {len(completed_orders)}
❌ **Bekor qilingan:** {len(cancelled_orders)}

📋 **Jami buyurtmalar:** {len(orders)}

**So'nggi 5 ta buyurtma:**"""
    
    for order in orders[:5]:
        user = db.get_user(order.user_id)
        username = f"@{user.username}" if user and user.username else "Noma'lum"
        text += f"\n\n🆔 **{order.order_id}**"
        text += f"\n👤 {username}"
        text += f"\n🚗 {order.brand} {order.model}"
        text += f"\n💰 {format_price(order.total_amount)}"
        text += f"\n📊 {order.status}"
        text += f"\n📅 {order.created_at[:10]}"
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def admin_order_detail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin buyurtma tafsilotlarini ko'rish"""
    user_id = update.effective_user.id
    
    # Admin tekshirish
    if user_id != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
        return
    
    # Buyurtma ID ni olish
    if not context.args:
        await update.message.reply_text("❌ Buyurtma ID ni kiriting.\nMasalan: `/order 12345678`")
        return
    
    order_id = context.args[0]
    order_data = db.get_order_with_items(order_id)
    
    if not order_data:
        await update.message.reply_text(f"❌ Buyurtma `{order_id}` topilmadi.")
        return
    
    order = order_data['order']
    items = order_data['items']
    user = db.get_user(order.user_id)
    
    user_name = user.full_name if user else 'Noma\'lum'
    user_username = user.username if user and user.username else 'Noma\'lum'
    
    text = f"""📋 **Buyurtma tafsilotlari**

🆔 **ID:** `{order.order_id}`
👤 **Mijoz:** {user_name}
📱 **Username:** @{user_username}
🆔 **User ID:** `{order.user_id}`

🚗 **Mashina:**
• Brend: {order.brand}
• Model: {order.model}
• Kuzov: {order.body_type}

🔧 **Xizmatlar:**"""
    
    for item in items:
        text += f"\n• {item.service_name} — {format_price(item.price)}"
    
    text += f"""

💰 **Umumiy summa:** {format_price(order.total_amount)}
📊 **Holat:** {order.status}
📅 **Yaratilgan:** {order.created_at}
📅 **Yangilangan:** {order.updated_at}"""
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def fallback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Boshqa barcha xabarlarni boshqarish"""
    text = (update.message.text or "").strip()
    
    if text == "🚗 Boshlash" or text.lower() == "boshlash":
        return await boshlash_handler(update, context)
    
    if text == "🔧 Admin Panel" or text.lower() == "admin panel":
        # Admin tekshirish
        user_id = update.effective_user.id
        if user_id != ADMIN_CHAT_ID:
            await update.message.reply_text("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
            return
        
        # Admin panel statistikasi
        total_users = len(db.get_all_users())
        total_orders = len(db.get_all_orders())
        pending_orders = len([o for o in db.get_all_orders() if o.status == "pending"])
        
        text = f"""🔧 **Admin Panel**

📊 **Statistika:**
👥 Jami foydalanuvchilar: {total_users}
📋 Jami buyurtmalar: {total_orders}
⏳ Kutilayotgan buyurtmalar: {pending_orders}

**Mavjud funksiyalar:**"""
        
        await update.message.reply_text(
            text,
            reply_markup=admin_panel_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    # Admin panel uchun xabar yuborish
    if context.user_data.get("broadcast_type"):
        return await process_broadcast_message(update, context)
    
    await update.message.reply_text(
        "Tugmalar orqali harakat qiling. /start ni bosing yoki \"🚗 Boshlash\" tugmasini tanlang."
    )
