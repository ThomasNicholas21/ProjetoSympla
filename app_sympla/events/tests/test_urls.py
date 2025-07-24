from events.tests.test_base import EventsFixture
from django.urls import reverse


class TestUrl(EventsFixture):
    def test_home_view_url(self):
        home_view_url = reverse('events:home-view')
        self.assertEqual(home_view_url, '/')

    def test_list_view_url(self):
        list_view_url = reverse('events:list-view')
        self.assertEqual(list_view_url, '/eventos/')
