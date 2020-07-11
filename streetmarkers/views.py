import json
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Palace, Path, BasicMarker, MarkerType
from .forms import BasicMarkerForm

### logging ###
import logging
import logging.config
import sys

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

import markdown

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
        context['markers'] = [ {
            'title': m.title,
            'palace': m.palace,
            'path': m.path,
            'type': m.type,
            'lat': m.lat,
            'lng': m.lng,
            'infoText': markdown.markdown(m.infoText, safe_mode=True)
        } for m in BasicMarker.objects.all()]
        context['palaces'] = Palace.objects.filter(createdBy=self.request.user)
        return context


@login_required
def create_marker(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        infoText = request.POST.get('infoText')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        palace = Palace.objects.get(pk=request.POST.get('palace'))
        path = Path.objects.get(pk=request.POST.get('path'))
        type = MarkerType.objects.get(typeName='basic')
        response_data = {}

        marker = BasicMarker(
            createdBy=request.user, 
            title=title, 
            palace=palace, 
            path=path, 
            type=type, 
            infoText=infoText, 
            lat=lat, 
            lng=lng
        )
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

# loads all markers created by the logged in user
@login_required
def load_markers(request):
    if request.method == 'GET':
        basicMarkers = BasicMarker.objects.filter(createdBy=request.user) 
        markers = [ {
            'infoText': m.infoText,
            'lat': m.basemarker_ptr.lat,
            'lng': m.basemarker_ptr.lng,
            'title': m.basemarker_ptr.title,
            'path': m.basemarker_ptr.path.title,
            'palace': m.basemarker_ptr.palace.title,
        } for m in basicMarkers ]
        response_data = json.dumps(markers)
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
def get_palaces(request):
    if request.method == 'GET':
        palaces = Palace.objects.filter(createdBy=request.user) 
        palaces = [ {
            'title': m.title,
            'pk': m.pk,
        } for m in palaces]
        response_data = json.dumps(palaces)
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
def get_paths(request, pk):
    if request.method == 'GET':
        palace = Palace.objects.get(createdBy=request.user, pk=pk)
        paths = [ {
            'title': m.title,
            'pk': m.pk,
        } for m in palace.path_set.all()]
        response_data = json.dumps(paths)
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
def get_markers(request, pk):
    if request.method == 'GET':
        path = Path.objects.get(createdBy=request.user, pk=pk)
        markers = [ {
            'title': m.title,
            'pk': m.pk,
        } for m in path.basemarker_set.all()]
        response_data = json.dumps(markers)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_Type="application/json"
        )


#Create Views
# assert user is createdBy user

class PalaceCreate(LoginRequiredMixin, CreateView):
    model = Palace 
    fields = ['title']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('streetmarkers:user_palace')

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)

class PathCreate(LoginRequiredMixin, CreateView):
    model = Path 
    fields = ['title', 'type']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('streetmarkers:user_palace')

    def form_valid(self, form):
        palace = Palace.objects.get(pk=self.kwargs['pk'])
        form.instance.palace = palace
        form.instance.createdBy = self.request.user
        return super().form_valid(form)

#Update Views
# assert user is createdBy user

class PalaceUpdate(LoginRequiredMixin, UpdateView):
    model = Palace 
    fields = ['title']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('streetmarkers:user_palace')

class PathUpdate(LoginRequiredMixin, UpdateView):
    model = Path 
    fields = ['title', 'type']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('streetmarkers:user_palace')

class BasicMarkerUpdate(LoginRequiredMixin, UpdateView):
    model = BasicMarker 
    fields = ['title', 'path', 'infoText']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('streetmarkers:user_palace')

#Delete Views
# assert user is createdBy user

class PalaceDelete(LoginRequiredMixin, DeleteView):
    model = Palace 
    success_url = reverse_lazy('streetmarkers:user_palace')

class PathDelete(LoginRequiredMixin, DeleteView):
    model = Path 
    success_url = reverse_lazy('streetmarkers:user_palace')

class BasicMarkerDelete(LoginRequiredMixin, DeleteView):
    model = BasicMarker 
    success_url = reverse_lazy('streetmarkers:user_palace')