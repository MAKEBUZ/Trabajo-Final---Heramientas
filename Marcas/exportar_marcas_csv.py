import csv
import re
import argparse
import os
import sys


def build_brand_patterns():
    patterns = []
    def p(label, regex):
        patterns.append((label, re.compile(regex, re.IGNORECASE)))

    # Principales
    p("Apple", r"(^|\W)(APPLE|IPHONE|IPAD|IPOD|IMAC|MACBOOK|MAC\s?OS|MACOS)(\W|$)")
    p("Samsung", r"(^|\W)(SAMSUNG|GALAXY)(\W|$)")
    p("Microsoft", r"(^|\W)(MICROSOFT|MSFT|WINDOWS|WIN7|WINXP|VISTA)(\W|$)")
    p("Nvidia", r"(^|\W)(NVIDIA|NVDA|GEFORCE|GTX|RTX)(\W|$)")
    p("Nintendo", r"(^|\W)(NINTENDO|SWITCH|WIIU|WII|3DS|DS)(\W|$)")
    p("Xbox", r"(^|\W)(XBOX|X\-BOX|XBOX360|X360)(\W|$)")

    # Adicionales
    p("PlayStation", r"(^|\W)(PLAYSTATION|PS1|PS2|PS3|PS4|PS5|PSP|VITA)(\W|$)")
    p("Sony", r"(^|\W)(SONY)(\W|$)")
    p("Google", r"(^|\W)(GOOGLE|ANDROID|PIXEL|NEXUS|CHROME|CHROMEOS)(\W|$)")
    p("Amazon", r"(^|\W)(AMAZON|KINDLE|FIRE\s?TV|FIRE\s?STICK|ECHO|ALEXA)(\W|$)")
    p("Intel", r"(^|\W)(INTEL|PENTIUM|CELERON|CORE\s?I[3579])(\W|$)")
    p("AMD", r"(^|\W)(AMD|RADEON|RYZEN|THREADRIPPER)(\W|$)")
    p("Lenovo", r"(^|\W)(LENOVO|THINKPAD|IDEAPAD)(\W|$)")
    p("Dell", r"(^|\W)(DELL|ALIENWARE|XPS|INSPIRON)(\W|$)")
    p("HP", r"(^|\W)(HP|HEWLETT\s?PACKARD|PAVILION|ELITEBOOK|SPECTRE)(\W|$)")
    p("ASUS", r"(^|\W)(ASUS|ROG|ZENBOOK|VIVOBOOK)(\W|$)")
    p("Acer", r"(^|\W)(ACER|PREDATOR|ASPIRE)(\W|$)")
    p("MSI", r"(^|\W)(MSI|STEALTH|TITAN|RAIDER)(\W|$)")
    p("Huawei", r"(^|\W)(HUAWEI|HONOR)(\W|$)")
    p("Xiaomi", r"(^|\W)(XIAOMI|REDMI|POCO)(\W|$)")
    p("OnePlus", r"(^|\W)(ONEPLUS)(\W|$)")
    p("Oppo", r"(^|\W)(OPPO)(\W|$)")
    p("Vivo", r"(^|\W)(VIVO)(\W|$)")
    p("Motorola", r"(^|\W)(MOTOROLA|MOTO\s?G|MOTO\s?E)(\W|$)")
    p("LG", r"(^|\W)(LG)(\W|$)")
    p("HTC", r"(^|\W)(HTC)(\W|$)")
    p("Nokia", r"(^|\W)(NOKIA|LUMIA)(\W|$)")
    p("BlackBerry", r"(^|\W)(BLACKBERRY|BB10|BOLD|CURVE)(\W|$)")
    # Audio / periféricos
    p("Bose", r"(^|\W)(BOSE)(\W|$)")
    p("JBL", r"(^|\W)(JBL)(\W|$)")
    p("Beats", r"(^|\W)(BEATS)(\W|$)")
    p("Sennheiser", r"(^|\W)(SENNHEISER)(\W|$)")
    p("Logitech", r"(^|\W)(LOGITECH)(\W|$)")
    p("Razer", r"(^|\W)(RAZER)(\W|$)")
    p("Corsair", r"(^|\W)(CORSAIR)(\W|$)")
    p("SteelSeries", r"(^|\W)(STEELSERIES)(\W|$)")
    p("HyperX", r"(^|\W)(HYPERX)(\W|$)")
    p("Elgato", r"(^|\W)(ELGATO)(\W|$)")
    p("Turtle Beach", r"(^|\W)(TURTLE\s?BEACH)(\W|$)")
    # Almacenamiento
    p("Seagate", r"(^|\W)(SEAGATE)(\W|$)")
    p("Western Digital", r"(^|\W)(WESTERN\s?DIGITAL|WD)(\W|$)")
    p("SanDisk", r"(^|\W)(SANDISK)(\W|$)")
    p("Kingston", r"(^|\W)(KINGSTON)(\W|$)")
    p("Crucial", r"(^|\W)(CRUCIAL)(\W|$)")
    p("Transcend", r"(^|\W)(TRANSCEND)(\W|$)")
    # Componentes PC / GPU partners
    p("EVGA", r"(^|\W)(EVGA)(\W|$)")
    p("Zotac", r"(^|\W)(ZOTAC)(\W|$)")
    p("Sapphire", r"(^|\W)(SAPPHIRE)(\W|$)")
    p("PowerColor", r"(^|\W)(POWER\s?COLOR)(\W|$)")
    p("Gigabyte", r"(^|\W)(GIGABYTE)(\W|$)")
    p("ASRock", r"(^|\W)(ASROCK)(\W|$)")
    p("XFX", r"(^|\W)(XFX)(\W|$)")
    # Cámaras / drones
    p("Canon", r"(^|\W)(CANON)(\W|$)")
    p("Nikon", r"(^|\W)(NIKON)(\W|$)")
    p("Fujifilm", r"(^|\W)(FUJIFILM|FUJI\s?FILM)(\W|$)")
    p("Olympus", r"(^|\W)(OLYMPUS)(\W|$)")
    p("GoPro", r"(^|\W)(GOPRO)(\W|$)")
    p("DJI", r"(^|\W)(DJI)(\W|$)")
    # Televisores / AV
    p("Philips", r"(^|\W)(PHILIPS)(\W|$)")
    p("Panasonic", r"(^|\W)(PANASONIC)(\W|$)")
    p("Sharp", r"(^|\W)(SHARP)(\W|$)")
    p("TCL", r"(^|\W)(TCL)(\W|$)")
    p("Hisense", r"(^|\W)(HISENSE)(\W|$)")
    p("Vizio", r"(^|\W)(VIZIO)(\W|$)")
    # Streaming / media
    p("Netflix", r"(^|\W)(NETFLIX)(\W|$)")
    p("Disney+", r"(^|\W)(DISNEY\+|DISNEY\s?PLUS)(\W|$)")
    p("Hulu", r"(^|\W)(HULU)(\W|$)")
    p("HBO", r"(^|\W)(HBO|HBO\s?MAX|MAX)(\W|$)")
    p("Prime Video", r"(^|\W)(PRIME\s?VIDEO)(\W|$)")
    p("Paramount+", r"(^|\W)(PARAMOUNT\+)(\W|$)")
    p("Peacock", r"(^|\W)(PEACOCK)(\W|$)")
    p("YouTube", r"(^|\W)(YOUTUBE)(\W|$)")
    p("Spotify", r"(^|\W)(SPOTIFY)(\W|$)")
    p("Apple Music", r"(^|\W)(APPLE\s?MUSIC)(\W|$)")
    p("Amazon Music", r"(^|\W)(AMAZON\s?MUSIC)(\W|$)")
    p("Tidal", r"(^|\W)(TIDAL)(\W|$)")
    p("Deezer", r"(^|\W)(DEEZER)(\W|$)")
    p("Warner Bros", r"(^|\W)(WARNER\s?BROS)(\W|$)")
    p("Universal", r"(^|\W)(UNIVERSAL\s?PICTURES|UNIVERSAL)(\W|$)")
    p("20th Century", r"(^|\W)(20TH\s?CENTURY\s?STUDIOS|20TH\s?CENTURY\s?FOX)(\W|$)")
    p("Sony Pictures", r"(^|\W)(SONY\s?PICTURES)(\W|$)")
    # Social / tech
    p("Facebook", r"(^|\W)(FACEBOOK|FB)(\W|$)")
    p("Instagram", r"(^|\W)(INSTAGRAM|IG)(\W|$)")
    p("WhatsApp", r"(^|\W)(WHATSAPP)(\W|$)")
    p("Messenger", r"(^|\W)(MESSENGER)(\W|$)")
    p("TikTok", r"(^|\W)(TIKTOK)(\W|$)")
    p("Snapchat", r"(^|\W)(SNAPCHAT)(\W|$)")
    p("Twitter", r"(^|\W)(TWITTER)(\W|$)")
    p("Meta", r"(^|\W)(META)(\W|$)")
    # Pagos / fintech
    p("PayPal", r"(^|\W)(PAYPAL)(\W|$)")
    p("Visa", r"(^|\W)(VISA)(\W|$)")
    p("Mastercard", r"(^|\W)(MASTERCARD)(\W|$)")
    p("Stripe", r"(^|\W)(STRIPE)(\W|$)")
    p("Square", r"(^|\W)(SQUARE)(\W|$)")
    p("Apple Pay", r"(^|\W)(APPLE\s?PAY)(\W|$)")
    p("Google Pay", r"(^|\W)(GOOGLE\s?PAY)(\W|$)")
    # Cloud / enterprise
    p("AWS", r"(^|\W)(AWS|AMAZON\s?WEB\s?SERVICES)(\W|$)")
    p("Azure", r"(^|\W)(AZURE)(\W|$)")
    p("Google Cloud", r"(^|\W)(GOOGLE\s?CLOUD|GCP)(\W|$)")
    p("IBM", r"(^|\W)(IBM)(\W|$)")
    p("Oracle", r"(^|\W)(ORACLE)(\W|$)")
    p("Salesforce", r"(^|\W)(SALESFORCE)(\W|$)")
    p("SAP", r"(^|\W)(SAP)(\W|$)")
    p("VMware", r"(^|\W)(VMWARE)(\W|$)")
    p("Docker", r"(^|\W)(DOCKER)(\W|$)")
    p("Kubernetes", r"(^|\W)(KUBERNETES|K8S)(\W|$)")
    # Retail / e-commerce
    p("eBay", r"(^|\W)(EBAY)(\W|$)")
    p("Walmart", r"(^|\W)(WALMART)(\W|$)")
    p("Target", r"(^|\W)(TARGET)(\W|$)")
    p("Best Buy", r"(^|\W)(BEST\s?BUY)(\W|$)")
    p("Costco", r"(^|\W)(COSTCO)(\W|$)")
    p("Ikea", r"(^|\W)(IKEA)(\W|$)")
    p("AliExpress", r"(^|\W)(ALIEXPRESS)(\W|$)")
    p("Shopify", r"(^|\W)(SHOPIFY)(\W|$)")
    # Automotriz
    p("Tesla", r"(^|\W)(TESLA)(\W|$)")
    p("Ford", r"(^|\W)(FORD)(\W|$)")
    p("Toyota", r"(^|\W)(TOYOTA)(\W|$)")
    p("BMW", r"(^|\W)(BMW)(\W|$)")
    p("Mercedes", r"(^|\W)(MERCEDES|MERCEDES\-BENZ)(\W|$)")
    p("Audi", r"(^|\W)(AUDI)(\W|$)")
    p("Volkswagen", r"(^|\W)(VOLKSWAGEN|VW)(\W|$)")
    p("Nissan", r"(^|\W)(NISSAN)(\W|$)")
    p("Honda", r"(^|\W)(HONDA)(\W|$)")
    p("Hyundai", r"(^|\W)(HYUNDAI)(\W|$)")
    p("Kia", r"(^|\W)(KIA)(\W|$)")
    p("Chevrolet", r"(^|\W)(CHEVROLET|CHEVY)(\W|$)")
    p("Porsche", r"(^|\W)(PORSCHE)(\W|$)")
    p("Ferrari", r"(^|\W)(FERRARI)(\W|$)")
    p("Lamborghini", r"(^|\W)(LAMBORGHINI)(\W|$)")
    p("Maserati", r"(^|\W)(MASERATI)(\W|$)")
    p("Bugatti", r"(^|\W)(BUGATTI)(\W|$)")
    p("McLaren", r"(^|\W)(MC\s?LAREN|MCLAREN)(\W|$)")
    p("Bentley", r"(^|\W)(BENTLEY)(\W|$)")
    p("Rolls-Royce", r"(^|\W)(ROLLS\-ROYCE|ROLLS\s?ROYCE)(\W|$)")
    p("Citroen", r"(^|\W)(CITROEN|CITROËN)(\W|$)")
    p("Peugeot", r"(^|\W)(PEUGEOT)(\W|$)")
    p("Renault", r"(^|\W)(RENAULT)(\W|$)")
    p("Alfa Romeo", r"(^|\W)(ALFA\s?ROMEO)(\W|$)")
    p("Skoda", r"(^|\W)(SKODA|ŠKODA)(\W|$)")
    p("Seat", r"(^|\W)(SEAT)(\W|$)")
    p("Fiat", r"(^|\W)(FIAT)(\W|$)")
    p("Subaru", r"(^|\W)(SUBARU)(\W|$)")
    p("Mazda", r"(^|\W)(MAZDA)(\W|$)")
    p("Mini", r"(^|\W)(MINI)(\W|$)")
    p("Land Rover", r"(^|\W)(LAND\s?ROVER)(\W|$)")
    p("Jaguar", r"(^|\W)(JAGUAR)(\W|$)")
    p("Infiniti", r"(^|\W)(INFINITI)(\W|$)")
    p("Lexus", r"(^|\W)(LEXUS)(\W|$)")
    p("Ram", r"(^|\W)(RAM)(\W|$)")
    p("Dodge", r"(^|\W)(DODGE)(\W|$)")
    p("Jeep", r"(^|\W)(JEEP)(\W|$)")
    p("Cadillac", r"(^|\W)(CADILLAC)(\W|$)")
    p("Lincoln", r"(^|\W)(LINCOLN)(\W|$)")
    p("Yamaha", r"(^|\W)(YAMAHA)(\W|$)")
    p("Suzuki", r"(^|\W)(SUZUKI)(\W|$)")
    p("Kawasaki", r"(^|\W)(KAWASAKI)(\W|$)")
    p("Ducati", r"(^|\W)(DUCATI)(\W|$)")
    p("Harley-Davidson", r"(^|\W)(HARLEY\-DAVIDSON)(\W|$)")
    p("KTM", r"(^|\W)(KTM)(\W|$)")
    p("Triumph", r"(^|\W)(TRIUMPH)(\W|$)")
    p("Aprilia", r"(^|\W)(APRILIA)(\W|$)")
    p("Piaggio", r"(^|\W)(PIAGGIO)(\W|$)")
    p("Vespa", r"(^|\W)(VESPA)(\W|$)")
    p("Husqvarna", r"(^|\W)(HUSQVARNA)(\W|$)")
    p("Royal Enfield", r"(^|\W)(ROYAL\s?ENFIELD)(\W|$)")
    p("Benelli", r"(^|\W)(BENELLI)(\W|$)")
    # Ropa / calzado
    p("Nike", r"(^|\W)(NIKE)(\W|$)")
    p("Adidas", r"(^|\W)(ADIDAS)(\W|$)")
    p("Puma", r"(^|\W)(PUMA)(\W|$)")
    p("Under Armour", r"(^|\W)(UNDER\s?ARMOUR)(\W|$)")
    p("Reebok", r"(^|\W)(REEBOK)(\W|$)")
    p("New Balance", r"(^|\W)(NEW\s?BALANCE)(\W|$)")
    p("Zara", r"(^|\W)(ZARA)(\W|$)")
    p("H&M", r"(^|\W)(H\&M)(\W|$)")
    p("Uniqlo", r"(^|\W)(UNIQLO)(\W|$)")
    p("Pull&Bear", r"(^|\W)(PULL\&BEAR)(\W|$)")
    p("Bershka", r"(^|\W)(BERSHKA)(\W|$)")
    p("Stradivarius", r"(^|\W)(STRADIVARIUS)(\W|$)")
    p("Massimo Dutti", r"(^|\W)(MASSIMO\s?DUTTI)(\W|$)")
    p("Shein", r"(^|\W)(SHEIN)(\W|$)")
    p("Levi's", r"(^|\W)(LEVI\'S|LEVIS)(\W|$)")
    p("Converse", r"(^|\W)(CONVERSE)(\W|$)")
    p("Vans", r"(^|\W)(VANS)(\W|$)")
    p("Crocs", r"(^|\W)(CROCS)(\W|$)")
    p("Tommy Hilfiger", r"(^|\W)(TOMMY\s?HILFIGER)(\W|$)")
    p("Ralph Lauren", r"(^|\W)(RALPH\s?LAUREN)(\W|$)")
    p("Gucci", r"(^|\W)(GUCCI)(\W|$)")
    p("Prada", r"(^|\W)(PRADA)(\W|$)")
    p("Balenciaga", r"(^|\W)(BALENCIAGA)(\W|$)")
    p("Louis Vuitton", r"(^|\W)(LOUIS\s?VUITTON)(\W|$)")
    p("Off-White", r"(^|\W)(OFF\-WHITE)(\W|$)")
    p("Moncler", r"(^|\W)(MONCLER)(\W|$)")
    p("Stone Island", r"(^|\W)(STONE\s?ISLAND)(\W|$)")
    p("The North Face", r"(^|\W)(THE\s?NORTH\s?FACE)(\W|$)")
    p("Patagonia", r"(^|\W)(PATAGONIA)(\W|$)")
    p("Columbia", r"(^|\W)(COLUMBIA)(\W|$)")
    p("Lacoste", r"(^|\W)(LACOSTE)(\W|$)")
    p("Chanel", r"(^|\W)(CHANEL)(\W|$)")
    p("Dior", r"(^|\W)(DIOR)(\W|$)")
    p("Yves Saint Laurent", r"(^|\W)(YVES\s?SAINT\s?LAURENT|YSL)(\W|$)")
    p("Paco Rabanne", r"(^|\W)(PACO\s?RABANNE)(\W|$)")
    p("Calvin Klein", r"(^|\W)(CALVIN\s?KLEIN|CK)(\W|$)")
    p("Armani", r"(^|\W)(ARMANI|GIORGIO\s?ARMANI)(\W|$)")
    p("Versace", r"(^|\W)(VERSACE)(\W|$)")
    p("Carolina Herrera", r"(^|\W)(CAROLINA\s?HERRERA)(\W|$)")
    p("Jean Paul Gaultier", r"(^|\W)(JEAN\s?PAUL\s?GAULTIER)(\W|$)")
    p("Tom Ford", r"(^|\W)(TOM\s?FORD)(\W|$)")
    p("Hugo Boss", r"(^|\W)(HUGO\s?BOSS)(\W|$)")
    p("Givenchy", r"(^|\W)(GIVENCHY)(\W|$)")
    p("Burberry", r"(^|\W)(BURBERRY)(\W|$)")
    p("Lancome", r"(^|\W)(LANCOME|LANCÔME)(\W|$)")
    p("Hermes", r"(^|\W)(HERMES|HERMÈS)(\W|$)")
    p("Montblanc", r"(^|\W)(MONTBLANC)(\W|$)")
    p("Victoria's Secret", r"(^|\W)(VICTORIA\'S\s?SECRET|VICTORIAS\s?SECRET)(\W|$)")
    p("LOreal", r"(^|\W)(L\'OREAL|LOREAL)(\W|$)")
    p("Nivea", r"(^|\W)(NIVEA)(\W|$)")
    p("Dove", r"(^|\W)(DOVE)(\W|$)")
    p("Axe", r"(^|\W)(AXE)(\W|$)")
    p("Old Spice", r"(^|\W)(OLD\s?SPICE)(\W|$)")
    # Comida / bebidas / cadenas
    p("McDonald's", r"(^|\W)(MCDONALD\'S|MCDONALDS)(\W|$)")
    p("Burger King", r"(^|\W)(BURGER\s?KING)(\W|$)")
    p("KFC", r"(^|\W)(KFC|KENTUCKY\s?FRIED\s?CHICKEN)(\W|$)")
    p("Subway", r"(^|\W)(SUBWAY)(\W|$)")
    p("Starbucks", r"(^|\W)(STARBUCKS)(\W|$)")
    p("Domino's", r"(^|\W)(DOMINO\'S|DOMINOS)(\W|$)")
    p("Pizza Hut", r"(^|\W)(PIZZA\s?HUT)(\W|$)")
    p("Taco Bell", r"(^|\W)(TACO\s?BELL)(\W|$)")
    p("Coca-Cola", r"(^|\W)(COCA\-COLA|COCACOLA|COKE)(\W|$)")
    p("Pepsi", r"(^|\W)(PEPSI)(\W|$)")
    # Consolas / gaming plataformas
    p("Sega", r"(^|\W)(SEGA)(\W|$)")
    p("Atari", r"(^|\W)(ATARI)(\W|$)")
    p("GameCube", r"(^|\W)(GAMECUBE)(\W|$)")
    p("Game Boy", r"(^|\W)(GAME\s?BOY|GBA)(\W|$)")
    p("Steam", r"(^|\W)(STEAM)(\W|$)")
    p("Epic Games", r"(^|\W)(EPIC\s?GAMES|EPIC\s?STORE)(\W|$)")
    p("EA", r"(^|\W)(ELECTRONIC\s?ARTS|EA\s?GAMES)(\W|$)")
    p("Ubisoft", r"(^|\W)(UBISOFT)(\W|$)")
    p("Rockstar", r"(^|\W)(ROCKSTAR\s?GAMES)(\W|$)")
    p("Bethesda", r"(^|\W)(BETHESDA)(\W|$)")
    p("PSN", r"(^|\W)(PSN|PLAYSTATION\s?NETWORK)(\W|$)")
    # Operadores móviles
    p("Verizon", r"(^|\W)(VERIZON)(\W|$)")
    p("AT&T", r"(^|\W)(AT\&T|ATT)(\W|$)")
    p("T-Mobile", r"(^|\W)(T\-?MOBILE)(\W|$)")
    p("Sprint", r"(^|\W)(SPRINT)(\W|$)")
    p("Vodafone", r"(^|\W)(VODAFONE)(\W|$)")
    p("Orange", r"(^|\W)(ORANGE)(\W|$)")
    p("Movistar", r"(^|\W)(MOVISTAR)(\W|$)")
    p("Claro", r"(^|\W)(CLARO)(\W|$)")
    p("Telcel", r"(^|\W)(TELCEL)(\W|$)")
    # Sistemas operativos
    p("Ubuntu", r"(^|\W)(UBUNTU)(\W|$)")
    p("Debian", r"(^|\W)(DEBIAN)(\W|$)")
    p("Fedora", r"(^|\W)(FEDORA)(\W|$)")
    p("Red Hat", r"(^|\W)(RED\s?HAT)(\W|$)")
    p("CentOS", r"(^|\W)(CENTOS)(\W|$)")
    return patterns


