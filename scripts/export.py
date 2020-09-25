import collections
import pickle

import psycopg2

Problem = collections.namedtuple(
    "Problem", "id,title,description,author,published,uses"
)


def connect(dbname, user, host, password):
    conn = psycopg2.connect(
        f"dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
    )
    return conn


def dump_problems(dbname, user, host, password, dump_file):
    """Dump problems from old Dojopuzzles database"""

    conn = connect(dbname, user, host, password)
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
        "SELECT id, titulo, descricao, nome_contribuidor, publicado FROM problemas_problema"
    )
    result = cur.fetchall()

    all_problems = []
    for problem in result:
        id_, title, description, author, published = problem
        all_problems.append(
            Problem(
                id=id_,
                title=title,
                description=description,
                author=author,
                published=published,
                uses=total_uses.get(id_, 0),
            )
        )

    with open(dump_file, "wb") as problems_file:
        pickle.dump(all_problems, problems_file)
