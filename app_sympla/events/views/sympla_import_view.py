from django.views.generic import TemplateView
from django.shortcuts import render
from django.db import transaction
from django.utils.timezone import datetime
from django.utils.dateparse import parse_datetime
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from events.models import Event, Location, Category, Batch
from events.services import sympla_service
from logs.models import Log
from typing import Any


URL = 'https://api.sympla.com.br/public/v1.5.1/events'


class SymplaImportView(TemplateView):
    template_name = 'events/page/sympla.html'

    def get_context_data(self, **kwargs) -> dict[Any]:
        context: dict = super().get_context_data(**kwargs)
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context: dict = {}

        s_token: str = request.POST.get('s_token') or (
                'a28e68e547aacfa3426548a989e41e39'
                'f3db9d43a2cfe0ab4a261eec6f240b39'
            )
        page_size: str = request.POST.get('page_size') or 100
        page: str = request.POST.get('page') or 1

        try:
            events: list[dict] = sympla_service(
                    url=URL,
                    s_token=s_token,
                    page_size=int(page_size),
                    page=int(page)
                )
            created_count: int = 0

            with transaction.atomic():
                batch: Batch = Batch.objects.create()

                for event in events:
                    location: Location = self.get_or_create_location(
                        event['location']
                    )
                    categories: list = self.get_or_create_categories(
                        event.get('category_prim'),
                        event.get('category_sec')
                    )

                    start_date: datetime = parse_datetime(event['start_date'])

                    last_event: Event = Event.objects.get_last_event(
                        sympla_id=event['sympla_id']
                        )

                    if self.should_create_event(
                        last_event,
                        event,
                        start_date,
                        location,
                        categories
                    ):
                        event_object: Event = Event.objects.create(
                            sympla_id=event['sympla_id'],
                            name=event['name'],
                            start_date=start_date,
                            location=location,
                            batch=batch
                        )
                        event_object.category.set(categories)
                        created_count += 1

            if created_count:
                context['success'] = f'{created_count} evento(s) importado(s)!'
            else:
                context['success'] = 'Nenhum evento novo para importar.'

        except Exception as e:
            context['error'] = f'Ocorreu um erro: {str(e)}'

        self.create_log(
            batch=batch,
            context=context,
            created_count=created_count
        )

        return render(request, self.template_name, context)

    def get_or_create_location(self, location_data: dict[str]) -> Location:
        location, _ = Location.objects.get_or_create(
            location_name=location_data['location_name'],
            city=location_data['city']
        )
        return location

    def get_or_create_categories(
                self,
                *category_names: tuple
            ) -> list[Category]:
        categories: list = []
        for name in category_names:
            if name:
                category, _ = Category.objects.get_or_create(name=name)
                categories.append(category)
        return categories

    def should_create_event(
                self, last_event: Event,
                event_data: dict, start_date: datetime,
                location: Location, categories: list
            ) -> bool:
        if not last_event:
            return True

        current_category_names = set(c.name for c in categories)
        last_category_names = set(
            last_event.category.values_list(
                'name', flat=True
                )
            )

        return (
            last_event.name != event_data['name'] or
            last_event.start_date != start_date or
            last_event.location != location or
            current_category_names != last_category_names
        )

    def create_log(
                self, batch: Batch,
                context: dict, created_count: int
            ) -> None:
        Log.objects.create(
            batch=batch,
            message=context['success'] or context['error'],
            imported_amount=created_count,
            status=(
                'success'
                if context['success']
                else 'error'
            )
        )
