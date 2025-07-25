from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from logs.models import Log
from logs.serializer import LogSerializer


class LogPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


@extend_schema_view(
    list=extend_schema(
        summary='Listar eventos',
        description=(
            'Retorna uma lista paginada de logs, ele armazena '
            'informações das importações feitas através do service '
            'sympla API.'
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
        ]
    )
)
class LogAPIView(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    pagination_class = LogPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
