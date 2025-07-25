from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.http import HttpResponse
from events.models import Event
import csv


class CsvAPIView(ViewSet):
    @extend_schema(
        summary='Exportar eventos em CSV',
        description=(
            'Gera um arquivo CSV contendo todos os eventos cadastrados.'
        ),
        responses={
            200: OpenApiResponse(
                description='Arquivo CSV gerado com sucesso (UTF-8 com BOM).'
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='export-csv')
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename='eventos.csv'"

        response.write(u'\ufeff')
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Nome', 'Data de Início', 'Local', 'Cidade',
            'Categorias', 'Sympla ID', 'Batch ID'
        ])

        events = Event.objects.all().select_related(
            'location', 'batch'
        ).prefetch_related('category')

        for event in events:
            categories = ', '.join(c.name for c in event.category.all())
            writer.writerow([
                event.id,
                event.name,
                event.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                event.location.location_name if event.location else '',
                event.location.city if event.location else '',
                categories,
                event.sympla_id,
                event.batch.id if event.batch else '',
            ])

        return response
