from django.db import models


class ProblemManager(models.Manager):
    def most_used(self):
        return (
            super()
            .get_queryset()
            .filter(uses__gt=0)
            .filter(published=True)
            .order_by("-uses")
        )

    def random(self):
        return self.order_by("?").first()
