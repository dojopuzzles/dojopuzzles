from django.db import models
from django.utils.text import slugify

from problems.managers import ProblemManager


class SelectUnpublishedProblemException(Exception):
    ...


class Problem(models.Model):
    title = models.CharField(max_length=100, blank=False)
    slug = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    author = models.CharField(max_length=100, blank=True, null=True)
    published = models.BooleanField(default=False)
    uses = models.IntegerField(default=0)

    objects = ProblemManager()

    class Meta:
        verbose_name = "problem"
        verbose_name_plural = "problems"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("problems:problem_details", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def select(self):
        """ Problem is selected for Coding Dojo """
        if self.published:
            self.uses += 1
            self.save()
        else:
            raise SelectUnpublishedProblemException()
