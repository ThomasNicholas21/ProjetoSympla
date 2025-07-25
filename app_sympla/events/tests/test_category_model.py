from django.core.exceptions import ValidationError
from events.tests.test_base import EventsFixture


class TestCategoryModel(EventsFixture):
    def setUp(self):
        self.category = self.make_category()
        return super().setUp()

    def test_category_name_max_length(self):
        setattr(self.category, 'name', 'Test' * 128)
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_category_str_method(self):
        self.category.name = 'Testing __str__'
        self.category.full_clean()
        self.category.save()

        self.assertEqual(
            str(self.category),
            'Testing __str__'
        )
