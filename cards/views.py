from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, DetailView
from django.urls import reverse_lazy, reverse
from PIL import Image as PILImage
from itertools import cycle
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from .models import Card, Image
from .forms import FileFieldForm
from service.image_processor import ImageProcessor


class CardListView(LoginRequiredMixin, ListView):
    context_object_name = 'card_list'
    template_name = 'cards/card_list.html'
    login_url = 'login'

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)


class CardDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'card'
    template_name = 'cards/card_detail.html'
    login_url = 'login'

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)


class UploadImagesView(LoginRequiredMixin, FormView):
    template_name = 'cards/upload_images.html'
    form_class = FileFieldForm
    success_url = reverse_lazy('cards')

    def get_success_url(self):
        card_pk = Card.objects.filter(user_id=self.request.user.pk).first().id
        return reverse('card_detail', kwargs={'pk': card_pk})

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        image_format = "JPG"
        face, back = list(), list()
        np_array = cycle([face, back])
        for f in files:
            image = PILImage.open(f)
            scan = ImageProcessor(image)
            add_array = next(np_array)
            for cropped_image in scan.cropped_images:
                add_array.append(cropped_image)
        for first, second in zip(face, back):
            card = Card.objects.create(user_id=self.request.user.pk)
            image_1 = Image.objects.create(card=card)
            image_2 = Image.objects.create(card=card)
            filename = str(card.pk)
            save_numpy_array_as_image(
                first,
                image_1.path,
                filename + "-1." + image_format)
            save_numpy_array_as_image(
                second,
                image_2.path,
                filename + "-2." + image_format)
            # words_list = collect_words(image_1.image.url)
            # card.parsed_info = ' '.join(words_list)
            # card.description = ' '.join(words_list).title()
            card.title = f"{card.pk}"
            card.description = f"{card.pk}"
            card.price = 1000

            card.save()
        return super().form_valid(self)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Загрузка изображений'
        return context


def save_numpy_array_as_image(numpy_array, image_field, filename):
    pil_image = PILImage.fromarray(numpy_array)
    buffer = BytesIO()
    pil_image.save(buffer, format='JPEG')
    image_file = InMemoryUploadedFile(buffer, None, filename, 'image/jpeg',
                                      buffer.tell(), None)
    image_field.save(filename, image_file)
