from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('create_marker/', views.create_marker, name='create_marker')
]