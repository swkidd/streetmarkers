from django.urls import path

from . import views

app_name = 'pegs'

urlpatterns = [
    path('', views.PegDetailView.as_view(), name='peg_detail'),
]