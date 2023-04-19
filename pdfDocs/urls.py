from django.urls import path
from .views import (
    CreateUserView, FileUploadView, PdfsListView,
    WordSearchView, PdfRetreiveView, PdfSentencesRetreiveView,
    WordOcurranceView, Top5OccurringWords, GetPageAsImageView,
    PdfDeleteView
    )

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-user/',  CreateUserView.as_view()), 
    path('upload-pdf/', FileUploadView.as_view()),
    path('pdfs-list/', PdfsListView.as_view()),
    path('word-search/<str:word>', WordSearchView.as_view()),
    path('retreive-pdf/<int:id>', PdfRetreiveView.as_view()),
    path('retreive-sentences/<int:id>', PdfSentencesRetreiveView.as_view()),
    path('word-occurrence/<int:id>/<str:word>', WordOcurranceView.as_view()),
    path('top-5-words/<int:id>', Top5OccurringWords.as_view()),
    path('get-page-image/<int:id>/<int:pageNo>', GetPageAsImageView.as_view()),
    path('delete-pdf/<int:id>', PdfDeleteView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
