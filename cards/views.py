from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Card


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
