from django.urls import path,include
from .views import message_view,create_room

# Add your URL patterns here
urlpatterns = [
   
    # Example URL pattern
    # path('example/', views.example_view, name='example'),
    path('create_room/',create_room),
    path('<str:room_name>/<str:username>/',message_view,name='room')
]