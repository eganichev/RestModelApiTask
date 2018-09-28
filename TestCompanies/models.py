from django.db import models
from rest_framework.exceptions import ValidationError


class Company(models.Model):
    name = models.CharField('Name', max_length=300)

    def save(self, *args, **kwargs):
        if self.offices.filter(is_headquarter=True).count() <= 1:
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Only one headquarter per company could be')


class Office(models.Model):
    street = models.CharField('Street', max_length=256, blank=True)
    postal_code = models.CharField('Postal Code', max_length=32, blank=True)
    city = models.CharField('City', max_length=128, blank=True, null=True)
    monthly_rent = models.DecimalField(decimal_places=2, max_digits=10,
                                       blank=True, null=True)
    company_owner = models.ForeignKey(Company, related_name='offices',
                                      on_delete=models.CASCADE)
    is_headquarter = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.company_owner.offices.filter(is_headquarter=True).count() == 1 and self.is_headquarter:
            raise ValidationError('Only one headquarter per company could be')
        else:
            super().save(*args, **kwargs)
