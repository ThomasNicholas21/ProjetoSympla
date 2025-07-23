from django.core.exceptions import ValidationError
from logs.tests.test_base import LogFixture


class TestLogModel(LogFixture):
    def setUp(self):
        self.log = self.create_log()
        return super().setUp()

    def test_log_status_max_length(self):
        setattr(self.log, 'status', 'Test' * 12)
        with self.assertRaises(ValidationError):
            self.log.full_clean()
