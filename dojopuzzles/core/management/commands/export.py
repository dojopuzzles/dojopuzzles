import collections
import pickle

from django.core.management.base import BaseCommand
import psycopg2

Problem = collections.namedtuple(
    "Problem", "id,title,slug,description,author,published,uses"
)


class Command(BaseCommand):
    help = "Export problems from old dojopuzzles website"

    def add_arguments(self, parser):
        parser.add_argument("host", nargs="?")
        parser.add_argument("user", nargs="?")
        parser.add_argument("dbname", nargs="?")
        parser.add_argument("password", nargs="?")
        parser.add_argument("output", nargs="?")

    def _connect(self, dbname, user, host, password):
        conn = psycopg2.connect(
            f"dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        )
        return conn

    def handle(self, *args, **options):
        self.stdout.write("Dumping problems from old dojopuzzles website")

        host = options["host"]
        user = options["user"]
        dbname = options["dbname"]
        password = options["password"]
        output = options["output"]

        conn = self._connect(dbname, user, host, password)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                problema_id, COUNT(problema_id)
            FROM
                problemas_problemautilizado
            GROUP BY
                problema_id
        """
        )
        result = cur.fetchall()
        total_uses = {problem_id: problem_uses for problem_id, problem_uses in result}

        cur.execute(
            "SELECT id, titulo, slug, descricao, nome_contribuidor, publicado FROM problemas_problema"
        )
        result = cur.fetchall()

        all_problems = []
        for problem in result:
            id_, title, slug, description, author, published = problem
            all_problems.append(
                Problem(
                    id=id_,
                    title=title,
                    slug=slug,
                    description=description,
                    author=author,
                    published=published,
                    uses=total_uses.get(id_, 0),
                )
            )

        with open(output, "wb") as problems_file:
            pickle.dump(all_problems, problems_file)

        self.stdout.write(f"Problems exported to {output}")
