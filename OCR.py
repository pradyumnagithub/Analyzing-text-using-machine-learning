import pytesseract as tess
# To download tesseract ocr https://github.com/UB-Mannheim/tesseract/wiki and install it then locate tesseract.exe
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image

# OCR = Optical Character Recognition
class Ocr:
    def imgToText(self, img_path:str):
        img = Image.open(img_path)
        text = tess.image_to_string(img)

        return text


if __name__ == '__main__':
    ocr = Ocr()
    text = ocr.imgToText(r'C:\Users\prady\Desktop\Project\img2.jpg')
    print(text)


#import pytesseract

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path as per your installation
