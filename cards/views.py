from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, DetailView, UpdateView
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from PIL import Image as PILImage
from itertools import cycle
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import openpyxl
# import requests
from bs4 import BeautifulSoup
from django_htmx.http import HttpResponseClientRedirect
from django_htmx.http import HttpResponseClientRefresh
from django_htmx.http import retarget
from django_htmx.middleware import HtmxDetails
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.shortcuts import render
import time

from .models import Card, Image
from .forms import FileFieldForm, CardUpdateForm
from service.image_processor import ImageProcessor


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


class CardListView(LoginRequiredMixin, ListView):
    context_object_name = 'card_list'
    template_name = 'cards/card_list.html'
    login_url = 'login'

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        object_list = self.get_queryset()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['time_stamp'] = time.time_ns()
        return context


class CardDetailView(LoginRequiredMixin, DetailView, UpdateView):
    context_object_name = 'card'
    template_name = 'cards/card_detail.html'
    login_url = 'login'
    pk_url_kwarg = 'pk'
    form_class = CardUpdateForm

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        object_list = self.get_queryset()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['time_stamp'] = time.time_ns()
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class UploadImagesView(LoginRequiredMixin, FormView):
    template_name = 'cards/upload_images.html'
    form_class = FileFieldForm
    success_url = reverse_lazy('cards')

    def get_success_url(self):
        card_pk = Card.objects.filter(user=self.request.user).first().id
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


def export_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="mydata.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'My Data'

    queryset = list(Card.objects.filter(user=request.user).values_list('pk', 'title', 'description', 'price'))
    for row_num, row in enumerate(queryset, 1):
        image = Image.objects.filter(card_id=row[0])
        for each in image:
            row = row + (each.path.url, )
        for col_num, cell_value in enumerate(row[1:], 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
    workbook.save(response)
    return response



@require_http_methods(["DELETE", "POST", "PUT"])
def rotate_image(request: HtmxHttpRequest, pk) -> HttpResponse:
    image = Image.objects.get(id=pk)
    rotated_image = PILImage.open(image.path.path)
    rotated_image = rotated_image.rotate(270, PILImage.NEAREST, expand=True)
    rotated_image.save(image.path.path)
    return render(request, 'cards/img-rotate.html',
                  {
                      "img_pk": pk,
                      "img_url": image.path.url,
                      "time_stamp": time.time_ns()
                  },
                  )


def collect_words(image_url, domain='https://bidlot.ru'):
    words = list()
    try:
        url = r'https://yandex.ru/images/search?source=collections&rpt=imageview&url=' + domain + image_url
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        similar = (soup.find('div', class_='Tags_type_expandable')
                   .find_all('span', class_='Button2-Text'))
        for i in similar:
            words.append(i.getText())
    except Exception as msg:
        logger.info(f"{msg}")
        words.append(msg)
    return words
