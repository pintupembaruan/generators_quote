import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from deep_translator import GoogleTranslator

def get_random_quote():
    """Mengambil quote dari API publik dengan sistem cadangan."""
    try:
        # Menggunakan ZenQuotes API (lebih stabil)
        response = requests.get("https://zenquotes.io/api/random", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data[0]['q'], data[0]['a']
    except Exception as e:
        print(f"Gagal ambil API: {e}")
    
    # Cadangan jika internet/API bermasalah
    backup = [
        ("Keep going. Each step is a progress.", "Unknown"),
        ("Life is what happens when you're busy making other plans.", "John Lennon"),
        ("The only way to do great work is to love what you do.", "Steve Jobs")
    ]
    return random.choice(backup)

def translate_to_id(text):
    """Menerjemahkan teks ke Bahasa Indonesia."""
    try:
        translated = GoogleTranslator(source='en', target='id').translate(text)
        return translated
    except:
        return text # Jika gagal, gunakan teks asli

def generate_abstract_image(output_path, quote_text, author):
    # Ukuran Gambar
    w, h = 1000, 1000
    bg_color = (random.randint(0, 30), random.randint(0, 30), random.randint(0, 30))
    img = Image.new('RGB', (w, h), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Seni Abstrak Sederhana
    for _ in range(40):
        color = (random.randint(40, 200), random.randint(40, 200), random.randint(40, 200))
        x1, y1 = random.randint(0, w), random.randint(0, h)
        x2, y2 = random.randint(0, w), random.randint(0, h)
        draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 4))
        draw.rectangle([x1, y1, x1+10, y1+10], outline=color)

    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    draw = ImageDraw.Draw(img)

    # Pengaturan Teks (Bungkus Teks agar tidak keluar gambar)
    margin = 80
    current_h = 400
    words = quote_text.split()
    lines = []
    line = ""
    
    for word in words:
        if len(line + word) < 35:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)
    lines.append(f"\n— {author}")

    # Menulis teks ke gambar
    for l in lines:
        draw.text((margin, current_h), l, fill="white")
        current_h += 40 # Jarak baris

    img.save(output_path)

def send_to_telegram(image_path):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not token or not chat_id:
        return
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(image_path, 'rb') as photo:
        requests.post(url, data={'chat_id': chat_id}, files={'photo': photo}, timeout=20)

if __name__ == "__main__":
    print("Memulai bot...")
    raw_quote, author = get_random_quote()
    print(f"Quote asli: {raw_quote}")
    
    indo_quote = translate_to_id(raw_quote)
    print(f"Terjemahan: {indo_quote}")
    
    path = "result.png"
    generate_abstract_image(path, indo_quote, author)
    send_to_telegram(path)
    print("Selesai!")
