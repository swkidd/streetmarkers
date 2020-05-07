from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import Marker
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required 
from django.urls import reverse

import json
import markdown

class HomePageView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['markers'] = [ {
        #     **m,
        #     'infoText': markdown.markdown(m['infoText']),
        # } for m in Marker.objects.values()]
        return context

class MapPageView(LoginRequiredMixin, TemplateView):
    template_name = 'map.html'

    #support multiple form (marker) types by adding form list to context
    #use bootstrap forms to render conditional on a select tag
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['markers'] = [{
            **m,
            #remove html support for markdown
            'infoText': markdown.markdown(m['infoText']),
        } for m in Marker.objects.values()]
        return context

@login_required
def create_marker(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        infoText = request.POST.get('infoText')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        response_data = {}

        marker = Marker(title=title, infoText=infoText, lat=lat, lng=lng)
        marker.save()

        response_data['result'] = 'Create post successful!'
        response_data['markerpk'] = marker.pk
        response_data['title'] = marker.title
        response_data['infoText'] = markdown.markdown(marker.infoText)
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
