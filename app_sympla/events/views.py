from django.shortcuts import render
from django.db import transaction
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive
from events.models import Event, Location, Category, Batch
from events.services import sympla_service


URL = "https://api.sympla.com.br/public/v1.5.1/events"


def home(request):
    context = {}

    if request.method == "POST":
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
                    location_data = event.get('location')
                    location_object, _ = Location.objects.get_or_create(
                        location_name=location_data['location_name'],
                        city=location_data['city']
                    )

                    categories = []
                    event_categories = [
                        event['category_prim'], event['category_sec']
                    ]
                    for name in event_categories:
                        if name:
                            category_object, _ = (
                                Category.objects.get_or_create(
                                    name=name
                                )
                            )
                            categories.append(category_object)

                    start_date = parse_datetime(event['start_date'])
                    if is_naive(start_date):
                        start_date = make_aware(start_date)

                    last_event = Event.objects.filter(
                        sympla_id=event['sympla_id']).order_by(
                            '-batch__id'
                        ).first()
                    should_create = False

                    if not last_event:
                        should_create = True
                    else:
                        if (
                            last_event.name != event['name'] or
                            last_event.start_date != start_date or
                            last_event.location != location_object or
                            set(
                                last_event.category.values_list(
                                    'name', flat=True
                                    )
                                ) != set(
                                    [
                                        c.name for c in categories
                                    ]
                                )
                        ):
                            should_create = True

                    if should_create:
                        event_object = Event.objects.create(
                            sympla_id=event['sympla_id'],
                            name=event['name'],
                            start_date=start_date,
                            location=location_object,
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

    return render(request, "events/page/sympla.html", context)


def list_view(request):
    batches = Batch.objects.prefetch_related('event_set__location', 'event_set__category').order_by('-id') # noqa
    return render(request, 'events/page/list_sympla.html', {'batches': batches}) # noqa
