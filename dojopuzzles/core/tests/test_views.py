from django.test import TestCase
from django.urls import reverse


class CorePagesViewTestCase(TestCase):
    def test_access_main_page(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_access_about_page(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)
