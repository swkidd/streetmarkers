from django.shortcuts import render

from .models import PegSystem
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class PegDetailView(LoginRequiredMixin, ListView):
    model = ListView 
    template_name = 'pegs/peg_detail.html'
    paginate_by = 5

    def get_queryset(self):
        return PegSystem.objects.filter(createdBy=self.request.user).order_by('title')
