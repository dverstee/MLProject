from django.db import models


class ApiKey(models.Model):
    key = models.CharField(max_length=36, primary_key=True)
    usable_from = models.DateTimeField(default=None, blank=True, null=True)
    is_in_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_banned = models.BooleanField(default=False)