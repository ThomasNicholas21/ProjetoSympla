from django.urls import path
from events.views import home


app_name = 'events'


urlpatterns = [
    path('', home, name='home-view'),
]
