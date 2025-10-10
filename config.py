import os
from dotenv import load_dotenv

load_dotenv()

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")

# Admin chat ID (agar vergul bilan bo'lsa, birinchi ID ni oladi)
admin_ids_str = os.getenv("ADMIN_CHAT_ID", "111111111")
if "," in admin_ids_str:
    ADMIN_CHAT_ID = int(admin_ids_str.split(",")[0].strip())
else:
    ADMIN_CHAT_ID = int(admin_ids_str)

# Brendlar va modellar (kuzov turi bilan)
BRANDS = {
    "CHEVROLET": {
        "COBALT": "sedan", "CORVETTE": "sedan", "CRUZE": "sedan", "GENTRA": "sedan", 
        "EPICA": "sedan", "LACETTI": "sedan", "MALIBU": "sedan", "MALIBU 2": "sedan",
        "NEXIA 1-2": "sedan", "NEXIA 3": "sedan", "SPARK": "sedan", "CAMARO": "sedan",
        "CAVALIER": "sedan", "EQUINOX": "suv", "TRAILBLAZER": "suv", "TRAVERSE": "suv",
        "CAPTIVA": "suv", "TRACKER": "suv", "TAHOE": "suv", "NIVA": "suv",
        "ORLANDO": "minivan"
    },
    "BYD": {
        "HAN": "sedan", "CHAZOR": "sedan", "SEAL": "sedan", "DOLPHIN": "sedan",
        "QIN PLUS": "sedan", "SONG PLUS": "sedan", "YANGWANG U": "sedan",
        "TANG": "suv", "YUAN PLUS": "suv", "SONG PRO": "suv", "YUAN UP": "suv",
        "U9": "minivan"
    },
    "HUNDAY": {
        "ELANTRA": "sedan", "GENESIS": "sedan", "I-20": "sedan", "I-30": "sedan",
        "I-40": "sedan", "SOLARIS": "sedan", "SONATA": "sedan",
        "CRETA": "suv", "SANTA FE": "suv", "TUCSON": "suv", "PALISADE": "suv",
        "STARIA": "minivan"
    },
    "KIA": {
        "OPTIMA": "sedan", "SOUL": "sedan", "SELTOS": "sedan", "STINGER": "sedan",
        "K-5": "sedan", "RIO": "sedan",
        "SORENTO": "suv", "SPORTAGE": "suv", "K-8": "suv", "K-9": "suv",
        "CARNIVAL": "minivan", "EV-3": "minivan", "EV-6": "minivan", "EV-9": "minivan"
    },
    "NISSAN": {
        "ALTIMA": "sedan", "TEANA": "sedan", "TIIDA": "sedan", "QASHKAI": "suv", "PATROL": "suv"
    },
    "TOYOTA": {
        "AVALON": "sedan", "CAMRY": "sedan", "C-HR": "sedan", "YARIS": "sedan",
        "HIGHLANDER": "suv", "HILUX": "suv", "LAND CRUISER": "suv",
        "LAND CRUISER PRADO": "suv", "RAV 4": "suv", "ALPHARD": "minivan"
    },
    "BMW": {
        "3- SER": "sedan", "4- SER": "sedan", "5- SER": "sedan", "7- SER": "sedan", "8- SER": "sedan",
        "X-3": "suv", "X-5": "suv", "X-6": "suv", "X-7": "suv"
    },
    "CHERY": {
        "ARRIZO 6": "sedan", "ARRIZO 8": "sedan",
        "TIGGO 7": "suv", "TIGGO 8": "suv", "TIGGO 9": "suv"
    },
    "INFINITY": {
        "Q40": "sedan", "Q50": "sedan", "Q60": "sedan", "Q70": "sedan",
        "QX": "suv", "FX": "suv", "EX": "suv"
    },
    "LEXUS": {
        "LS": "sedan", "ES": "sedan", "IS": "sedan", "RC": "sedan",
        "RX": "suv", "GX": "suv", "LX": "suv", "HS": "suv"
    },
    "MERCEDES-BENZ": {
        "C": "sedan", "E": "sedan", "S": "sedan", "SL": "sedan", "SLS": "sedan",
        "GLA": "suv", "GLB": "suv", "GLC": "suv", "GLE": "suv", "GLS": "suv"
    },
    "SKODA": {
        "Octavia": "sedan", "Fabia": "sedan",
        "Kodiaq": "suv"
    },
    "TESLA": {
        "Model 3": "sedan",
        "Model X": "suv", "Model Y": "suv", "Cybertruck": "suv"
    },
    "VOLKSWAGEN": {
        "Jetta": "sedan", "Passat": "sedan",
        "ID.4": "suv", "ID.4 Crozz": "suv", "ID.6 Crozz": "suv", "ID.6": "suv"
    },
    "LAND ROVER": {
        "RANGE ROVER BIOGRAPHY": "suv", "RANGE ROVER SPORT": "suv"
    },
    "ZEEKR": {
        "7X": "suv", "MIX": "suv"
    },
    "HAVAL": {
        "Haval H1.": "suv", "Haval H2.": "suv", "Haval H4.": "suv", 
        "Haval H5.": "suv", "Haval H6.": "suv", "Haval H7.": "suv"
    },
    "LEAP MOTO": {
        "B01": "minivan", "B10": "minivan", "C01": "minivan", "C10": "minivan",
        "C11": "minivan", "C16": "minivan", "S01": "minivan", "T03": "minivan"
    }
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

# Brend rasmlari
BRAND_IMAGES = {
    "CHEVROLET": "images/brands/chevrolet.jpg",
    "BYD": "images/brands/byd.png",
    "HUNDAY": "images/brands/HUNDAY.png",
    "KIA": "images/brands/kia.png",
    "NISSAN": "images/brands/NISSAN.jpg",
    "TOYOTA": "images/brands/TOYOTA.jpg",
    "BMW": "images/brands/BMW.jpg",
    "CHERY": "images/brands/CHERY.jpg",
    "INFINITY": "images/brands/INFINITY.jpg",
    "LEXUS": "images/brands/LEXUS.jpg",
    "MERCEDES-BENZ": "images/brands/MERCEDES-BENZ.jpg",
    "SKODA": "images/brands/SKODA.jpg",
    "TESLA": "images/brands/TESLA.jpg",
    "VOLKSWAGEN": "images/brands/VOLKSWAGEN.png",
    "LAND ROVER": "images/brands/LAND-ROVER.jpg",
    "ZEEKR": "images/brands/ZEEKR.jpg",
    "HAVAL": "images/brands/HAVAL.jpg",
    "LEAP MOTO": "images/brands/LEAP-MOTO.png"
}

# Model rasmlari
MODEL_IMAGES = {
    "CHEVROLET": {
        "COBALT": "images/models/cobalt.jpg",
        "CORVETTE": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/2020_Chevrolet_Corvette_Stingray_C8_%281%29.jpg/300px-2020_Chevrolet_Corvette_Stingray_C8_%281%29.jpg",
        "CRUZE": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/2016_Chevrolet_Cruze_LT_sedan_%2814561234567%29.jpg/300px-2016_Chevrolet_Cruze_LT_sedan_%2814561234567%29.jpg",
        "EQUINOX": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/2018_Chevrolet_Equinox_LT_%2814561234567%29.jpg/300px-2018_Chevrolet_Equinox_LT_%2814561234567%29.jpg",
        "TRAILBLAZER": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/2021_Chevrolet_Trailblazer_%2814561234567%29.jpg/300px-2021_Chevrolet_Trailblazer_%2814561234567%29.jpg",
        "ORLANDO": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/2012_Chevrolet_Orlando_%2814561234567%29.jpg/300px-2012_Chevrolet_Orlando_%2814561234567%29.jpg"
    },
    "BYD": {
        "HAN": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/BYD_Han_%2814561234567%29.jpg/300px-BYD_Han_%2814561234567%29.jpg",
        "TANG": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/BYD_Tang_%2814561234567%29.jpg/300px-BYD_Tang_%2814561234567%29.jpg",
        "U9": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/BYD_U9_%2814561234567%29.jpg/300px-BYD_U9_%2814561234567%29.jpg"
    },
    "HUNDAY": {
        "ELANTRA": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/2021_Hyundai_Elantra_%2814561234567%29.jpg/300px-2021_Hyundai_Elantra_%2814561234567%29.jpg",
        "CRETA": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/2020_Hyundai_Creta_%2814561234567%29.jpg/300px-2020_Hyundai_Creta_%2814561234567%29.jpg",
        "STARIA": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/2021_Hyundai_Staria_%2814561234567%29.jpg/300px-2021_Hyundai_Staria_%2814561234567%29.jpg"
    },
    "KIA": {
        "OPTIMA": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/2018_Kia_Optima_%2814561234567%29.jpg/300px-2018_Kia_Optima_%2814561234567%29.jpg",
        "SPORTAGE": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/2022_Kia_Sportage_%2814561234567%29.jpg/300px-2022_Kia_Sportage_%2814561234567%29.jpg",
        "CARNIVAL": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/2021_Kia_Carnival_%2814561234567%29.jpg/300px-2021_Kia_Carnival_%2814561234567%29.jpg"
    },
    "TOYOTA": {
        "CAMRY": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/2021_Toyota_Camry_%2814561234567%29.jpg/300px-2021_Toyota_Camry_%2814561234567%29.jpg",
        "RAV 4": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/2021_Toyota_RAV4_%2814561234567%29.jpg/300px-2021_Toyota_RAV4_%2814561234567%29.jpg",
        "ALPHARD": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/2021_Toyota_Alphard_%2814561234567%29.jpg/300px-2021_Toyota_Alphard_%2814561234567%29.jpg"
    }
}
