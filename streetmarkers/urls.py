from django.urls import path

from . import views

app_name = 'streetmarkers'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('map/', views.MapPageView.as_view(), name='map'),
    path('create_marker/', views.create_marker, name='create_marker')
]