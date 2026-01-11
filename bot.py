import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from deep_translator import GoogleTranslator

# --- AMBIL QUOTE & TERJEMAHAN ---
def get_quote_indo():
    try:
        res = requests.get("https://zenquotes.io/api/random", timeout=10).json()
        en_quote = res[0]['q']
        author = res[0]['a']
        id_quote = GoogleTranslator(source='en', target='id').translate(en_quote)
        return id_quote, author
    except:
        return "Perjuangan hari ini adalah kekuatan untuk hari esok.", "Anonim"

# --- GENERATOR GAMBAR NEON FUTURISTIK ---
def create_neon_image(text, author, output):
    w, h = 1080, 1080
    img = Image.new('RGB', (w, h), color=(5, 5, 15))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Warna Neon
    colors = [(0, 255, 255, 180), (255, 0, 255, 180), (50, 255, 50, 180), (255, 255, 0, 180)]
    main_color = random.choice(colors)
    font_color = random.choice([(255, 255, 255), (0, 255, 255), (255, 255, 0)])

    # Gambar Dekorasi Neon
    for _ in range(80):
        x1, y1 = random.randint(0, w), random.randint(0, h)
        size = random.randint(2, 6)
        draw.ellipse([x1, y1, x1+size, y1+size], fill=random.choice(colors))
        if _ < 15:
            draw.line([random.randint(0,w), 0, random.randint(0,w), h], fill=(main_color[0], main_color[1], main_color[2], 30))

    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    draw = ImageDraw.Draw(img, 'RGBA')

    # LOAD FONT DARI SISTEM UBUNTU (GitHub Actions)
    # Mencari font yang pasti ada setelah di-install di workflow
    possible_fonts = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "Arial.ttf"
    ]
    
    font_main = None
    for path in possible_fonts:
        if os.path.exists(path):
            font_main = ImageFont.truetype(path, 60)
            font_auth = ImageFont.truetype(path, 35)
            break
    
    if not font_main:
        font_main = ImageFont.load_default()
        font_auth = ImageFont.load_default()

    # Wrap Text
    words = text.split()
    lines = []
    curr_line = ""
    for word in words:
        # Cek lebar kata jika menggunakan font truetype
        text_width = font_main.getlength(curr_line + word) if hasattr(font_main, 'getlength') else len(curr_line + word) * 30
        if text_width < 850:
            curr_line += word + " "
        else:
            lines.append(curr_line.strip())
            curr_line = word + " "
    lines.append(curr_line.strip())

    # Posisi Vertikal
    line_spacing = 80
    current_y = (h - (len(lines) * line_spacing)) // 2

    # Gambar Text Center
    for line in lines:
        line_w = font_main.getlength(line) if hasattr(font_main, 'getlength') else len(line) * 30
        current_x = (w - line_w) // 2
        draw.text((current_x+3, current_y+3), line, fill=(0,0,0,200), font=font_main) # Shadow
        draw.text((current_x, current_y), line, fill=font_color, font=font_main)
        current_y += line_spacing

    # Author
    auth_txt = f"— {author}"
    auth_w = font_auth.getlength(auth_txt) if hasattr(font_auth, 'getlength') else len(auth_txt) * 20
    draw.text(((w - auth_w) // 2, current_y + 40), auth_txt, fill=(200, 200, 200), font=font_auth)

    img.save(output)

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
