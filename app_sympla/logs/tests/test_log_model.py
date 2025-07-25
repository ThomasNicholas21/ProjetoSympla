from django.core.exceptions import ValidationError
from logs.tests.test_base import LogFixture


class TestLogModel(LogFixture):
    def setUp(self):
        self.log = self.make_log()
        return super().setUp()

    def test_log_status_max_length(self):
        setattr(self.log, 'status', 'Test' * 12)
        with self.assertRaises(ValidationError):
            self.log.full_clean()

    def test_log_str_method(self):
        self.log.full_clean()
        self.log.save()

        self.assertEqual(
            str(self.log),
            f'Log: da carga {self.log.batch.pk}'
        )
