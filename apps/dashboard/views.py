from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from apps.tasks.models import Task
from apps.plans.models import DailyPlan, MonthlyPlan
from apps.users.models import UserAvailability

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        user = request.user

        # Get today's plan
        today_plan = DailyPlan.objects.filter(user=user, date=today).first()

        # Get upcoming tasks
        upcoming_tasks = Task.objects.filter(created_by=user, dailyplantask__daily_plan__date__gt=today).distinct()[:5]

        # Get monthly plan for current month
        current_month_plan = MonthlyPlan.objects.filter(user=user, month=today.month, year=today.year).first()

        # Count total tasks
        total_tasks = Task.objects.filter(created_by=user).count()

        # Get next 7 days availability
        next_7_days = [today + timedelta(days=i) for i in range(7)]
        availabilities = UserAvailability.objects.filter(user=user, date__in=next_7_days)
        availability_dict = {av.date: av.is_available for av in availabilities}

        # Get high priority tasks
        high_priority_tasks = Task.objects.filter(created_by=user, priority__gte=3)[:5]


        dashboard_data = {
            "today_plan": {
                "date": today,
                "tasks": [
                    {
                        "name": task.task.name,
                        "start_time": task.start_time,
                        "end_time": task.end_time
                    } for task in today_plan.dailyplantask_set.all()
                ] if today_plan else []
            },
            "upcoming_tasks": [
                {
                    "name": task.name,
                    "next_occurrence": task.dailyplantask_set.filter(daily_plan__date__gt=today).order_by('daily_plan__date').first().daily_plan.date if task.dailyplantask_set.filter(daily_plan__date__gt=today).exists() else None
                } for task in upcoming_tasks
            ],
            "monthly_plan": {
                "month": current_month_plan.month if current_month_plan else None,
                "year": current_month_plan.year if current_month_plan else None,
                "total_days_planned": DailyPlan.objects.filter(user=user, date__month=today.month, date__year=today.year).count() if current_month_plan else 0
            },
            "total_tasks": total_tasks,
            "upcoming_availability": [
                {
                    'date': date,
                    'is_available': availability_dict.get(date, True)  # Default to available if not set
                } for date in next_7_days
            ],
            "high_priority_tasks": [
                {
                    "name": task.name,
                    "priority": task.get_priority_display(),
                } for task in high_priority_tasks
            ],
        }

        return Response(dashboard_data)