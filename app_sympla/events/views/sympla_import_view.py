from django.views.generic import TemplateView
from django.shortcuts import render
from django.db import transaction
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive
from events.models import Event, Location, Category, Batch
from events.services import sympla_service
from logs.models import Log


URL = "https://api.sympla.com.br/public/v1.5.1/events"


class SymplaImportView(TemplateView):
    template_name = "events/page/sympla.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        context = {}

        s_token = request.POST.get("s_token") or (
            'a28e68e547aacfa3426548a989e41e39'
            'f3db9d43a2cfe0ab4a261eec6f240b39'
        )

        try:
            events = sympla_service(URL, s_token=s_token)
            created_count = 0

            with transaction.atomic():
                batch = Batch.objects.create()

                for event in events:
                    location = self.get_or_create_location(event['location'])
                    categories = self.get_or_create_categories(
                        event.get('category_prim'),
                        event.get('category_sec')
                    )

                    start_date = parse_datetime(event['start_date'])
                    if is_naive(start_date):
                        start_date = make_aware(start_date)

                    last_event = Event.objects.get_last_event(
                        sympla_id=event['sympla_id']
                        )

                    if self.should_create_event(
                        last_event,
                        event,
                        start_date,
                        location,
                        categories
                    ):
                        event_object = Event.objects.create(
                            sympla_id=event['sympla_id'],
                            name=event['name'],
                            start_date=start_date,
                            location=location,
                            batch=batch
                        )
                        event_object.category.set(categories)
                        created_count += 1

            if created_count:
                context['success'] = f"{created_count} evento(s) importado(s)!"
            else:
                context['success'] = "Nenhum evento novo para importar."

        except Exception as e:
            context['error'] = f"Ocorreu um erro: {str(e)}"

        Log.objects.create(
            batch=batch,
            message=context['success'] or context['error'],
            imported_amount=created_count,
            status=(
                'sucess'
                if context['success']
                else 'error'
            )
        )

        return render(request, self.template_name, context)

    def get_or_create_location(self, location_data):
        location, _ = Location.objects.get_or_create(
            location_name=location_data['location_name'],
            city=location_data['city']
        )
        return location

    def get_or_create_categories(self, *category_names):
        categories = []
        for name in category_names:
            if name:
                category, _ = Category.objects.get_or_create(name=name)
                categories.append(category)
        return categories

    def should_create_event(
                self, last_event,
                event_data, start_date,
                location, categories
            ):
        if not last_event:
            return True

        current_cat_names = set(c.name for c in categories)
        last_cat_names = set(
            last_event.category.values_list(
                'name', flat=True
                )
            )

        return (
            last_event.name != event_data['name'] or
            last_event.start_date != start_date or
            last_event.location != location or
            current_cat_names != last_cat_names
        )

    def create_log(
                self, batch,
                context, created_count
            ):
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
