from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from problems.models import Problem

admin.site.register(Problem, MarkdownxModelAdmin)
