from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from apps.departments.models import Department



class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=15, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    job_position = models.CharField(_('job position'), max_length=100, blank=True)
    CONTRACT_TYPES = (
        ('FT', _('Full Time')),
        ('PT', _('Part Time')),
        ('CT', _('Contract')),
    )
    contract_type = models.CharField(_('contract type'), max_length=2, choices=CONTRACT_TYPES, default='FT')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = CustomUserManager()

class UserAvailability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField(_('date'))
    is_available = models.BooleanField(_('is available'), default=True)
    note = models.TextField(_('note'), blank=True)

    class Meta:
        unique_together = ('user', 'date')
        verbose_name = _('user availability')
        verbose_name_plural = _('user availabilities')

    def __str__(self):
        return f"{self.user.get_full_name()} - {'Available' if self.is_available else 'Unavailable'} on {self.date}"