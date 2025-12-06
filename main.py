import logging
import weakref
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from config import BOT_TOKEN
from handlers import start_command, callback_handler, fallback_handler, admin_orders_command, admin_order_detail_command
from admin_panel import admin_panel_command

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Botni ishga tushirish"""
    # Python 3.14 mosligi uchun workaround - weak reference muammosini hal qilish
    # JobQueue.set_application metodini patch qilish
    from telegram.ext import JobQueue
    
    original_set_application = JobQueue.set_application
    
    def patched_set_application(self, application):
        """Weak reference o'rniga to'g'ridan-to'g'ri reference"""
        try:
            self._application = weakref.ref(application)
        except TypeError:
            # Python 3.14 uchun workaround - weak reference o'rniga to'g'ridan-to'g'ri reference
            self._application = lambda: application
    
    JobQueue.set_application = patched_set_application
    
    # Bot yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("admin", admin_panel_command))
    application.add_handler(CommandHandler("orders", admin_orders_command))
    application.add_handler(CommandHandler("order", admin_order_detail_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_handler))
    application.add_handler(MessageHandler(filters.PHOTO, fallback_handler))
    application.add_handler(MessageHandler(filters.VIDEO, fallback_handler))
    application.add_handler(MessageHandler(filters.Document.ALL, fallback_handler))
    
    # Botni ishga tushirish (Python 3.14 uchun event loop yaratish)
    logger.info("Bot ishga tushirilmoqda...")
    try:
        # Python 3.14 uchun yangi event loop yaratish
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        application.run_polling()
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi.")
    finally:
        loop.close()


if __name__ == "__main__":
    main()
