from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=50)
    primary_breed = models.CharField(max_length=50, null=True)

    owner = models.ForeignKey(
        "Owner",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
