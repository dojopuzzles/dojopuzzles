from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from problems.models import Problem


class CorePagesViewTestCase(TestCase):
    def test_access_main_page(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_access_about_page(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)


class HomeViewTestCase(TestCase):
    def test_home_has_total_number_of_problems_used_in_context(self):
        baker.make(Problem, uses=41)
        baker.make(Problem, uses=1)

        response = self.client.get(reverse("core:home"))
        self.assertTrue("problems_used" in response.context)
        self.assertEqual(42, response.context["problems_used"])
