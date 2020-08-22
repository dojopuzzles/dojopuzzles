from django.db import models


class ProblemManager(models.Manager):

    def random(self):
        return self.order_by("?").first()
