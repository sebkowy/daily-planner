from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.tasks.models import Task

class DailyPlan(models.Model):
    date = models.DateField(_('date'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_plans')
    tasks = models.ManyToManyField(Task, through='DailyPlanTask')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        unique_together = ('date', 'user')
        verbose_name = _('daily plan')
        verbose_name_plural = _('daily plans')

    def __str__(self):
        return f"Daily Plan for {self.user.get_full_name()} on {self.date}"

class DailyPlanTask(models.Model):
    daily_plan = models.ForeignKey('DailyPlan', on_delete=models.CASCADE, related_name='tasks')
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('daily_plan', 'task')

    def __str__(self):
        return f"{self.task.name} for {self.daily_plan}"

class MonthlyPlan(models.Model):
    month = models.PositiveIntegerField(_('month'))
    year = models.PositiveIntegerField(_('year'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='monthly_plans')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        unique_together = ('month', 'year', 'user')
        verbose_name = _('monthly plan')
        verbose_name_plural = _('monthly plans')

    def __str__(self):
        return f"Monthly Plan for {self.user.get_full_name()} - {self.month}/{self.year}"