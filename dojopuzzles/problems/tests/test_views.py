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


class ProblemListTestCase(TestCase):

    def test_template(self):
        response = self.client.get(reverse("problems:problem_list"))
        self.assertTemplateUsed(response, 'problems/list.html')

    def test_empty_message(self):
        baker.make(Problem, published=False)
        response = self.client.get(reverse("problems:problem_list"))
        self.assertContains(response, 'Nenhum problema encontrado.')

    def test_not_empty_message(self):
        baker.make(Problem, published=True)
        response = self.client.get(reverse("problems:problem_list"))
        self.assertNotContains(response, 'Nenhum problema encontrado.')

    def test_page_2(self):
        baker.make(Problem, published=True, _quantity=16)
        response = self.client.get(reverse("problems:problem_list"))
        self.assertContains(response, '<a href="?page=2">')

    def test_redirect_last_page_if_access_gratter_pagenum(self):
        baker.make(Problem, published=True, _quantity=16)
        response = self.client.get(f'{reverse("problems:problem_list")}?page=42')
        self.assertNotContains(response, '<a href="?page=2">')

    def test_redirect_first_page_if_access_invalid_page(self):
        baker.make(Problem, published=True, _quantity=16)
        response = self.client.get(f'{reverse("problems:problem_list")}?page=invalid_page')
        self.assertNotContains(response, '<a href="?page=1">')
