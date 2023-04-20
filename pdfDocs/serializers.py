from rest_framework import serializers, mixins
from django.contrib.auth.models import User
from pdfDocs.models import PdfDocument, Sentence, Word
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import FileUpload
from django.conf import settings
from .pdf_manip import PdfDocManip
import os

UserModel = get_user_model()
class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['file']

    def create(self, validated_data):
        file = validated_data['file']
        user = validated_data['user']
        file_upload = FileUpload(file=file, user=user)
        file_upload.save()

        
        # get the direcory where the pdf is saved
        pdf_path = file_upload.file.path 
        # use PdfManip to get info about a pdf
        pdf_manip = PdfDocManip(pdf_path=pdf_path)
        # create a pdfDocument instance
        
        pdf_doc = PdfDocument.objects.create(
            pdfFile_id  = file_upload,
            fileName    = pdf_manip.file_name,
            pdfLink     = file_upload.file.url,
            pagesNo     = pdf_manip.number_of_pages,
            fileSizeKB  = pdf_manip.file_size_kb,
        )
        pdf_doc.save()

        # create senteces 
        pdf_sentences = [
            Sentence(pdfID=pdf_doc, sentenceText=text)
            for text in pdf_manip.get_sentences()
        ]
        Sentence.objects.bulk_create(pdf_sentences)


        # create words of the pdf
        pdf_words = [
            Word(pdfID=pdf_doc, word=word, repeatTimes=rep) 
            for word, rep in pdf_manip.get_words_count().items()
        ]
        Word.objects.bulk_create(pdf_words)


        return file_upload

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta: 
        model = UserModel
        fields = ['id', 'username', 'password']


class PdfDocumentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = PdfDocument
        fields = [
            'id',
            'fileName',
            'pagesNo',
            'fileSizeKB',
            'uploadDateTime',
        ]


class SentenceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Sentence
        fields = [
            'sentenceText',
        ]



class WordSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Word
        fields = [
            'pdfID',
            'word',
            'repeatTimes',
        ]