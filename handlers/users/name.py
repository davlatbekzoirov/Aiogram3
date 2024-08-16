from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps

async def generate_image_with_text(photo_file: BytesIO, name: str) -> BytesIO:
    # * Foydalanuvchining fotosuratini olish
    user_photo = Image.open(photo_file)
    photo_width, photo_height = user_photo.size

    # * Ismning uzunligiga qarab shrift hajmini aniqlash
    font_size = 50 if len(name) <= 10 else 40 if len(name) <= 20 else 30
    try:
        font = ImageFont.truetype("Roboto-Regular.ttf.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # * Matn hajmini o'lchash uchun chizma kontekstini yaratish
    temp_image = Image.new('RGBA', (1, 1))  # ? Matn hajmini o'lchash uchun vaqtinchalik rasm
    draw = ImageDraw.Draw(temp_image)
    
    # * Matn hajmini olish uchun matn qutisidan foydalanish
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # * yangi rasm uchun umumiy balandlikni hisoblash
    total_height = photo_height + text_height + 20
    output_image = Image.new('RGBA', (photo_width, total_height), color='white')

    # * Foydalanuvchining fotosuratini yangi rasmga joylashtirish
    output_image.paste(user_photo, (0, text_height + 10))

    # * Chiqish tasviri uchun chizma kontekstini yaratish
    draw = ImageDraw.Draw(output_image)

    # * Matn o'rnini belgilash
    text_x = (photo_width - text_width) / 2
    text_y = 10

    # * Rasmga matnni yozish
    draw.text((text_x, text_y), name, font=font, fill='black')

    # * Rasmni BytesIO ob'ektiga saqlash
    output_image_bytes = BytesIO()
    output_image.save(output_image_bytes, format='PNG')  # ? Yaxshiroq sifat uchun PNG sifatida saqlash
    output_image_bytes.seek(0)

    return output_image_bytes.read()
