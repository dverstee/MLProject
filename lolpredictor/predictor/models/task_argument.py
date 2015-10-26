from django.db import models
from lolpredictor.predictor.models import Task


class TaskArgument(models.Model):
    task = models.ForeignKey(Task)
    attribute = models.CharField(max_length=20)
    value = models.CharField(max_length=200)
    type = models.IntegerField()

    class Meta:
        unique_together = (("task", "attribute"),)