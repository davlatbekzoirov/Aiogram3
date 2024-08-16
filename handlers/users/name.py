from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cv2, random
import numpy as np

def get_average_color(image):
    """Rasmning o'rtacha rangini hisoblang."""
    img_np = np.array(image) # ? Birinchi ikkita o'lcham piksel o'rnini (tasvirning balandligi va kengligi) ifodalaydi.
    # ! funktsiya birinchi ikkita o'q (balandlik va kenglik) bo'yicha piksel qiymatlarining o'rtacha (o'rtacha) qiymatini hisoblaydi. Bu, asosan, butun tasvir bo'ylab har bir rang kanali uchun barcha piksel qiymatlarini o'rtacha qiladi.
    avg_color = img_np.mean(axis=(0, 1))
    # ! O'rtacha rang qiymatlari float raqamlardir, shuning uchun ular yordamida butun sonlarga aylantiriladi
    return tuple(map(int, avg_color))

def create_multicolor_gradient_background(width, height, colors):
    """Bir nechta ranglar bilan vertikal gradient fon yarating."""
    gradient = Image.new('RGB', (width, height)) # ? berilgan o'lchamlarda bo'sh (qora) tasvir yaratiladi.
    draw = ImageDraw.Draw(gradient) # ? tasvirda chizish uchun obyekt yaratadi
    
    num_colors = len(colors) # ? ro'yxatidagi ranglar soni
    segment_height = height / (num_colors - 1) # ? bu har bir rang segmentining balandligi. Bu gradientning har bir qismida qaysi ranglar o'zgarishi kerakligini aniqlash uchun kerak.
    
    for i in range(num_colors - 1):
        # ! sikl yordamida ranglar oralig'ida vertikal chiziqlar chiziladi
        start_color = colors[i] # ? gradientning qaysi ikki rang o'rtasida o'zgarishini belgilaydi
        end_color = colors[i + 1] # ? gradientning qaysi ikki rang o'rtasida o'zgarishini belgilaydi 
        start_y = int(i * segment_height)# ? segmentning vertikal boshlanishi va tugash nuqtalari 
        end_y = int((i + 1) * segment_height)# ? segmentning vertikal boshlanishi va tugash nuqtalari
        
        for y in range(start_y, end_y):
            # * har bir chiziqning (y) koordinatasida joylashgan rangning RGB qiymatlarini hisoblab chiqadi. Bu ranglar segmentning boshlang'ich va tugash ranglari orasida o'zgaradi
            r = int(start_color[0] * (1 - (y - start_y) / segment_height) + end_color[0] * ((y - start_y) / segment_height))
            g = int(start_color[1] * (1 - (y - start_y) / segment_height) + end_color[1] * ((y - start_y) / segment_height))
            b = int(start_color[2] * (1 - (y - start_y) / segment_height) + end_color[2] * ((y - start_y) / segment_height))
            # ! gradientning har bir qatori uchun kerakli rang bilan chiziq chizadi.
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # ! yaratilgan gradient foni-ni qaytaradi
    return gradient

