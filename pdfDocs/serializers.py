from rest_framework import serializers
from django.contrib.auth.models import User
from pdfDocs.models import PdfDocument, Sentence, Word

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = User
        fields = ['username', 'password']


class PdfDocumentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = PdfDocument
        fields = [
            'user',
            'fileName',
            'pdfLink',
            'pagesNo',
            'fileSizeKB',
            'uploadDateTime',
        ]


class SentenceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Sentence
        fields = [
            'pdfID',   
            'sentenceText',
            'pageNumber',
        ]



class WordSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Word
        fields = [
            'pdfID',
            'word',
            'repeatTimes',
        ]


