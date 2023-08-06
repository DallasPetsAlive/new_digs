# mypy: ignore-errors
# mypy doesn't play nice with polymporphic models
from django.db import models
from polymorphic.models import PolymorphicModel

from .constants import CAT_BREEDS, CAT_COLORS, DOG_BREEDS, DOG_COLORS


class Person(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ParticipantApplication(models.Model):
    applicant = models.ForeignKey(to=Person, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return f"{self.applicant.first_name} {self.applicant.last_name}"


_yes_no_unknown = (
    ("y", "Yes"),
    ("n", "No"),
    ("u", "Unknown"),
)


class Pet(PolymorphicModel):
    pet_name = models.CharField(max_length=50, blank=False)
    status = models.CharField(
        choices=(
            ("applied", "Applied, Not Yet Accepted"),
            ("rejected", "Rejected"),
            ("accepted", "Accepted, Not Yet Published"),
            ("published", "Published, Available for Adoption"),
            ("pending", "Adoption Pending"),
            ("adopted", "Adopted"),
            ("removed", "Removed from Program"),
        ),
        max_length=20,
        blank=False,
        default="applied",
    )
    size = models.CharField(
        choices=(
            ("s", "Small"),
            ("m", "Medium"),
            ("l", "Large"),
            ("xl", "Extra-Large"),
        ),
        max_length=2,
        blank=False,
    )
    age = models.CharField(
        choices=(
            ("baby", "Baby"),
            ("young", "Young"),
            ("adult", "Adult"),
            ("senior", "Senior"),
        ),
        max_length=10,
        blank=False,
    )

    thumbnail = models.URLField()

    original_owner = models.ForeignKey(
        Person,
        blank=False,
        on_delete=models.CASCADE,
    )
    participant_application = models.ForeignKey(
        ParticipantApplication,
        blank=False,
        on_delete=models.CASCADE,
    )

    disclaimers = models.TextField()
    public_description = models.TextField()

    mixed_breed = models.CharField(choices=_yes_no_unknown, max_length=1, blank=False)
    sex = models.CharField(
        choices=(
            ("m", "Male"),
            ("f", "Female"),
        ),
        max_length=1,
        blank=False,
    )
    okay_with_dogs = models.CharField(choices=_yes_no_unknown, max_length=1, blank=False)
    okay_with_cats = models.CharField(choices=_yes_no_unknown, max_length=1, blank=False)
    okay_with_kids = models.CharField(choices=_yes_no_unknown, max_length=1, blank=False)

    special_needs = models.BooleanField(blank=False, default=False)
    special_needs_description = models.TextField()

    altered = models.CharField(choices=_yes_no_unknown, max_length=1, blank=False)

    vaccinated = models.CharField(choices=_yes_no_unknown, max_length=1, blank=False)

    internal_notes = models.TextField()

    adopted_date = models.DateField(blank=True, null=True)
    made_available_for_adoption_date = models.DateField(blank=True, null=True)
    removed_from_program_date = models.DateField(blank=True, null=True)

    removal_reason = models.CharField(
        choices=(
            ("kept", "Decided to keep pet"),
            ("surrendered", "Surrendered to shelter"),
            ("rehomed", "Rehomed elsewhere"),
            ("non_res", "Owner non-responsive/non-compliant"),
            ("euth", "Euthanized"),
            ("passed", "Passed away"),
            ("other", "Other"),
        ),
        blank=True,
        max_length=20,
    )

    coat_length = models.CharField(
        choices=(
            ("sh", "Short"),
            ("med", "Medium"),
            ("lg", "Long"),
        ),
        blank=True,
        max_length=3,
    )

    def __str__(self):
        return f"{self.pet_name}"


class Media(models.Model):
    pet = models.ForeignKey(to=Pet, on_delete=models.CASCADE, blank=False)
    publish = models.BooleanField(blank=False, default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pet.pet_name} - {self.url}"


class Photo(Media):
    url = models.URLField(blank=False, unique=True)


class Video(Media):
    def _youtube_url(video_url):
        return "youtube" in video_url or "youtu.be" in video_url

    url = models.URLField(blank=False, unique=True, validators=[_youtube_url])


class MedicalRecord(Media):
    url = models.URLField(blank=False, unique=True)


class Cat(Pet):
    breed = models.CharField(
        max_length=50,
        choices=[(breed, CAT_BREEDS[breed]) for breed in CAT_BREEDS],
        blank=False,
    )
    declawed = models.CharField(choices=_yes_no_unknown, max_length=1, blank=False)
    litter_box_trained = models.CharField(choices=_yes_no_unknown, max_length=1, blank=False)
    color = models.CharField(
        max_length=50,
        choices=[(color, CAT_COLORS[color]) for color in CAT_COLORS],
        blank=False,
    )


class Dog(Pet):
    breed = models.CharField(
        max_length=50,
        choices=[(breed, DOG_BREEDS[breed]) for breed in DOG_BREEDS],
        blank=False,
    )
    housetrained = models.CharField(choices=_yes_no_unknown, max_length=1, blank=False)
    color = models.CharField(
        max_length=50,
        choices=[(color, DOG_COLORS[color]) for color in DOG_COLORS],
        blank=False,
    )


class AdoptionApplication(models.Model):
    applicant = models.ForeignKey(to=Person, on_delete=models.CASCADE, blank=False)
    pet = models.ForeignKey(to=Pet, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return f"{self.applicant.first_name} {self.applicant.last_name} - {self.pet.pet_name}"
