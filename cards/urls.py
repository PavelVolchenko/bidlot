from django.urls import path

from .views import CardListView, CardDetailView, UploadImagesView, export_excel, rotate_image

urlpatterns = [
    path("", CardListView.as_view(), name="card_list"),
    path("<uuid:pk>/", CardDetailView.as_view(), name="card_detail"),
    path("upload-images/", UploadImagesView.as_view(), name="upload_images"),
    path('export/', export_excel, name='export_excel'),
]

htmx_urlpatterns = [
    path('rotate-image/<int:pk>/', rotate_image, name='rotate_image'),

]


urlpatterns += htmx_urlpatterns
