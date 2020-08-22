from unittest import mock

from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

import problems.views
from problems.models import Problem


class ProblemViewTestCase(TestCase):
    def setUp(self):
        self.problem = baker.make(Problem, published=True)

    def test_access_problem_detail_page(self):
        response = self.client.get(
            reverse("problems:problem_details", kwargs={"slug": self.problem.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_access_invalid_problem(self):
        response = self.client.get(
            reverse("problems:problem_details", kwargs={"slug": "i_do_not_exist"})
        )
        self.assertEqual(response.status_code, 404)

    def test_access_problem_detail_has_problem_in_context(self):
        response = self.client.get(
            reverse("problems:problem_details", kwargs={"slug": self.problem.slug})
        )
        self.assertTrue("problem" in response.context)
        self.assertEqual(self.problem, response.context["problem"])


class RandomProblemViewTestCase(TestCase):
    def test_access_random_problem(self):
        response = self.client.get(reverse("problems:problem_random"))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(problems.views.Problem.objects, "random")
    def test_access_random_problem_call_random_method(self, mock_random_method):
        response = self.client.get(reverse("problems:problem_random"))
        mock_random_method.assert_called_once()
