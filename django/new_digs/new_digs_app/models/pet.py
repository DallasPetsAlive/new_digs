from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=50)

    class Species(models.TextChoices):
        DOG = "DOG", ("Dog")
        CAT = "CAT", ("Cat")

    species = models.CharField(
        max_length=15,
        choices=Species.choices,
    )

    owner = models.ForeignKey(
        "Owner",
        on_delete=models.CASCADE,
    )
