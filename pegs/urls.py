from django.urls import path

from . import views

app_name = 'pegs'

urlpatterns = [
    path('', views.PegDetailView.as_view(), name='peg_detail'),
    path('update/popeg/<int:pk>', views.POPegUpdate.as_view(), name='popeg_update'),
    path('delete/popeg/<int:pk>', views.POPegDelete.as_view(), name='popeg_delete'),
]