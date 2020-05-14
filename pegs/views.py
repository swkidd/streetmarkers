from django.shortcuts import get_object_or_404, render

from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PegSystem, POPeg, PegType
from django.urls import reverse_lazy

### logging ###
import logging
import logging.config
import sys
from django.urls.base import reverse
from django.db.models import Q

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)
######

class PegDetailView(LoginRequiredMixin, ListView):
    model = PegSystem 
    template_name = 'pegs/peg_detail.html'
    paginate_by = 5

    def get_queryset(self):
        return PegSystem.objects.filter(createdBy=self.request.user).order_by('title')


# Create views
# assert user is createdBy user

class PegSystemCreate(LoginRequiredMixin, CreateView):
    model = PegSystem 
    fields = ['title', 'description', 'pegType']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('pegs:peg_detail')

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)

class POPegCreate(LoginRequiredMixin, CreateView):
    model = POPeg
    fields = ['content', 'person', 'object', 'notes']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('pegs:peg_detail')

    def form_valid(self, form):
        pegSystem = PegSystem.objects.get(pk = self.kwargs['pk'])
        form.instance.pegSystem = pegSystem
        form.instance.pegType = pegSystem.pegType
        return super().form_valid(form)


# Update views
# assert user is createdBy user

class PegSystemUpdate(LoginRequiredMixin, UpdateView):
    model = PegSystem 
    fields = ['title', 'description']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('pegs:peg_detail')

class POPegUpdate(LoginRequiredMixin, UpdateView):
    model = POPeg
    fields = ['content', 'person', 'object']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('pegs:peg_detail')

# Delete views
# assert user is createdBy user

class PegSystemDelete(LoginRequiredMixin, DeleteView):
    model = PegSystem 
    success_url = reverse_lazy('pegs:peg_detail')

class POPegDelete(LoginRequiredMixin, DeleteView):
    model = POPeg
    success_url = reverse_lazy('pegs:peg_detail')