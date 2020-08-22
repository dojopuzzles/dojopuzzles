from django.test import TestCase

from model_bakery import baker

from problems.models import Problem, SelectUnpublishedProblemException


class ProblemTestCase(TestCase):
    def test_create_new_problem(self):
        problem = Problem(
            title="Problem Title",
            slug="problem-title",
            description="Problem Description",
            published=False,
            author="Problem Author or Contributor",
        )
        problem.save()

        saved_problems = Problem.objects.all()
        self.assertEqual(saved_problems.count(), 1)

    def test_problem_repr(self):
        problem = baker.make(Problem)
        self.assertEqual(repr(problem), f"<Problem: {problem.title}>")

    def test_new_problem_not_published_by_default(self):
        problem = Problem(title="Problem Title", description="Problem Description",)
        problem.save()

        self.assertFalse(problem.published)

    def test_add_slug_to_problem_if_not_provided(self):
        problem = Problem(title="Problem Title", description="Problem Description",)
        problem.save()

        saved_problem = Problem.objects.get(pk=problem.pk)
        self.assertEqual(saved_problem.slug, "problem-title")

    def test_selected_problem_increase_uses_count(self):
        problem = baker.make(Problem, published=True)

        self.assertEqual(problem.uses, 0)
        problem.select()
        self.assertEqual(problem.uses, 1)

    def test_unpublished_problem_can_not_be_selected(self):
        problem = baker.make(Problem, published=False)

        with self.assertRaises(SelectUnpublishedProblemException):
            problem.select()

