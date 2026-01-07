import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from deep_translator import GoogleTranslator

# 1. DOWNLOAD FONT OTOMATIS (Agar Anti Gagal & Futuristik)
def download_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/orbitron/static/Orbitron-Bold.ttf"
    font_path = "font_futuristic.ttf"
    if not os.path.exists(font_path):
        print("Sedang mengunduh font futuristik...")
        r = requests.get(font_url)
        with open(font_path, 'wb') as f:
            f.write(r.content)
    return font_path

def get_random_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data[0]['q'], data[0]['a']
    except:
        pass
    return "The path to success is to take massive, determined action.", "Tony Robbins"

def translate_to_id(text):
    try:
        return GoogleTranslator(source='en', target='id').translate(text)
    except:
        return text

def generate_neon_abstract(output_path, quote_text, author):
    # Dimensi High Definition
    w, h = 1080, 1080
    # Background Gelap Deep Space
    img = Image.new('RGB', (w, h), color=(5, 5, 15))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Warna-warna Neon Cyberpunk
    neon_colors = [
        (255, 0, 255, 150),  # Magenta
        (0, 255, 255, 150),  # Cyan
        (50, 255, 50, 150),  # Neon Green
        (255, 255, 0, 150),  # Yellow Neon
        (255, 50, 50, 150)   # Red Neon
    ]

    # Layer 1: Partikel Debu Neon (Background)
    for _ in range(200):
        x, y = random.randint(0, w), random.randint(0, h)
        size = random.randint(1, 3)
        draw.ellipse([x, y, x+size, y+size], fill=random.choice(neon_colors))

    # Layer 2: Garis Futuristik / Grid acak
    for _ in range(15):
        color = random.choice(neon_colors)
        x1 = random.randint(0, w)
        draw.line([x1, 0, x1, h], fill=(color[0], color[1], color[2], 30), width=1)
        y1 = random.randint(0, h)
        draw.line([0, y1, w, y1], fill=(color[0], color[1], color[2], 30), width=1)

    # Layer 3: Neon Streaks (Garis cahaya menyala)
    for _ in range(10):
        color = random.choice(neon_colors)
        x_start = random.randint(0, w)
        y_start = random.randint(0, h)
        length = random.randint(100, 500)
        # Efek Glow (Garis tebal transparan + garis tipis terang)
        draw.line([x_start, y_start, x_start+length, y_start+length], fill=(color[0], color[1], color[2], 50), width=15)
        draw.line([x_start, y_start, x_start+length, y_start+length], fill=(255, 255, 255, 200), width=2)

    # Tambahkan Blur sedikit agar menyatu
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    draw = ImageDraw.Draw(img, 'RGBA')

    # LOAD FONT
    font_file = download_font()
    font_main = ImageFont.truetype(font_file, 55)
    font_auth = ImageFont.truetype(font_file, 35)

    # Wrap Teks (Center Alignment)
    words = quote_text.split()
    lines = []
    line = ""
    for word in words:
        if font_main.getlength(line + word) < 850:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())

    # Hitung posisi Vertical Center
    line_height = 80
    current_y = (h - (len(lines) * line_height)) // 2

    # Warna Font Acak Neon untuk Teks Utama
    text_color = random.choice([(255, 255, 255), (0, 255, 255), (255, 0, 255)])

    for line in lines:
        # Center Horizontal
        w_text = font_main.getlength(line)
        current_x = (w - w_text) // 2
        
        # Glow Effect pada Text
        draw.text((current_x+3, current_y+3), line, fill=(0,0,0,180), font=font_main) # Shadow
        draw.text((current_x, current_y), line, fill=text_color, font=font_main)
        current_y += line_height

    # Nama Author
    auth_txt = f"— {author}"
    auth_x = (w - font_auth.getlength(auth_txt)) // 2
    draw.text((auth_x, current_y + 40), auth_txt, fill=(200, 200, 200), font=font_auth)

    img.save(output_path)

def send_to_telegram(image_path):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not token or not chat_id: return
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(image_path, 'rb') as photo:
        requests.post(url, data={'chat_id': chat_id, 'caption': 'Bot Quote Futuristik ⚡️'}, files={'photo': photo})

if __name__ == "__main__":
    print("Generating Cyberpunk Quote...")
    raw_quote, author = get_random_quote()
    indo_quote = translate_to_id(raw_quote)
    path = "neon_quote.png"
    generate_neon_abstract(path, indo_quote, author)
    send_to_telegram(path)
    print("Success sent to Telegram!")
