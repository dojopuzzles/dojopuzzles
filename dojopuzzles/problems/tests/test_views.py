from unittest import mock

from django.test import TestCase
from django.urls import reverse

from model_bakery import baker
from markdownx.utils import markdownify

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

    def test_access_problem_detail_description_is_formatted_with_markdown(self):
        response = self.client.get(
            reverse("problems:problem_details", kwargs={"slug": self.problem.slug})
        )
        self.assertEqual(self.problem.formatted_description(), markdownify(self.problem.description))


class RandomProblemViewTestCase(TestCase):
    def setUp(self):
        self.problem = baker.make(Problem, published=True)

    def test_access_random_problem(self):
        response = self.client.get(reverse("problems:problem_random"))
        self.assertRedirects(
            response,
            reverse("problems:problem_details", kwargs={"slug": self.problem.slug}),
        )

    @mock.patch.object(problems.views.Problem.objects, "random")
    def test_access_random_problem_call_random_method(self, mock_random_method):
        mock_random_method.return_value = self.problem

        self.client.get(reverse("problems:problem_random"))
        mock_random_method.assert_called_once()


class ProblemSelectViewTestCase(TestCase):
    def setUp(self):
        self.problem = baker.make(Problem, published=True)

    def test_unable_to_select_not_published_problem(self):
        problem = baker.make(Problem, published=False)
        response = self.client.get(
            reverse("problems:problem_select", kwargs={"problem_id": problem.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_select_problem_redirect_to_problem_details_page(self):
        response = self.client.get(
            reverse("problems:problem_select", kwargs={"problem_id": self.problem.id})
        )
        self.assertRedirects(
            response,
            reverse("problems:problem_details", kwargs={"slug": self.problem.slug}),
        )

    def test_select_problem_increase_problem_uses(self):
        self.assertEqual(self.problem.uses, 0)
        _ = self.client.get(
            reverse("problems:problem_select", kwargs={"problem_id": self.problem.id})
        )
        problem = Problem.objects.get(pk=self.problem.id)
        self.assertEqual(problem.uses, 1)

    def test_select_problem_add_its_pk_in_session(self):
        response = self.client.get(
            reverse("problems:problem_select", kwargs={"problem_id": self.problem.id}),
            follow=True,
        )
        self.assertEqual(self.client.session.get("problem_selected"), self.problem.id)
