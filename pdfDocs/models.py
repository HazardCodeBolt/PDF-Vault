from django.db import models
from .pdf_manip import PdfDocManip
from django.contrib.auth.models import User

class FileUpload(models.Model):
    file            = models.FileField(upload_to='pdfs/')
    user            = models.ForeignKey(User, on_delete=models.CASCADE)

class PdfDocument(models.Model):
    pdfFile_id      = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    fileName        = models.CharField(max_length=120)
    pdfLink         = models.CharField(max_length=250)
    pagesNo         = models.IntegerField()
    fileSizeKB      = models.BigIntegerField()
    uploadDateTime  = models.DateTimeField(auto_now_add=True)



class Sentence(models.Model):
    pdfID           = models.ForeignKey(PdfDocument, on_delete=models.CASCADE)
    sentenceText    = models.CharField(max_length=1000)



class Word(models.Model):
    pdfID           = models.ForeignKey(PdfDocument, on_delete=models.CASCADE)
    word            = models.CharField(max_length=100)
    repeatTimes     = models.IntegerField()