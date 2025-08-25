from dataclasses import dataclass
from typing import List, Dict, Tuple
from config import SERVICES, BODY_TYPES


@dataclass
class Cart:
    """Foydalanuvchi savatchasi"""
    brand: str = ""
    model: str = ""
    body: str = ""  # 'sedan' | 'suv' | 'minivan'
    items: List[str] = None

    def __post_init__(self):
        if self.items is None:
            self.items = []

    def total(self) -> int:
        """Umumiy summani hisoblash"""
        if not self.body:
            return 0
        return sum(SERVICES[k]["prices"][self.body] for k in self.items)

    def clear(self):
        """Savatchani tozalash"""
        self.brand = ""
        self.model = ""
        self.body = ""
        self.items.clear()

    def add_item(self, service_key: str):
        """Xizmat qo'shish"""
        if service_key not in self.items:
            self.items.append(service_key)

    def remove_item(self, service_key: str):
        """Xizmatni olib tashlash"""
        if service_key in self.items:
            self.items.remove(service_key)

    def toggle_item(self, service_key: str):
        """Xizmatni qo'shish/olib tashlash"""
        if service_key in self.items:
            self.remove_item(service_key)
        else:
            self.add_item(service_key)

    def is_complete(self) -> bool:
        """Buyurtma to'liqmi tekshirish"""
        return bool(self.brand and self.model and self.body and self.items)


def chunk_buttons(options: List[Tuple[str, str]], row: int = 2):
    """Tugmalarni qatorlarga ajratish"""
    buttons = []
    for i in range(0, len(options), row):
        row_buttons = []
        for text, data in options[i:i+row]:
            row_buttons.append((text, data))
        buttons.append(row_buttons)
    return buttons


def format_price(price: int) -> str:
    """Narxni formatlash"""
    return f"{price:,} so'm"


def get_service_info(service_key: str, body_type: str) -> Dict:
    """Xizmat ma'lumotlarini olish"""
    if service_key not in SERVICES:
        return {}
    
    service = SERVICES[service_key].copy()
    service["price"] = service["prices"].get(body_type, 0)
    return service
