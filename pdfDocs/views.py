from .serializers import (
UserSerializer, PdfDocumentSerializer,
SentenceSerializer, WordSerializer, FileUploadSerializer
)

from rest_framework import generics, permissions, authentication, views, parsers, response, status
from rest_framework import response
from django.contrib.auth import get_user_model
from .models import FileUpload, PdfDocument, Word, Sentence
from django.http import FileResponse
from string import punctuation
from .pdf_manip import PdfDocManip
from django.shortcuts import get_object_or_404, get_list_or_404


class CreateUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer



class FileUploadView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    ]

    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class PdfsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]
    serializer_class = PdfDocumentSerializer
    queryset = PdfDocument.objects.all()



class WordSearchView(generics.ListAPIView):
    # show file id : with the sentences that have that word
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]
    # serializer_class = WordSerializer
    queryset = PdfDocument.objects.all()

    def get(self, request, word, *args, **kwargs):
        
        
        # 1 . get the documents that have the word, collect ids
        docs = [object.pdfID for object in Word.objects.all().filter(word=word)]

        # 2 . get sentences that have the word in, collect sentences
        context_list = []
        for document in docs :
            context = {}
            context['docID'] = document.id
            context['sentences'] = [
                object.sentenceText for object in 
                Sentence.objects.all()
                .filter(pdfID=document, sentenceText__contains=word)
            ]

            context_list.append(context)
        
        return response.Response({ 'word': word,'results': context_list})


class PdfRetreiveView(generics.RetrieveAPIView):
    queryset = FileUpload.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]


    def get(self, request, id,  *args, **kwargs):

        pdfdoc = get_object_or_404(PdfDocument, id=id)
        # pdfdoc = PdfDocument.objects.get(id=id)
        file = pdfdoc.pdfFile_id.file
        name = pdfdoc.fileName

        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment; filename="{name}"'
        response['Content-Type'] = 'application/pdf'

        return response
    


class PdfSentencesRetreiveView(views.APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]
    def get(self, request, id):
        queryset = get_object_or_404( Sentence, pdfID=id)
        serializer = SentenceSerializer(queryset, many=True)
        sentences = serializer.data
        
        context = {'pdfID':id, 'sentences': []}
        for sentence in sentences :
            context['sentences'].append(sentence['sentenceText'])
        return response.Response(context)


class WordOcurranceView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]


    def get(self, request, id,  word, *args, **kwargs):
        pdf = get_object_or_404(PdfDocument, id=id)
        words =  Word.objects.all().filter(pdfID=id, word__contains=word)
        sentences = Sentence.objects.all().filter(pdfID=id, sentenceText__contains=word)


        occurence = sum([ word_obj.repeatTimes for word_obj in words])

        context = {
            'pdfID': id,
            'word': word, 
            'occurrence' : occurence,
            'sentences' : []
        }



        for sentence in sentences:
            context['sentences'].append(sentence.sentenceText)

        return response.Response(context)





class Top5OccurringWords(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]

    def get(self, request, id, *args, **kwargs):
        pdf = get_object_or_404(PdfDocument, id=id)
        stop_words = [
            'a', 'an', 'and', 'as', 'at', 'be', 'by',
            'for', 'from', 'has', 'he', 'in', 'is', 
            'it', 'its', 'of', 'on', 'that', 'the', 
            'to', 'was', 'were', 'with'
        ]

        stop_words.extend(
            [word.title() for word in stop_words]
            + 
            [word.capitalize() for word in stop_words]
            +
            list(punctuation)
        )
        print(punctuation.split())
        words = Word.objects.filter(pdfID=id).exclude(word__in=stop_words).order_by('-repeatTimes')[:5]

        context = {
            'pdfID': id,
            'top5words': [] 
        }

        context['top5words'].extend([instance.word for instance in words])

        return response.Response(context)



class GetPageAsImageView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]

    def get(self, request, id, pageNo, *args, **kwargs):
        pdf = get_object_or_404(PdfDocument, id=id)
        if  not (0 < pageNo <= pdf.pagesNo):
            return response.Response({'details': 'pdf does not have this page'}, status=status.HTTP_404_NOT_FOUND)

        file = pdf.pdfFile_id.file
        pdf_path = file.path
        doc_manip = PdfDocManip(pdf_path=pdf_path)
        image_path = doc_manip.get_page_as_image(page_num=pageNo).replace('/', '\\')
        print(image_path)
        
        file = open(image_path, 'rb')     
        fileresponse = FileResponse(file)
        fileresponse['Content-Disposition'] = f'attachment; filename="pdf-{id}-page-{pageNo}.jpeg"'
        fileresponse['Content-Type'] = 'image/jpeg'
        return fileresponse
    


class PdfDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]

    def delete(self, request, id, *args, **kwargs):
        pdf = get_object_or_404(PdfDocument, id=id)
        pdf.pdfFile_id.delete()
        pdf.delete()
        return response.Response(
            {'detail': 'Successfully deleted the PDF'},
            status=status.HTTP_204_NO_CONTENT
        )
