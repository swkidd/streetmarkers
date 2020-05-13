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

class POPegCreate(LoginRequiredMixin, CreateView):
    model = POPeg
    fields = ['content', 'person', 'object', 'notes', 'pegSystem', 'pegType']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('pegs:peg_detail')


# Update views
# assert user is createdBy user

class POPegUpdate(LoginRequiredMixin, UpdateView):
    model = POPeg
    fields = ['content', 'person', 'object']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('pegs:peg_detail')

# Delete views
# assert user is createdBy user

class POPegDelete(LoginRequiredMixin, DeleteView):
    model = POPeg
    success_url = reverse_lazy('pegs:peg_detail')