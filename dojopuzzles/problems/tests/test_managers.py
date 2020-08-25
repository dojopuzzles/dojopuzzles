from django.test import TestCase
from problems.models import Problem

from model_bakery import baker


class MostUsedProblemTestCase(TestCase):
    def test_none_if_no_uses(self):
        baker.make(Problem, published=True)
        most_used = Problem.objects.most_used()
        self.assertEqual(list(most_used), [])

    def test_return_problem_if_has_uses(self):
        problem = baker.make(Problem, published=True, uses=1)
        most_used = Problem.objects.most_used()
        self.assertEqual(list(most_used), [problem])

    def test_return_none_if_unpublished(self):
        problem = baker.make(Problem, published=False, uses=1)
        most_used = Problem.objects.most_used()
        self.assertEqual(list(most_used), [])

    def test_most_used_sorted_by_uses(self):
        problem_1 = baker.make(Problem, published=True, uses=2)
        problem_2 = baker.make(Problem, published=True, uses=1)
        problem_3 = baker.make(Problem, published=True, uses=3)

        most_used = Problem.objects.most_used()
        self.assertEqual(list(most_used), [problem_3, problem_1, problem_2])
