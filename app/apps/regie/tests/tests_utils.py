from apps.regie.utils import snake_case
from django.test import SimpleTestCase


class TestUtils(SimpleTestCase):
    def test_snake_case(self):
        """
        text_list only when an reopens when unhappy string
        """
        string_in = "Mock data mock mock"
        string_out = "mock_data_mock_mock"

        print(snake_case(string_in))
        self.assertEqual(snake_case(string_in), string_out)
