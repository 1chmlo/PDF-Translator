import cv2
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def convert_pdf_to_image(file, start_page, end_page):
    images = convert_from_path(file, first_page=start_page, last_page=end_page)
    return images

def ocr_core(image):
    # Configurado para detectar texto en inglés
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def save_to_pdf(pages, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    c.setFont("Helvetica", 12)
    y = 750  
    for page in pages:
        for line in page:
            if y < 50:
                c.showPage()  
                y = 750  
            c.drawString(100, y, line)
            y -= 15  
        c.showPage()  # Aseguramos que cada página original se convierte en una página en el PDF
        y = 750  # Reiniciamos la posición para la siguiente página
    c.save()

# Solicitar al usuario que introduzca el nombre del archivo PDF a procesar
file_name = input('Por favor, introduce el nombre del archivo PDF escaneado a convertir (debe estar en la misma carpeta que este script): ')
start_page = int(input('Por favor, introduce la página de inicio: '))
end_page = int(input('Por favor, introduce la página de fin: '))

# Asumir que el archivo está en la misma carpeta que el script
file_path = f"./{file_name}"

# Convertir el PDF en imágenes
images = convert_pdf_to_image(file_path, start_page, end_page)

# Extraer el texto por página mediante OCR
recognized_pages = []
for image in images:
    extracted_text = ocr_core(image)
    
    if extracted_text:
        recognized_lines = extracted_text.split('\n')
        recognized_pages.append(recognized_lines)
    else:
        print("No se pudo reconocer texto en la imagen")

# Solicitar al usuario que introduzca el nombre del archivo de salida
output_file = input('Por favor, introduce el nombre del archivo de salida (PDF con texto seleccionable): ')

# Guardar el texto reconocido en un nuevo documento PDF
save_to_pdf(recognized_pages, output_file)

print(f"¡Listo! Se ha creado el archivo {output_file} con el texto reconocido y seleccionable.")