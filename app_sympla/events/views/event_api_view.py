from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from events.models import Event
from events.serializer import EventSerializer


class EventPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


@extend_schema_view(
    list=extend_schema(
        summary='Listar eventos',
        description=(
            'Retorna uma lista paginada de eventos, podendo ser '
            'filtrada por batch, nome e data de início. Além disso, '
            'tem params para paginação, sendo elas, page e page_size.'
        ),
        parameters=[
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Número da página (paginação)',
            ),
            OpenApiParameter(
                name='page_size',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Tamanho da página. Máximo: 10',
            ),
            OpenApiParameter(
                name='batch',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID do batch (carga de eventos)',
            ),
            OpenApiParameter(
                name='name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    'Filtro por nome '
                    '(case insensitive, aceita letras '
                    'maiúsculas e minúsculas)'
                ),
            ),
            OpenApiParameter(
                name='start_date',
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description='Data de início do evento (formato: YYYY-MM-DD)',
            ),
        ]
    )
)
class EventAPIView(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventPagination

    def list(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-id')

        batch = request.query_params.get('batch')
        name = request.query_params.get('name')
        start_date = request.query_params.get('start_date')

        if batch:
            queryset = queryset.filter(batch=batch)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if start_date:
            queryset = queryset.filter(start_date=start_date)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
