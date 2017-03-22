from django.contrib import admin
from .models import Challenge, Submission, HelpComment

admin.site.register(Challenge)
admin.site.register(Submission)
admin.site.register(HelpComment)
