from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    first_name = models.CharField(null=False, blank=False, max_length=255)
    last_name = models.CharField(null=False, blank=False, max_length=255)

    @property
    def spouse(self):
        try:
            marriage = Marriage.objects.get(spouse_a=self, status=Marriage.MARRIED)
            return marriage.spouse_b
        except Marriage.DoesNotExist:
            pass
        try:
            marriage = Marriage.objects.get(spouse_b=self, status=Marriage.MARRIED)
            return marriage.spouse_a
        except Marriage.DoesNotExist:
            pass
        return None

    def __str__(self):
        return self.first_name + " " + self.last_name


class Email(models.Model):
    owner = models.ForeignKey(Person, null=False, related_name="email_addresses")
    email_address = models.EmailField(null=False, blank=False)

    def __str__(self):
        return self.email_address


class Marriage(models.Model):
    MARRIED = 'M'
    DIVORCED = 'D'
    WIDOWED = 'W'
    MARITAL_STATUS = (
        (MARRIED, 'Married'),
        (DIVORCED, 'Divorced'),
        (WIDOWED, 'Widowed'),
    )

    spouse_a = models.ForeignKey(Person, null=False, related_name="spouse_a")
    spouse_b = models.ForeignKey(Person, null=False, related_name="spouse_b")
    status = models.CharField(max_length=1, choices=MARITAL_STATUS, default=MARRIED)
