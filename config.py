import os
from dotenv import load_dotenv

load_dotenv()

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")

# Admin chat ID
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "111111111"))

# Brendlar va modellar
BRANDS = {
    "CHEVROLET": [
        "COBALT", "CORVETTE", "CRUZE", "GENTRA", "EPICA", "EQUINOX", "LACETTI", "MALIBU",
        "MALIBU 2", "NIVA", "NEXIA 1-2", "NEXIA 3", "ORLANDO", "SPARK", "TAHOE",
        "TRACKER", "TRAILBLAZER", "TRAVERSE", "CAMARO", "CAPTIVA"
    ],
    "BYD": [
        "HAN", "CHAZOR", "SONG PLUS", "DOLPHIN", "QIN PLUS", "TANG", "YUAN PLUS", "SEAL",
        "SONG PRO", "YUAN UP", "U9", "YANGWANG U"
    ],
    "HUNDAY": [
        "CRETA", "ELANTRA", "GENESIS", "I-20", "I-30", "I-40", "PALISADE", "SANTA FE",
        "SOLARIS", "SONATA", "STARIA", "TUCSON"
    ],
    "KIA": [
        "CARNIVAL", "EV-3", "EV-6", "EV-9", "OPTIMA", "SOUL", "SELTOS", "STINGER",
        "SORENTO", "SPORTAGE", "K-5", "K-8", "K-9"
    ],
    "NISSAN": ["ALTIMA", "QASHKAI", "TEANA", "TIIDA", "PATROL"],
    "TOYOTA": ["AVALON", "ALPHARD", "C-HR", "CAMRY", "HIGHLANDER", "HILUX", "LAND CRUISER",
               "LAND CRUISER PRADO", "YARIS", "RAV 4"],
}

# Kuzov turlari
BODY_TYPES = {
    "sedan": "Sedan/Hetchbek/Universal",
    "suv": "Yo'ltanlamas (SUV)",
    "minivan": "Miniven",
}

# Xizmatlar va narxlar (UZS)
SERVICES = {
    # Kimyoviy tozalash
    "wash": {"name": "Moyka", "group": "Kimyoviy tozalash", "prices": {"sedan": 150_000, "suv": 200_000, "minivan": 250_000}},
    "detailing_chem": {"name": "Deteyling ximisctka", "group": "Kimyoviy tozalash", "prices": {"sedan": 1_500_000, "suv": 2_000_000, "minivan": 2_500_000}},
    "express_chem": {"name": "Ekspress ximisctka", "group": "Kimyoviy tozalash", "prices": {"sedan": 800_000, "suv": 1_000_000, "minivan": 1_300_000}},
    "wheel_arch": {"name": "Deteyling g'ildirak arkalari", "group": "Kimyoviy tozalash", "prices": {"sedan": 400_000, "suv": 600_000, "minivan": 800_000}},
    "engine_bay": {"name": "Deteyling motor bo'limi", "group": "Kimyoviy tozalash", "prices": {"sedan": 500_000, "suv": 600_000, "minivan": 700_000}},
    
    # Keramika
    "nasiozr53": {"name": "NASIOL ZR53", "group": "Keramika", "prices": {"sedan": 3_000_000, "suv": 4_000_000, "minivan": 5_000_000}},
    "nasiolnl272": {"name": "NASIOL NL272", "group": "Keramika", "prices": {"sedan": 4_000_000, "suv": 5_000_000, "minivan": 6_000_000}},
    "hendlexnc9": {"name": "Hendlex NC9 PRO", "group": "Keramika", "prices": {"sedan": 4_000_000, "suv": 5_000_000, "minivan": 6_000_000}},
    "codetgag1": {"name": "CODETHA G1", "group": "Keramika", "prices": {"sedan": 4_500_000, "suv": 5_500_000, "minivan": 6_500_000}},
    "ceramicproh9": {"name": "Ceramic PRO H9", "group": "Keramika", "prices": {"sedan": 5_000_000, "suv": 6_000_000, "minivan": 7_000_000}},
    "antirain": {"name": "Antidog' polusfera", "group": "Keramika", "prices": {"sedan": 600_000, "suv": 700_000, "minivan": 800_000}},
    "ceramic_leather": {"name": "Keramika – salon terisi", "group": "Keramika", "prices": {"sedan": 1_500_000, "suv": 2_000_000, "minivan": 2_500_000}},
    "ceramic_plastic": {"name": "Keramika – salon plastigi", "group": "Keramika", "prices": {"sedan": 1_000_000, "suv": 1_500_000, "minivan": 2_000_000}},
    "ceramic_discs_on": {"name": "Keramika disklar (yechmasdan)", "group": "Keramika", "prices": {"sedan": 1_000_000, "suv": 1_100_000, "minivan": 1_200_000}},
    "ceramic_discs_polish": {"name": "Keramika disklar (+polirovka)", "group": "Keramika", "prices": {"sedan": 1_500_000, "suv": 1_700_000, "minivan": 2_000_000}},
    
    # Shovqindan izolyatsiya
    "full_body_dash_out": {"name": "Butun kuzov + torpedo demontaji", "group": "Shovqindan izolyatsiya", "prices": {"sedan": 8_000_000, "suv": 9_000_000, "minivan": 10_000_000}},
    "full_body_no_dash": {"name": "Butun kuzov (torpedasiz)", "group": "Shovqindan izolyatsiya", "prices": {"sedan": 7_000_000, "suv": 8_000_000, "minivan": 11_000_000}},
    "doors": {"name": "Eshiklar", "group": "Shovqindan izolyatsiya", "prices": {"sedan": 1_500_000, "suv": 2_000_000, "minivan": 4_000_000}},
    "roof": {"name": "Tom", "group": "Shovqindan izolyatsiya", "prices": {"sedan": 800_000, "suv": 1_500_000, "minivan": 2_000_000}},
    "floor": {"name": "Pol", "group": "Shovqindan izolyatsiya", "prices": {"sedan": 1_500_000, "suv": 2_000_000, "minivan": 2_500_000}},
    "trunk": {"name": "Bagajnik", "group": "Shovqindan izolyatsiya", "prices": {"sedan": 650_000, "suv": 750_000, "minivan": 850_000}},
    "hood": {"name": "Kapot", "group": "Shovqindan izolyatsiya", "prices": {"sedan": 300_000, "suv": 400_000, "minivan": 500_000}},
    "wheel_arches_iso": {"name": "G'ildirak arkalari", "group": "Shovqindan izolyatsiya", "prices": {"sedan": 1_500_000, "suv": 2_000_000, "minivan": 2_500_000}},
    
    # Polirovka
    "detailing_polish": {"name": "Deteyling polirovka", "group": "Polirovka", "prices": {"sedan": 1_500_000, "suv": 2_500_000, "minivan": 3_500_000}},
    "new_car_polish": {"name": "Yangi mashina polirovkasi", "group": "Polirovka", "prices": {"sedan": 1_000_000, "suv": 1_500_000, "minivan": 2_000_000}},
    "restoration_polish": {"name": "Tiklovchi polirovka", "group": "Polirovka", "prices": {"sedan": 2_500_000, "suv": 3_000_000, "minivan": 3_500_000}},
}

SERVICE_GROUPS = ["Kimyoviy tozalash", "Keramika", "Shovqindan izolyatsiya", "Polirovka"]
