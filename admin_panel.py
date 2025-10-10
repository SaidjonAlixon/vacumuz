import logging
import os
import pandas as pd
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import ADMIN_CHAT_ID
from database import db
from models import format_price

logger = logging.getLogger(__name__)

# Admin panel tugmalari
def admin_panel_keyboard():
    """Admin panel asosiy tugmalari"""
    keyboard = [
        [InlineKeyboardButton("📢 Xabar Yuborish", callback_data="admin|broadcast")],
        [InlineKeyboardButton("📊 Hisobotlar", callback_data="admin|reports")],
        [InlineKeyboardButton("📋 Buyurtmalar", callback_data="admin|orders")],
        [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin|users")],
        [InlineKeyboardButton("❌ Yopish", callback_data="admin|close")]
    ]
    return InlineKeyboardMarkup(keyboard)

def broadcast_keyboard():
    """Xabar yuborish tugmalari"""
    keyboard = [
        [InlineKeyboardButton("📝 Matn xabari", callback_data="broadcast|text")],
        [InlineKeyboardButton("🖼️ Rasm + matn", callback_data="broadcast|photo")],
        [InlineKeyboardButton("📹 Video + matn", callback_data="broadcast|video")],
        [InlineKeyboardButton("📎 Fayl + matn", callback_data="broadcast|document")],
        [InlineKeyboardButton("🔗 Kanal xabari", callback_data="broadcast|forward")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="admin|panel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def reports_keyboard():
    """Hisobotlar tugmalari"""
    keyboard = [
        [InlineKeyboardButton("📅 Kunlik hisobot", callback_data="report|daily")],
        [InlineKeyboardButton("📆 Haftalik hisobot", callback_data="report|weekly")],
        [InlineKeyboardButton("📊 Oylik hisobot", callback_data="report|monthly")],
        [InlineKeyboardButton("📈 To'liq hisobot", callback_data="report|full")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="admin|panel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def confirm_broadcast_keyboard():
    """Xabar yuborishni tasdiqlash tugmalari"""
    keyboard = [
        [InlineKeyboardButton("✅ Yuborish", callback_data="confirm|broadcast")],
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel|broadcast")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Admin panel asosiy funksiyasi
async def admin_panel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel buyrug'i"""
    user_id = update.effective_user.id
    
    # Admin tekshirish
    if user_id != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
        return
    
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
    
    await update.message.reply_text(
        text,
        reply_markup=admin_panel_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

# Xabar yuborish funksiyalari
async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE, message_type: str):
    """Xabar yuborishni boshlash"""
    query = update.callback_query
    await query.answer()
    
    context.user_data["broadcast_type"] = message_type
    
    if message_type == "text":
        await query.edit_message_text(
            "📝 **Matn xabari yuborish**\n\nXabarni yuboring:",
            parse_mode=ParseMode.MARKDOWN
        )
    elif message_type == "photo":
        await query.edit_message_text(
            "🖼️ **Rasm + matn yuborish**\n\nRasm va matnni yuboring:",
            parse_mode=ParseMode.MARKDOWN
        )
    elif message_type == "video":
        await query.edit_message_text(
            "📹 **Video + matn yuborish**\n\nVideo va matnni yuboring:",
            parse_mode=ParseMode.MARKDOWN
        )
    elif message_type == "document":
        await query.edit_message_text(
            "📎 **Fayl + matn yuborish**\n\nFayl va matnni yuboring:",
            parse_mode=ParseMode.MARKDOWN
        )
    elif message_type == "forward":
        await query.edit_message_text(
            "🔗 **Kanal xabari yuborish**\n\nKanal xabarini forward qiling:",
            parse_mode=ParseMode.MARKDOWN
        )

async def process_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabar yuborish uchun xabarni qayta ishlash"""
    broadcast_type = context.user_data.get("broadcast_type")
    
    if not broadcast_type:
        return
    
    # Xabarni saqlash
    if broadcast_type == "text":
        context.user_data["broadcast_content"] = update.message.text
    elif broadcast_type == "photo":
        if update.message.photo:
            context.user_data["broadcast_photo"] = update.message.photo[-1].file_id
            context.user_data["broadcast_caption"] = update.message.caption or ""
    elif broadcast_type == "video":
        if update.message.video:
            context.user_data["broadcast_video"] = update.message.video.file_id
            context.user_data["broadcast_caption"] = update.message.caption or ""
    elif broadcast_type == "document":
        if update.message.document:
            context.user_data["broadcast_document"] = update.message.document.file_id
            context.user_data["broadcast_caption"] = update.message.caption or ""
    elif broadcast_type == "forward":
        if update.message.forward_from_chat:
            context.user_data["broadcast_forward"] = {
                "chat_id": update.message.forward_from_chat.id,
                "message_id": update.message.forward_from_message_id
            }
    
    # Foydalanuvchilar sonini olish
    users = db.get_all_users()
    user_count = len(users)
    
    # Tasdiqlash xabari
    preview_text = "📢 **Xabar yuborish tasdiqlash**\n\n"
    
    if broadcast_type == "text":
        preview_text += f"📝 **Matn:**\n{context.user_data['broadcast_content']}\n\n"
    elif broadcast_type == "photo":
        preview_text += f"🖼️ **Rasm + matn:**\n{context.user_data.get('broadcast_caption', '')}\n\n"
    elif broadcast_type == "video":
        preview_text += f"📹 **Video + matn:**\n{context.user_data.get('broadcast_caption', '')}\n\n"
    elif broadcast_type == "document":
        preview_text += f"📎 **Fayl + matn:**\n{context.user_data.get('broadcast_caption', '')}\n\n"
    elif broadcast_type == "forward":
        preview_text += f"🔗 **Kanal xabari forward qilinadi**\n\n"
    
    preview_text += f"👥 **Yuboriladigan foydalanuvchilar:** {user_count} ta\n\n"
    preview_text += "Xabarni yuborishni tasdiqlaysizmi?"
    
    await update.message.reply_text(
        preview_text,
        reply_markup=confirm_broadcast_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabarni barcha foydalanuvchilarga yuborish"""
    query = update.callback_query
    await query.answer()
    
    broadcast_type = context.user_data.get("broadcast_type")
    users = db.get_all_users()
    
    sent_count = 0
    failed_count = 0
    
    # Yuborish jarayonini boshlash
    await query.edit_message_text("📤 Xabar yuborilmoqda...")
    
    for user in users:
        try:
            if broadcast_type == "text":
                await context.bot.send_message(
                    chat_id=user.user_id,
                    text=context.user_data["broadcast_content"],
                    parse_mode=ParseMode.MARKDOWN
                )
            elif broadcast_type == "photo":
                await context.bot.send_photo(
                    chat_id=user.user_id,
                    photo=context.user_data["broadcast_photo"],
                    caption=context.user_data.get("broadcast_caption", ""),
                    parse_mode=ParseMode.MARKDOWN
                )
            elif broadcast_type == "video":
                await context.bot.send_video(
                    chat_id=user.user_id,
                    video=context.user_data["broadcast_video"],
                    caption=context.user_data.get("broadcast_caption", ""),
                    parse_mode=ParseMode.MARKDOWN
                )
            elif broadcast_type == "document":
                await context.bot.send_document(
                    chat_id=user.user_id,
                    document=context.user_data["broadcast_document"],
                    caption=context.user_data.get("broadcast_caption", ""),
                    parse_mode=ParseMode.MARKDOWN
                )
            elif broadcast_type == "forward":
                forward_data = context.user_data["broadcast_forward"]
                await context.bot.forward_message(
                    chat_id=user.user_id,
                    from_chat_id=forward_data["chat_id"],
                    message_id=forward_data["message_id"]
                )
            
            sent_count += 1
            
        except Exception as e:
            logger.error(f"Xabar yuborishda xatolik (user_id: {user.user_id}): {e}")
            failed_count += 1
    
    # Natijani saqlash
    content = context.user_data.get("broadcast_content", "") or context.user_data.get("broadcast_caption", "")
    db.save_broadcast(ADMIN_CHAT_ID, broadcast_type, content, sent_count)
    
    # Natijani ko'rsatish
    result_text = f"""✅ **Xabar yuborish yakunlandi**

📊 **Natija:**
✅ Muvaffaqiyatli yuborildi: {sent_count} ta
❌ Xatolik bilan: {failed_count} ta
👥 Jami foydalanuvchilar: {len(users)} ta

**Xabar turi:** {broadcast_type}"""
    
    await query.edit_message_text(
        result_text,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("⬅️ Admin panel", callback_data="admin|panel")
        ]]),
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Context ni tozalash
    context.user_data.pop("broadcast_type", None)
    context.user_data.pop("broadcast_content", None)
    context.user_data.pop("broadcast_photo", None)
    context.user_data.pop("broadcast_video", None)
    context.user_data.pop("broadcast_document", None)
    context.user_data.pop("broadcast_forward", None)
    context.user_data.pop("broadcast_caption", None)

# Hisobot yaratish funksiyalari
async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE, report_type: str):
    """Hisobot yaratish"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text("📊 Hisobot yaratilmoqda...")
    
    # Vaqt oralig'ini aniqlash
    now = datetime.now()
    if report_type == "daily":
        start_date = now.strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")
        title = f"Kunlik hisobot - {now.strftime('%d.%m.%Y')}"
    elif report_type == "weekly":
        start_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")
        title = f"Haftalik hisobot - {start_date} dan {end_date} gacha"
    elif report_type == "monthly":
        start_date = now.replace(day=1).strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")
        title = f"Oylik hisobot - {now.strftime('%B %Y')}"
    else:  # full
        start_date = "2020-01-01"
        end_date = now.strftime("%Y-%m-%d")
        title = f"To'liq hisobot - {start_date} dan {end_date} gacha"
    
    # Buyurtmalarni olish
    orders = db.get_orders_by_date_range(start_date, end_date)
    
    if not orders:
        await query.edit_message_text(
            f"📊 **{title}**\n\n❌ Bu vaqt oralig'ida buyurtmalar topilmadi.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Orqaga", callback_data="admin|reports")
            ]]),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Excel fayl yaratish
    report_data = []
    total_amount = 0
    
    for order in orders:
        user = db.get_user(order.user_id)
        items = db.get_order_items(order.order_id)
        
        # Xizmatlar ro'yxati
        services = ", ".join([item.service_name for item in items])
        
        report_data.append({
            "Buyurtma ID": order.order_id,
            "Foydalanuvchi ID": order.user_id,
            "Ism": user.full_name if user else "Noma'lum",
            "Username": f"@{user.username}" if user and user.username else "Noma'lum",
            "Telefon": user.phone if user else "Noma'lum",
            "Brend": order.brand,
            "Model": order.model,
            "Kuzov turi": order.body_type,
            "Xizmatlar": services,
            "Umumiy narx": order.total_amount,
            "Holat": order.status,
            "Buyurtma vaqti": order.created_at,
            "Tasdiqlangan vaqt": order.updated_at if order.status != "pending" else "Tasdiqlanmagan"
        })
        
        total_amount += order.total_amount
    
    # Excel fayl yaratish
    df = pd.DataFrame(report_data)
    
    # Fayl nomi
    filename = f"report_{report_type}_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join("reports", filename)
    
    # Reports papkasini yaratish
    os.makedirs("reports", exist_ok=True)
    
    # Excel fayl yaratish
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Hisobot', index=False)
        
        # Qo'shimcha statistikalar
        stats_data = {
            "Ko'rsatkich": [
                "Jami buyurtmalar",
                "Jami summa",
                "Tasdiqlangan buyurtmalar",
                "Kutilayotgan buyurtmalar",
                "Bekor qilingan buyurtmalar",
                "O'rtacha buyurtma summasi"
            ],
            "Qiymat": [
                len(orders),
                f"{total_amount:,} so'm",
                len([o for o in orders if o.status == "confirmed"]),
                len([o for o in orders if o.status == "pending"]),
                len([o for o in orders if o.status == "cancelled"]),
                f"{total_amount // len(orders):,} so'm" if orders else "0 so'm"
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        stats_df.to_excel(writer, sheet_name='Statistika', index=False)
    
    # Faylni yuborish
    with open(filepath, 'rb') as file:
        await context.bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=InputFile(file, filename=filename),
            caption=f"📊 **{title}**\n\n📋 Jami buyurtmalar: {len(orders)}\n💰 Jami summa: {format_price(total_amount)}"
        )
    
    # Faylni o'chirish
    os.remove(filepath)
    
    await query.edit_message_text(
        f"✅ **{title}**\n\n📊 Hisobot yaratildi va yuborildi!\n\n📋 Jami buyurtmalar: {len(orders)}\n💰 Jami summa: {format_price(total_amount)}",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("⬅️ Orqaga", callback_data="admin|reports")
        ]]),
        parse_mode=ParseMode.MARKDOWN
    )

