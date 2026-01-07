import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from deep_translator import GoogleTranslator

# --- KONFIGURASI DOWNLOAD FONT ---
def download_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/orbitron/static/Orbitron-Bold.ttf"
    font_path = "font_futuristic.ttf"
    if not os.path.exists(font_path):
        try:
            r = requests.get(font_url)
            with open(font_path, 'wb') as f:
                f.write(r.content)
        except:
            return None # Fallback ke default jika gagal
    return font_path

# --- AMBIL QUOTE & TERJEMAHAN ---
def get_quote_indo():
    try:
        # Ambil dari API
        res = requests.get("https://zenquotes.io/api/random", timeout=10).json()
        en_quote = res[0]['q']
        author = res[0]['a']
        # Terjemahkan
        id_quote = GoogleTranslator(source='en', target='id').translate(en_quote)
        return id_quote, author
    except:
        return "Perjuangan hari ini adalah kekuatan untuk hari esok.", "Anonim"

# --- GENERATOR GAMBAR NEON FUTURISTIK ---
def create_neon_image(text, author, output):
    w, h = 1080, 1080
    # Background gelap total
    img = Image.new('RGB', (w, h), color=(5, 5, 10))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Warna Neon Acak
    colors = [(0, 255, 255, 180), (255, 0, 255, 180), (50, 255, 50, 180), (255, 255, 0, 180)]
    main_color = random.choice(colors)
    font_color = random.choice([(255, 255, 255), (0, 255, 255), (255, 255, 0)])

    # Gambar Partikel & Garis Neon Acak
    for _ in range(60):
        x1, y1 = random.randint(0, w), random.randint(0, h)
        x2, y2 = random.randint(0, w), random.randint(0, h)
        draw.line([x1, y1, x2, y2], fill=(main_color[0], main_color[1], main_color[2], 40), width=random.randint(1, 2))
        draw.ellipse([x1, y1, x1+5, y1+5], fill=random.choice(colors))

    # Efek Glow (Blur)
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Font Setup
    f_path = download_font()
    if f_path:
        font_main = ImageFont.truetype(f_path, 65)
        font_auth = ImageFont.truetype(f_path, 40)
    else:
        font_main = ImageFont.load_default()
        font_auth = ImageFont.load_default()

    # Wrap Text agar ke tengah
    words = text.split()
    lines = []
    curr_line = ""
    for word in words:
        if font_main.getlength(curr_line + word) < 800:
            curr_line += word + " "
        else:
            lines.append(curr_line.strip())
            curr_line = word + " "
    lines.append(curr_line.strip())

    # Tentukan posisi Y (Vertical Center)
    total_h = len(lines) * 90
    current_y = (h - total_h) // 2

    # Gambar Teks (Center Horizontal)
    for line in lines:
        line_w = font_main.getlength(line)
        current_x = (w - line_w) // 2
        # Shadow/Glow Text
        draw.text((current_x+4, current_y+4), line, fill=(0,0,0,150), font=font_main)
        draw.text((current_x, current_y), line, fill=font_color, font=font_main)
        current_y += 90

    # Gambar Author
    auth_txt = f"— {author}"
    auth_x = (w - font_auth.getlength(auth_txt)) // 2
    draw.text((auth_x, current_y + 40), auth_txt, fill=(180, 180, 180), font=font_auth)

    img.save(output)

# --- KIRIM KE TELEGRAM ---
def send_telegram(path):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        with open(path, 'rb') as f:
            requests.post(url, data={'chat_id': chat_id}, files={'photo': f})

if __name__ == "__main__":
    quote, author = get_quote_indo()
    file_name = "post.png"
    create_neon_image(quote, author, file_name)
    send_telegram(file_name)
    print("Bot Berhasil Berjalan!")
