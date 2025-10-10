import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Database fayl yo'li
DATABASE_FILE = "bot_database.db"

@dataclass
class User:
    """Foydalanuvchi ma'lumotlari"""
    user_id: int
    username: str = ""
    full_name: str = ""
    phone: str = ""
    created_at: str = ""

@dataclass
class Order:
    """Buyurtma ma'lumotlari"""
    order_id: str
    user_id: int
    brand: str
    model: str
    body_type: str
    total_amount: int
    status: str = "pending"  # pending, confirmed, completed, cancelled
    created_at: str = ""
    updated_at: str = ""

@dataclass
class OrderItem:
    """Buyurtma xizmatlari"""
    id: int = 0
    order_id: str = ""
    service_key: str = ""
    service_name: str = ""
    price: int = 0

class Database:
    """SQLite ma'lumotlar bazasi"""
    
    def __init__(self, db_file: str = DATABASE_FILE):
        self.db_file = db_file
        self.init_database()
    
    def get_connection(self):
        """Database ulanishini olish"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # Dict kabi ishlash uchun
        return conn
    
    def init_database(self):
        """Database jadvallarini yaratish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Foydalanuvchilar jadvali
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        full_name TEXT,
                        phone TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Buyurtmalar jadvali
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id TEXT PRIMARY KEY,
                        user_id INTEGER,
                        brand TEXT NOT NULL,
                        model TEXT NOT NULL,
                        body_type TEXT NOT NULL,
                        total_amount INTEGER NOT NULL,
                        status TEXT DEFAULT 'pending',
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        confirmed_at TEXT,
                        confirmed_by INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                """)
                
                # Buyurtma xizmatlari jadvali
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS order_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id TEXT,
                        service_key TEXT NOT NULL,
                        service_name TEXT NOT NULL,
                        price INTEGER NOT NULL,
                        FOREIGN KEY (order_id) REFERENCES orders (order_id)
                    )
                """)
                
                # Xabar yuborish tarixi jadvali
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS broadcasts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_id INTEGER NOT NULL,
                        message_type TEXT NOT NULL,
                        content TEXT,
                        sent_count INTEGER DEFAULT 0,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Database jadvallari yaratildi")
                
        except Exception as e:
            logger.error(f"Database yaratishda xatolik: {e}")
    
    # Foydalanuvchi operatsiyalari
    def create_or_update_user(self, user: User) -> bool:
        """Foydalanuvchini yaratish yoki yangilash"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Foydalanuvchi mavjudligini tekshirish
                cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user.user_id,))
                exists = cursor.fetchone()
                
                if exists:
                    # Yangilash
                    cursor.execute("""
                        UPDATE users 
                        SET username = ?, full_name = ?, phone = ?
                        WHERE user_id = ?
                    """, (user.username, user.full_name, user.phone, user.user_id))
                else:
                    # Yaratish
                    cursor.execute("""
                        INSERT INTO users (user_id, username, full_name, phone)
                        VALUES (?, ?, ?, ?)
                    """, (user.user_id, user.username, user.full_name, user.phone))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Foydalanuvchi saqlashda xatolik: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Foydalanuvchini olish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return User(
                        user_id=row['user_id'],
                        username=row['username'] or "",
                        full_name=row['full_name'] or "",
                        phone=row['phone'] or "",
                        created_at=row['created_at']
                    )
                return None
                
        except Exception as e:
            logger.error(f"Foydalanuvchini olishda xatolik: {e}")
            return None
    
    # Buyurtma operatsiyalari
    def create_order(self, order: Order, items: List[OrderItem]) -> bool:
        """Buyurtma yaratish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Buyurtma yaratish
                cursor.execute("""
                    INSERT INTO orders (order_id, user_id, brand, model, body_type, total_amount, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (order.order_id, order.user_id, order.brand, order.model, 
                     order.body_type, order.total_amount, order.status))
                
                # Buyurtma xizmatlarini yaratish
                for item in items:
                    cursor.execute("""
                        INSERT INTO order_items (order_id, service_key, service_name, price)
                        VALUES (?, ?, ?, ?)
                    """, (item.order_id, item.service_key, item.service_name, item.price))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Buyurtma yaratishda xatolik: {e}")
            return False
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Buyurtmani olish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
                row = cursor.fetchone()
                
                if row:
                    return Order(
                        order_id=row['order_id'],
                        user_id=row['user_id'],
                        brand=row['brand'],
                        model=row['model'],
                        body_type=row['body_type'],
                        total_amount=row['total_amount'],
                        status=row['status'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                return None
                
        except Exception as e:
            logger.error(f"Buyurtmani olishda xatolik: {e}")
            return None
    
    def get_order_items(self, order_id: str) -> List[OrderItem]:
        """Buyurtma xizmatlarini olish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
                rows = cursor.fetchall()
                
                items = []
                for row in rows:
                    items.append(OrderItem(
                        id=row['id'],
                        order_id=row['order_id'],
                        service_key=row['service_key'],
                        service_name=row['service_name'],
                        price=row['price']
                    ))
                return items
                
        except Exception as e:
            logger.error(f"Buyurtma xizmatlarini olishda xatolik: {e}")
            return []
    
    def update_order_status(self, order_id: str, status: str, admin_id: int = None) -> bool:
        """Buyurtma holatini yangilash"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if status == "confirmed" and admin_id:
                    cursor.execute("""
                        UPDATE orders 
                        SET status = ?, updated_at = CURRENT_TIMESTAMP, 
                            confirmed_at = CURRENT_TIMESTAMP, confirmed_by = ?
                        WHERE order_id = ?
                    """, (status, admin_id, order_id))
                else:
                    cursor.execute("""
                        UPDATE orders 
                        SET status = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE order_id = ?
                    """, (status, order_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Buyurtma holatini yangilashda xatolik: {e}")
            return False
    
    def get_user_orders(self, user_id: int) -> List[Order]:
        """Foydalanuvchi buyurtmalarini olish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM orders 
                    WHERE user_id = ? 
                    ORDER BY created_at DESC
                """, (user_id,))
                rows = cursor.fetchall()
                
                orders = []
                for row in rows:
                    orders.append(Order(
                        order_id=row['order_id'],
                        user_id=row['user_id'],
                        brand=row['brand'],
                        model=row['model'],
                        body_type=row['body_type'],
                        total_amount=row['total_amount'],
                        status=row['status'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    ))
                return orders
                
        except Exception as e:
            logger.error(f"Foydalanuvchi buyurtmalarini olishda xatolik: {e}")
            return []
    
    def get_all_orders(self, status: str = None) -> List[Order]:
        """Barcha buyurtmalarni olish (admin uchun)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if status:
                    cursor.execute("""
                        SELECT * FROM orders 
                        WHERE status = ?
                        ORDER BY created_at DESC
                    """, (status,))
                else:
                    cursor.execute("""
                        SELECT * FROM orders 
                        ORDER BY created_at DESC
                    """)
                
                rows = cursor.fetchall()
                
                orders = []
                for row in rows:
                    orders.append(Order(
                        order_id=row['order_id'],
                        user_id=row['user_id'],
                        brand=row['brand'],
                        model=row['model'],
                        body_type=row['body_type'],
                        total_amount=row['total_amount'],
                        status=row['status'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    ))
                return orders
                
        except Exception as e:
            logger.error(f"Barcha buyurtmalarni olishda xatolik: {e}")
            return []
    
    def get_order_with_items(self, order_id: str) -> Optional[Dict]:
        """Buyurtma va uning xizmatlarini birga olish"""
        order = self.get_order(order_id)
        if not order:
            return None
        
        items = self.get_order_items(order_id)
        return {
            'order': order,
            'items': items
        }
    
    def get_all_users(self) -> List[User]:
        """Barcha foydalanuvchilarni olish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
                rows = cursor.fetchall()
                
                users = []
                for row in rows:
                    users.append(User(
                        user_id=row['user_id'],
                        username=row['username'] or "",
                        full_name=row['full_name'] or "",
                        phone=row['phone'] or "",
                        created_at=row['created_at']
                    ))
                return users
                
        except Exception as e:
            logger.error(f"Barcha foydalanuvchilarni olishda xatolik: {e}")
            return []
    
    def get_orders_by_date_range(self, start_date: str, end_date: str) -> List[Order]:
        """Belgilangan vaqt oralig'idagi buyurtmalarni olish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM orders 
                    WHERE DATE(created_at) BETWEEN ? AND ?
                    ORDER BY created_at DESC
                """, (start_date, end_date))
                rows = cursor.fetchall()
                
                orders = []
                for row in rows:
                    orders.append(Order(
                        order_id=row['order_id'],
                        user_id=row['user_id'],
                        brand=row['brand'],
                        model=row['model'],
                        body_type=row['body_type'],
                        total_amount=row['total_amount'],
                        status=row['status'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    ))
                return orders
                
        except Exception as e:
            logger.error(f"Vaqt oralig'idagi buyurtmalarni olishda xatolik: {e}")
            return []
    
    def save_broadcast(self, admin_id: int, message_type: str, content: str, sent_count: int) -> bool:
        """Xabar yuborish tarixini saqlash"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO broadcasts (admin_id, message_type, content, sent_count)
                    VALUES (?, ?, ?, ?)
                """, (admin_id, message_type, content, sent_count))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Xabar yuborish tarixini saqlashda xatolik: {e}")
            return False

# Global database obyekti
db = Database()
