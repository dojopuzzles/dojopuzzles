import pickle

from django.core.management.base import BaseCommand

from core.management.commands.export import Problem  # noqa
from problems import models


class Command(BaseCommand):
    help = "Import problems from old dojopuzzles website"

    def add_arguments(self, parser):
        parser.add_argument("input_file")

    def handle(self, *args, **options):
        input_file = options["input_file"]

        self.stdout.write(f"Importing problems from {input_file}")

        input_file = options["input_file"]
        with open(input_file, "rb") as problems:
            all_problems = pickle.load(problems)

        for problem in all_problems:
            new_problem = models.Problem(
                title=problem.title,
                slug=problem.slug,
                description=problem.description,
                author=problem.author,
                published=problem.published,
                uses=problem.uses,
            )
            new_problem.save()

        self.stdout.write("{} problems imported".format(len(all_problems)))
