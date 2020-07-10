from django.urls import path

from . import views

app_name = 'streetmarkers'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('user/palaces/', views.UserPalaceView.as_view(), name='user_palace'),
    path('user/palaces/create', views.PalaceCreate.as_view(), name='palace_create'),
    path('user/palaces/update/<int:pk>', views.PalaceUpdate.as_view(), name='palace_update'),
    path('user/palaces/delete/<int:pk>', views.PalaceDelete.as_view(), name='palace_delete'),
    path('user/<int:pk>/create/path', views.PathCreate.as_view(), name='path_create'),
    path('user/paths/update/<int:pk>', views.PathUpdate.as_view(), name='path_update'),
    path('user/paths/delete/<int:pk>', views.PathDelete.as_view(), name='path_delete'),
    path('user/markers/update/<int:pk>', views.BasicMarkerUpdate.as_view(), name='marker_update'),
    path('user/markers/delete/<int:pk>', views.BasicMarkerDelete.as_view(), name='marker_delete'),
    path('map/', views.MapPageView.as_view(), name='map'),
    path('ajax/create_marker/', views.create_marker, name='create_marker'),
    path('ajax/load_markers/', views.load_markers, name='load_markers'),
    path('ajax/get_palaces/', views.get_palaces, name='get_palaces')
]