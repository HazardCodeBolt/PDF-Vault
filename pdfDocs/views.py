from .serializers import (
UserSerializer, PdfDocumentSerializer,
SentenceSerializer, WordSerializer, FileUploadSerializer
)

from rest_framework import generics, permissions, authentication, views, parsers, response
from django.contrib.auth import get_user_model
from .models import FileUpload, PdfDocument



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


