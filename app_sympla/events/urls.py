from django.urls import path
from events.views import SymplaImportView, SymplaListView


app_name = 'events'


urlpatterns = [
    path('', SymplaImportView.as_view(), name='home-view'),
    path('eventos/', SymplaListView.as_view(), name='list-view'),
]