async def generate_image_with_text(photo_file: BytesIO, name: str) -> BytesIO:
    """Asosiy f-sia rasmni chizadi"""

    # ! Rasmni yuklash va RGB formatiga o'tkazish
    user_photo = Image.open(photo_file).convert('RGB')
    # * photo_file dan rasm yuklanadi va RGB formatiga aylantiriladi
    

    # ! Rasm o'lchamini olish va kvadrat qutiga kesish:
    width, height = user_photo.size
    min_dimension = min(width, height)
    left = (width - min_dimension) // 2
    top = (height - min_dimension) // 2
    right = (width + min_dimension) // 2
    bottom = (height + min_dimension) // 2
    user_photo = user_photo.crop((left, top, right, bottom))
    # * Rasmning eng kichik o'lchami (kenglik yoki balandlik) aniqlanadi va rasmni shu o'lchamda kvadrat qilib kesib olinadi.


    # ! Rasmni kerakli o'lchamga o'zgartirish:
    user_photo = user_photo.resize((min_dimension, min_dimension), Image.Resampling.LANCZOS)
    photo_width, photo_height = user_photo.size
    # * Rasm kvadrat shaklga keltirilgandan so'ng, u kerakli o'lchamga (min_dimension x min_dimension) o'zgartiriladi
    

    # ! Rasmni NumPy massiviga aylantirish va grayscale formatga o'tkazish
    img_np = np.array(user_photo)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    # * PIL formatidagi rasm NumPy massiviga o'tkaziladi va keyin u grayscale (oq-qora) formatga aylantiriladi
    
    
    # ! Blurring va chetlarni aniqlash
    gray_blur = cv2.medianBlur(gray, 3)
    edges = cv2.adaptiveThreshold(gray_blur, 255, 
                                  cv2.ADAPTIVE_THRESH_MEAN_C, 
                                  cv2.THRESH_BINARY, blockSize=5, C=10)
    # * Grayscale rasmga median blur qo'llanadi va chetlar aniqlash texnikasi bilan chetlar (edges) topiladi.


    # ! Bilaterial filtr va karton effekt yaratish
    color = cv2.bilateralFilter(img_np, d=5, sigmaColor=50, sigmaSpace=50)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    # * Bilaterial filtr yordamida tasvirning ranglari yumshatiladi va chetlar (edges) bilan birlashtiriladi, bu esa rasmga karton (cartoon) effekt beradi
    
    
    # ! Karton rasmni PIL formatiga qaytarish va aylana shaklga keltirish
    cartoon_img = Image.fromarray(cartoon)

    # ? Dumaloq niqob yarating
    mask = Image.new('L', (photo_width, photo_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, photo_width, photo_height), fill=255)

    # ? Dumaloq niqobni multfilm tasviriga qo'llang
    circular_img = Image.new('RGBA', (photo_width, photo_height))
    circular_img.paste(cartoon_img, (0, 0), mask=mask)
    # * Karton effektli rasmni PIL formatiga qaytariladi va aylana shaklidagi maska yordamida rasm aylana shaklida kesiladi.


    # !Fon ranglarini aniqlash va gradient fon yaratish
    average_color = get_average_color(user_photo)
    
    # ? Gradient uchun bir nechta ranglarni aniqlang
    gradient_colors = [(255, 255, 255), (240, 240, 240), (220, 220, 220), 
                       (200, 200, 200), average_color]
                       
    # ? Ko'p rangli gradient fon yarating
    gradient_height = photo_height + 200  # ? Zarur bo'lganda gradient balandligini oshiring
    gradient_background = create_multicolor_gradient_background(photo_width, gradient_height, gradient_colors)
    # * Rasmning o'rtacha rangini aniqlash va ushbu rang bilan bir nechta ranglar yordamida vertikal gradient fon yaratish.
    
    
    # ! Matnning o'lchamini aniqlash va mos fontni tanlash
    font_size = 80 if len(name) <= 10 else 70 if len(name) <= 20 else 60
    try:
        font = ImageFont.truetype("GreyQo-Regular.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    # * Matnning uzunligiga qarab mos font o'lchami tanlanadi va font yuklanadi


    # ? Matn hajmini o'lchash
    temp_image = Image.new('RGBA', (1, 1))
    draw = ImageDraw.Draw(temp_image)
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # ! Yangi rasm yaratish va matnni joylashtirish
    total_height = photo_height + text_height + 70  # ? Kattaroq matn uchun qo'shimcha joy
    output_image = Image.new('RGBA', (photo_width, total_height))
    output_image.paste(gradient_background, (0, 0))

    # ? Dumaloq tasvirni yangi rasmga yopishtiring
    output_image.paste(circular_img, (0, 0), mask=mask)

    # ? Dumaloq tasvir ostidagi rasmga matn chizing
    draw = ImageDraw.Draw(output_image)
    text_x = (photo_width - text_width) / 2
    text_y = photo_height + 20  # ? Matnni rasm ostiga qo'ying, to'ldirishni sozlang
    draw.text((text_x, text_y), name, font=font, fill='black')
    # * Yangi rasm yaratilib, unda fon, aylana rasm va matn joylashtiriladi
    
    
    # ! Rasmni BytesIO obyektiga saqlash va qaytarish
    output_image_bytes = BytesIO()
    output_image.save(output_image_bytes, format='PNG')
    output_image_bytes.seek(0)

    return output_image_bytes.read()
    # * Oxirgi rasm BytesIO obyektiga PNG formatida saqlanadi va foydalanuvchiga qaytariladi
