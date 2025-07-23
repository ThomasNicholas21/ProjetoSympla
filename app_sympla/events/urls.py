from django.urls import path
from events.views import home, list_view


app_name = 'events'


urlpatterns = [
    path('', home, name='home-view'),
    path('eventos/', list_view, name='list-view'),
]
