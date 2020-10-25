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
        _ = baker.make(Problem, published=False, uses=1)
        most_used = Problem.objects.most_used()
        self.assertEqual(list(most_used), [])

    def test_most_used_sorted_by_uses(self):
        problem_1 = baker.make(Problem, published=True, uses=2)
        problem_2 = baker.make(Problem, published=True, uses=1)
        problem_3 = baker.make(Problem, published=True, uses=3)

        most_used = Problem.objects.most_used()
        self.assertEqual(list(most_used), [problem_3, problem_1, problem_2])


class TotalUsedProblemTestCase(TestCase):
    def test_zero_if_no_problems(self):
        total_used = Problem.objects.total_used()
        self.assertEqual(total_used, 0)

    def test_sum_of_uses_of_all_problems(self):
        _ = baker.make(Problem, published=True, uses=2)
        _ = baker.make(Problem, published=True, uses=1)
        total_used = Problem.objects.total_used()
        self.assertEqual(total_used, 3)


class PublishedProblemTestCase(TestCase):

    def setUp(self):
        self.problems = Problem.objects.published()

    def test_none_if_no_problem(self):
        self.assertEqual(0, self.problems.count())

    def test_none_if_no_published_problem(self):
        baker.make(Problem, published=False)
        self.assertEqual(0, self.problems.count())

    def test_two_problems_with_2_published__unpublished(self):
        baker.make(Problem, published=True, _quantity=2)
        baker.make(Problem, published=False)
        self.assertEqual(2, self.problems.count())
