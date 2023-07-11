from django.db import models

from new_digs_app.constants import DOG_BREEDS

from .pet import Pet


class Dog(Pet):
    class Meta:
        constraints = [
            models.CheckConstraint(
                name="dog_primary_breed_check",
                check=models.Q(primary_breed__in=DOG_BREEDS),
            )
        ]
