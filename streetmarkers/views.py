import json
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Palace, Path, BasicMarker
from .forms import PalaceForm, PathForm, BasicMarkerForm

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

#import markdown


class UserPalaceView(LoginRequiredMixin, ListView):
    model = Palace
    template_name = 'streetmarkers/user_palace.html'
    paginate_by = 5

    def get_queryset(self):
        return Palace.objects.filter(createdBy=self.request.user).order_by('title')


class UserPalaceDetailView(LoginRequiredMixin, DetailView):
    model = Palace

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paths'] = Path.objects.filter(
            createdBy=self.request.user).filter(palace=self.get_object())
        return context


class UserPathDetailView(LoginRequiredMixin, DetailView):
    model = Path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['markers'] = BasicMarker.objects.filter(
            createdBy=self.request.user).filter(path=self.get_object())
        return context


class HomePageView(TemplateView):
    template_name = 'streetmarkers/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MapPageView(LoginRequiredMixin, TemplateView):
    template_name = 'streetmarkers/map.html'

    # support multiple form (marker) types by adding form list to context
    # use bootstrap forms to render conditional on a select tag
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basicMarkerForm'] = BasicMarkerForm
        context['basicPathForm'] = PathForm
        context['palaceForm'] = PalaceForm

        context['palaces'] = Palace.objects.filter(createdBy=self.request.user)
        logging.info(self.request.user)
        logging.info(context['palaces'])
        return context


@login_required
def create_marker(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        infoText = request.POST.get('infoText')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        response_data = {}

        marker = BasicMarker(title=title, infoText=infoText, lat=lat, lng=lng)
        marker.save()

        response_data['result'] = 'Create post successful!'
        response_data['markerpk'] = marker.pk
        response_data['title'] = marker.title
        response_data['infoText'] = marker.infoText
        response_data['lng'] = marker.lng
        response_data['lat'] = marker.lat

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_Type="application/json"
        )


@login_required
def load_paths(request):
    if request.method == 'GET':
        palace_id = request.GET.get('palace_id')
        paths = Path.objects.filter(palace_id=palace_id)
        response_data = [
            {
                'title': path.title,
                'palace_title': path.palace.title,
                'palace_id': path.palace.id,
                'type': path.type.typeName,
            } for path in paths
        ]
        logging.info(palace_id)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_Type="application/json"
        )
