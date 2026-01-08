from PIL import Image, ImageDraw, ImageFont
import os

# Crear imagen 800x600 con fondo indigo
img = Image.new('RGB', (800, 600), color='#6366f1')
draw = ImageDraw.Draw(img)

# Intentar cargar fuente
try:
    font_title = ImageFont.truetype('arial.ttf', 72)
    font_subtitle = ImageFont.truetype('arial.ttf', 36)
except:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()

# Texto principal
text1 = 'Flyer Informativo'
text2 = 'Agrega tu imagen aquí'
text3 = '(800x600px recomendado)'

# Calcular posiciones
bbox1 = draw.textbbox((0, 0), text1, font=font_title)
width1 = bbox1[2] - bbox1[0]
pos1 = ((800 - width1) // 2, 200)

bbox2 = draw.textbbox((0, 0), text2, font=font_subtitle)
width2 = bbox2[2] - bbox2[0]
pos2 = ((800 - width2) // 2, 320)

bbox3 = draw.textbbox((0, 0), text3, font=font_subtitle)
width3 = bbox3[2] - bbox3[0]
pos3 = ((800 - width3) // 2, 380)

# Dibujar textos
draw.text(pos1, text1, fill='white', font=font_title)
draw.text(pos2, text2, fill='white', font=font_subtitle)
draw.text(pos3, text3, fill='#cbd5e1', font=font_subtitle)

# Dibujar borde decorativo
draw.rectangle([50, 50, 750, 550], outline='white', width=3)

# Guardar
output_path = os.path.join('static', 'uploads', 'popup_dummy.jpg')
img.save(output_path, 'JPEG', quality=95)
print(f'✓ Imagen dummy creada: {output_path}')
