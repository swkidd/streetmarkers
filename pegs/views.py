from django.shortcuts import render

from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PegSystem, POPeg
from django.urls import reverse_lazy

class PegDetailView(LoginRequiredMixin, ListView):
    model = PegSystem 
    template_name = 'pegs/peg_detail.html'
    paginate_by = 5

    def get_queryset(self):
        return PegSystem.objects.filter(createdBy=self.request.user).order_by('title')


# Update views

class POPegUpdate(LoginRequiredMixin, UpdateView):
    model = POPeg
    fields = ['content', 'person', 'object']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('pegs:peg_detail')

# Delete views

class POPegDelete(LoginRequiredMixin, DeleteView):
    model = POPeg
    success_url = reverse_lazy('peg_detail')