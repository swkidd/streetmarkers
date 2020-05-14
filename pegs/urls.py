from django.urls import path

from . import views

app_name = 'pegs'

urlpatterns = [
    path('', views.PegDetailView.as_view(), name='peg_detail'),
    path('create/pegsystem/', views.PegSystemCreate.as_view(), name='pegsystem_create'),
    path('update/pegsystem/<int:pk>', views.PegSystemUpdate.as_view(), name='pegsystem_update'),
    path('delete/pegsystem/<int:pk>', views.PegSystemDelete.as_view(), name='pegsystem_delete'),
    path('<int:pk>/create/popeg/', views.POPegCreate.as_view(), name='popeg_create'),
    path('update/popeg/<int:pk>', views.POPegUpdate.as_view(), name='popeg_update'),
    path('delete/popeg/<int:pk>', views.POPegDelete.as_view(), name='popeg_delete'),
]