from django.views.generic import ListView, DetailView

from .models import Card


class CardListView(ListView):
    model = Card
    context_object_name = 'card_list'
    template_name = 'cards/card_list.html'


class CardDetailView(DetailView):
    model = Card
    context_object_name = 'card'
    template_name = 'cards/card_detail.html'
