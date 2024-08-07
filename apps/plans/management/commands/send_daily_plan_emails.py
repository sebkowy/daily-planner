from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.plans.models import DailyPlan
from apps.plans.utils import send_daily_plan_email

class Command(BaseCommand):
    help = 'Sends daily plan emails to all users'

    def handle(self, *args, **options):
        today = timezone.now().date()
        daily_plans = DailyPlan.objects.filter(date=today)

        for plan in daily_plans:
            send_daily_plan_email(plan)
            self.stdout.write(self.style.SUCCESS(f'Successfully sent daily plan email to {plan.user.email}'))