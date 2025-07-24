from django.views.generic import ListView
from events.models import Batch


class SymplaListView(ListView):
    model = Batch
    template_name = 'events/page/list_sympla.html'
    context_object_name = 'batches'
    queryset = Batch.objects.prefetch_location_and_category_set()
    ordering = '-id'
