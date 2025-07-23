from django.shortcuts import render
from events.models import Event, Location, Category, Batch
from events.services import sympla_service
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime


def home(request):
    context = {}

    if request.method == "POST":
        s_token = request.POST.get("s_token")
        url = "https://api.sympla.com.br/public/v3/events"

        if not s_token:
            s_token = (
                'a28e68e547aacfa3426548a989e41e39'
                'f3db9d43a2cfe0ab4a261eec6f240b39'
            )

        try:
            events = sympla_service(url, s_token)
            batch = Batch.objects.create()

            for event in events:
                location_data = event['location']
                location_obj, _ = Location.objects.get_or_create(
                    location_name=location_data['location_name'],
                    city=location_data['city']
                )

                categories = []
                event_category = [
                    event['category_prim'], event['category_sec']
                ]
                for category_name in event_category:
                    if category_name:
                        category_obj, _ = (
                            Category.objects.get_or_create(
                                name=category_name
                            )
                        )
                        categories.append(category_obj)

                start_date = make_aware(parse_datetime(event['start_date']))

                event_obj = Event.objects.create(
                    name=event['name'],
                    start_date=start_date,
                    location=location_obj,
                    sympla_id=event['sympla_id'] + event['start_date'],
                    batch=batch
                )

                event_obj.category.set(categories)


            context['success'] = f"{len(events)} eventos importados com sucesso!" # noqa

        except Exception as e:
            context['error'] = f"Ocorreu um erro: {e}"

    return render(request, "events/page/sympla.html", context)


def list_view(request):
    batches = Batch.objects.prefetch_related('event_set__location', 'event_set__category') # noqa
    return render(request, 'events/page/list_sympla.html', {'batches': batches}) # noqa
