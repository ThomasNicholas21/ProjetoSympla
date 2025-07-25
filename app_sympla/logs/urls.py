from django.urls import path
from logs.views import LogAPIView


app_name = 'log'


urlpatterns = [
    path(
        'logs/public/v1/api/',
        LogAPIView.as_view(
            {
                'get': 'list'
            }
        ),
        name='log-api-view'
    ),
]
