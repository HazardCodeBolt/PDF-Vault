import os
import nltk
import time
import math
import pdf2image
# from io import BytesIO
from PyPDF2 import PdfReader
nltk.download('punkt')

class PdfDocManip:

    def __init__(self, pdf_path) :
        self.pdf_path = pdf_path
        self.file_size_kb = math.ceil(os.path.getsize(pdf_path) / 1024)
        with open(pdf_path, 'rb') as f:
            self.pdf = PdfReader(f)
            self.number_of_pages = len(self.pdf.pages)
            self.file_name = self.pdf.metadata.title
            self.text_content = ''
            for i in range(self.number_of_pages):
                page = self.pdf.pages[i]
                self.text_content += page.extract_text()

            

    def get_sentences(self):
        return nltk.tokenize.sent_tokenize(self.text_content)
        

    def get_info(self,):
        info = {
            'file_name': self.file_name,
            'number_of_pages' : self.number_of_pages, 
            'file_size': self.file_size_kb,
        }
        return info



    def get_page_as_image(self,page_num):
        pages = pdf2image.convert_from_path(
            self.pdf_path,
            first_page=page_num, 
            last_page=page_num,
            poppler_path=r'./poppler-0.68.0/bin'
            )
        time_now = time.strftime("%Y%m%d-%H%M%S")
        pages[0].save(fr'./images/{time_now}.jpg', 'JPEG')
            

    def get_words_count(self,):
        words = nltk.word_tokenize(self.text_content)
        word_count = nltk.FreqDist(words)

        freq_dict = {}
        for word, count in word_count.items():
            freq_dict[word] = count

        return freq_dict

    def upload_pdf():
        pass


