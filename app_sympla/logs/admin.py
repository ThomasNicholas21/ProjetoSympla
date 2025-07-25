from django.contrib import admin
from logs.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_max_show_all = 10
    list_display = [
        'id', 'batch', 'created_at',
        'imported_amount',
    ]
    ordering = '-id',
