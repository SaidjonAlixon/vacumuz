# 🚗 Avtomobil Detailing Telegram Bot

Bu bot avtomobil detailing xizmatlari uchun buyurtma berish imkonini beradi.

## ✨ Xususiyatlar

- 🏷️ **Brend tanlash**: CHEVROLET, BYD, HUNDAY, KIA, NISSAN, TOYOTA
- 🚙 **Model tanlash**: Har bir brend uchun ko'plab modellar
- 🚐 **Kuzov turi**: Sedan/Hetchbek/Universal, SUV, Miniven
- 🔧 **Xizmatlar**: 4 ta kategoriyada 30+ xizmat
- 🧺 **Savatcha**: Tanlangan xizmatlarni ko'rish va tahrirlash
- 💰 **Narx hisoblash**: Kuzov turiga qarab avtomatik hisoblash
- 📋 **Buyurtma**: Buyurtma kartasi va admin tasdiqlash
- 👨‍💼 **Admin paneli**: Buyurtmalarni tasdiqlash/bekor qilish

## 🚀 Railway da ishga tushirish

### 1. GitHub ga yuklash
```bash
git init
git add .
git commit -m "Initial commit: Avtomobil Detailing Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/tuniningbot.git
git push -u origin main
```

### 2. Railway da ishga tushirish
1. [Railway.app](https://railway.app) ga boring
2. "New Project" → "Deploy from GitHub repo"
3. GitHub repository ni tanlang
4. Environment variables ni sozlang:
   - `BOT_TOKEN` = your_telegram_bot_token
   - `ADMIN_CHAT_ID` = your_telegram_user_id
5. "Deploy Now" ni bosing

### 3. Environment Variables
Railway da quyidagi o'zgaruvchilarni sozlang:
```
BOT_TOKEN=your_bot_token_here
ADMIN_CHAT_ID=your_telegram_user_id
```

### 4. Muhim eslatma
- Bot **Worker process** sifatida ishlaydi (web emas)
- Healthcheck kerak emas
- Avtomatik restart va monitoring mavjud

## 📱 Foydalanish

### Foydalanuvchi uchun:
1. `/start` buyrug'ini yuboring
2. "🚗 Boshlash" tugmasini bosing
3. Brend → Model → Kuzov → Xizmatlar ketma-ketligida tanlang
4. "🧺 Savatcha" orqali tanlanganlarni ko'ring
5. "✅ Yakunlash" orqali buyurtma bering

### Admin uchun:
- Yangi buyurtmalar avtomatik yuboriladi
- "✅ Tasdiqlash" yoki "❌ Bekor qilish" tugmalari
- Mijozga avtomatik xabar yuboriladi

## 🏗️ Loyiha strukturasi

```
tuniningbot/
├── main.py              # Asosiy bot fayli
├── config.py            # Konfiguratsiya va ma'lumotlar
├── models.py            # Ma'lumotlar strukturasi
├── keyboards.py         # Tugma layoutlari
├── handlers.py          # Xabar boshqaruvchilari
├── utils.py             # Yordamchi funksiyalar
├── requirements.txt     # Kerakli paketlar
├── Procfile            # Railway deployment (worker)
├── railway.json        # Railway sozlamalari
├── runtime.txt         # Python versiyasi
└── README.md           # Ushbu fayl
```

## 🔧 Xizmatlar va narxlar

### Kimyoviy tozalash
- Moyka: 150,000 - 250,000 so'm
- Deteyling ximisctka: 1,500,000 - 2,500,000 so'm
- Ekspress ximisctka: 800,000 - 1,300,000 so'm

### Keramika
- NASIOL ZR53: 3,000,000 - 5,000,000 so'm
- Ceramic PRO H9: 5,000,000 - 7,000,000 so'm
- Antidog' polusfera: 600,000 - 800,000 so'm

### Shovqindan izolyatsiya
- Butun kuzov: 7,000,000 - 11,000,000 so'm
- Eshiklar: 1,500,000 - 4,000,000 so'm
- Tom: 800,000 - 2,000,000 so'm

### Polirovka
- Deteyling polirovka: 1,500,000 - 3,500,000 so'm
- Yangi mashina: 1,000,000 - 2,000,000 so'm
- Tiklovchi: 2,500,000 - 3,500,000 so'm

## 🐛 Xatolarni tuzatish

### Bot ishlamayapti:
1. Railway da environment variables to'g'ri sozlanganini tekshiring
2. Bot token to'g'ri kiritilganini tekshiring
3. Railway logs ni ko'ring
4. **Worker process** sifatida ishlayotganini tekshiring

### Healthcheck xatosi:
- Bu normal holat, bot web server emas
- Bot ishlayotgan bo'lsa, healthcheck xatosi tashvish qilmasin

### Xizmatlar ko'rinmayapti:
1. `config.py` dagi ma'lumotlarni tekshiring
2. Railway da qayta deploy qiling

## 📞 Yordam

Muammolar bo'lsa:
- GitHub Issues oching
- Railway logs ni tekshiring
- Telegram: @your_username

## 📄 Litsenziya

MIT License

---

**Eslatma**: Bu bot Railway platformasida **Worker process** sifatida ishlaydi va 24/7 mavjud. Avtomatik restart va monitoring bilan ta'minlangan. Healthcheck xatosi normal holat, chunki bot web server emas.