def classify_brand(text, patterns):
    if not text:
        return "sin marca"
    for label, rx in patterns:
        if rx.search(text):
            return label
    return "sin marca"


def detect_header_and_indices(header_row):
    # Normaliza y detecta columnas
    lowered = [c.strip().lower() for c in header_row]
    user_idx = None
    text_idx = None
    ids_idx = None

    try:
        user_idx = lowered.index("user")
    except ValueError:
        pass
    try:
        text_idx = lowered.index("text")
    except ValueError:
        pass
    try:
        ids_idx = lowered.index("ids")
    except ValueError:
        # algunos encabezados usan 'id'
        try:
            ids_idx = lowered.index("id")
        except ValueError:
            pass

    header_detected = (user_idx is not None and text_idx is not None)
    if header_detected:
        if ids_idx is None:
            ids_idx = 1  # fallback razonable
        return True, ids_idx, user_idx, text_idx
    else:
        # Asume formato Sentiment140: target, ids, date, flag, user, text
        return False, 1, 4, 5


def process_csv(path, output, preserve_all_columns=False, inplace=False):
    patterns = build_brand_patterns()
    total = 0
    written = 0
    header_detected = False
    ids_idx = 1
    user_idx = 4
    text_idx = 5

    if not os.path.exists(path):
        print(f"ERROR: no existe el archivo de entrada: {path}", file=sys.stderr)
        sys.exit(1)

    # Asegura directorio de salida
    out_dir = os.path.dirname(output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # Si vamos a preservar todas las columnas y modificar in-place, usamos la misma codificación del archivo fuente
    out_encoding = "ISO-8859-1" if preserve_all_columns else "UTF-8"

    tmp_output = output
    if inplace:
        base_dir = os.path.dirname(path)
        base_name = os.path.basename(path)
        tmp_output = os.path.join(base_dir, f".{base_name}.tmp")

    with open(path, "r", encoding="ISO-8859-1", newline="") as fin, \
         open(tmp_output, "w", encoding=out_encoding, newline="") as fout:
        reader = csv.reader(fin, delimiter=",", quotechar='"')
        writer = csv.writer(fout, delimiter=",", quotechar='"')

        first = True
        # header de salida
        if not preserve_all_columns:
            writer.writerow(["ids", "user", "text", "Marca"])

        for row in reader:
            total += 1
            if first:
                first = False
                header_detected, ids_idx, user_idx, text_idx = detect_header_and_indices(row)
                if header_detected:
                    # escribir encabezado preservado + Marca si se preservan todas las columnas
                    if preserve_all_columns:
                        writer.writerow(row + ["Marca"])
                        continue
                    # si no preservamos todo, no escribir la fila de encabezado de entrada como dato
                    continue

            if len(row) <= max(ids_idx, user_idx, text_idx):
                continue
            text = row[text_idx]
            marca = classify_brand(text, patterns)
            if preserve_all_columns:
                writer.writerow(row + [marca])
            else:
                ids = row[ids_idx]
                user = row[user_idx]
                writer.writerow([ids, user, text, marca])
            written += 1

            if written % 100000 == 0:
                print(f"Progreso: {written} filas escritas...")

    print(f"Terminado. Filas leídas: {total}, filas escritas: {written}")
    print(f"Salida: {tmp_output}")

    # Reemplazo in-place si se especifica
    if inplace:
        try:
            os.replace(tmp_output, path)
            print(f"Archivo original reemplazado: {path}")
        except Exception as e:
            print(f"No se pudo reemplazar el archivo original: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Exportar columnas y agregar Marca desde CSV (sin Spark)")
    parser.add_argument("--path", type=str, required=True, help="Ruta del CSV de entrada")
    parser.add_argument("--output", type=str, default="usuarios_texto_marca.csv", help="Ruta del CSV de salida")
    parser.add_argument("--inplace", action="store_true", default=False, help="Modificar el archivo de entrada in-place")
    parser.add_argument("--preserve_all_columns", action="store_true", default=False, help="Preservar todas las columnas y agregar 'Marca' al final")
    return parser.parse_args()


def main():
    args = parse_args()
    process_csv(args.path, args.output, preserve_all_columns=args.preserve_all_columns, inplace=args.inplace)


if __name__ == "__main__":
    main()
