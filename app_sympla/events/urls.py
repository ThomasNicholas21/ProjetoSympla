from django.urls import path
from events.views import SymplaImportView, SymplaListView, EventAPIView


app_name = 'events'


urlpatterns = [
    path('', SymplaImportView.as_view(), name='home-view'),
    path('eventos/', SymplaListView.as_view(), name='list-view'),

    # api view
    path('eventos/v1/api/', EventAPIView.as_view(
        {
            'get': 'list'
        }
    ), name='api-view'),
]
