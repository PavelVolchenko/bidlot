from django.urls import path

from .views import CardListView, CardDetailView, UploadImagesView

urlpatterns = [
    path("", CardListView.as_view(), name="card_list"),
    path("<uuid:pk>/", CardDetailView.as_view(), name="card_detail"),
    path("upload-images/", UploadImagesView.as_view(), name="upload_images"),
]
