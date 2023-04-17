from django.urls import path
from .views import (CreateUserView, FileUploadView)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-user/',  CreateUserView.as_view()), 
    path('upload-pdf/', FileUploadView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
