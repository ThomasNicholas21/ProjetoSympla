from django.contrib import admin
from events.models import Category, Batch, Event, Location


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_max_show_all = 10
    ordering = '-id',


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_max_show_all = 10
    list_display = ['id', 'created_at']
    ordering = '-id',


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_max_show_all = 10
    list_display = ['id', 'name', 'start_date']
    ordering = '-id',


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_max_show_all = 10
    list_display = ['id', 'location_name', 'city']
    ordering = '-id',
