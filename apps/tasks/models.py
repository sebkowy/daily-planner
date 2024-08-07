from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    TASK_TYPES = (
        ('SD', 'Service Desk'),
        ('ESK', 'Eskalacje'),
        ('MFIF', 'MFIF'),
        ('SNOW', 'ServiceNow'),
        ('EIR', 'EIR'),
        ('MON', 'Monitoring'),
        ('OTHER', 'Other'),
    )

    PRIORITY_CHOICES = (
        (1, _('Low')),
        (2, _('Medium')),
        (3, _('High')),
        (4, _('Urgent')),
    )


    name = models.CharField(_('task name'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    task_type = models.CharField(_('task type'), max_length=5, choices=TASK_TYPES)
    duration = models.DurationField(_('duration'), help_text=_('Expected duration of the task'))
    is_cyclical = models.BooleanField(_('is cyclical'), default=False)
    cycle_time = models.DurationField(_('cycle time'), null=True, blank=True, help_text=_('Time between cycles for cyclical tasks'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    priority = models.IntegerField(_('priority'), choices=PRIORITY_CHOICES, default=2)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')