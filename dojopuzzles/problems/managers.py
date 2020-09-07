from django.db import models
from django.db.models import Sum


class ProblemManager(models.Manager):
    def most_used(self):
        return (
            super()
            .get_queryset()
            .filter(uses__gt=0)
            .filter(published=True)
            .order_by("-uses")
        )

    def total_used(self):
        return self.aggregate(Sum("uses")).get("uses__sum") or 0

    def random(self):
        return self.order_by("?").first()
