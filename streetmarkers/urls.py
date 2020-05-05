from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('map/', views.MapPageView.as_view(), name='map'),
    path('create_marker/', views.create_marker, name='create_marker')
]