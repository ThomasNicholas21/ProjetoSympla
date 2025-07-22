from django.contrib import admin
from events.models import Category, Batch, Events


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    pass


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    pass
