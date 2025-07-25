from rest_framework import serializers
from events.models import Event, Location, Category


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_name', 'city']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'start_date',
            'location', 'category',
            'sympla_id', 'batch'
        ]

    location = LocationSerializer()
    category = CategorySerializer(many=True)
