from django.shortcuts import render

from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)

import random

from .models import Card

from .forms import CardCheckForm
from django.shortcuts import get_object_or_404, redirect

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by("box_number","-date_created")


class BoxView(CardListView):
    template_name = "flashcards/box.html"
    form_class = CardCheckForm

    def get_queryset(self):
        return Card.objects.filter(box_number=self.kwargs["box_num"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["box_number"] = self.kwargs["box_num"]
        if self.object_list:
            context["check_card"] = random.choice(self.object_list)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            card.move(form.cleaned_data["solved"])

        return redirect(request.META.get("HTTP_REFERER"))


class CardCreateView(CreateView):
    model = Card
    fields = ["question","answer","box_number"]
    success_url = reverse_lazy("card-create")
    
class CardUpdateView(CardCreateView,UpdateView):
    success_url = reverse_lazy("card-list")
