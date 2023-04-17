from django.contrib import admin
import pdfDocs.models as models
# Register your models here.
admin.site.register(models.PdfDocument)
admin.site.register(models.FileUpload)
admin.site.register(models.Sentence)
admin.site.register(models.Word)