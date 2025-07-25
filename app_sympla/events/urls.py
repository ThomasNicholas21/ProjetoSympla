from django.urls import path
from rest_framework.routers import DefaultRouter
from events.views import (
    SymplaImportView,
    SymplaListView,
    EventAPIView,
    CsvAPIView
)


app_name = 'events'
router = DefaultRouter()
router.register(r'eventos/dump/v1/api', CsvAPIView, basename='csv')

urlpatterns = [
    path('', SymplaImportView.as_view(), name='home-view'),
    path('eventos/', SymplaListView.as_view(), name='list-view'),

    # api view
    path('eventos/public/v1/api/', EventAPIView.as_view(
        {
            'get': 'list'
        }
    ), name='event-api-view'),
    *router.urls,
]
