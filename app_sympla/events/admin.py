from django.contrib import admin
from events.models import Category, Batch, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    pass
