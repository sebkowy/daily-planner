from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from .models import DailyPlan, DailyPlanTask
from apps.tasks.models import Task

class CalendarEventsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        if not start_date or not end_date:
            return Response({"error": "Both start and end dates are required."}, status=400)

        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()

        daily_plan_tasks = DailyPlanTask.objects.filter(
            daily_plan__user=request.user,
            daily_plan__date__range=[start_date, end_date]
        ).select_related('daily_plan', 'task')

        events = []
        for dpt in daily_plan_tasks:
            events.append({
                'id': f'dpt_{dpt.id}',
                'title': dpt.task.name,
                'start': timezone.datetime.combine(dpt.daily_plan.date, dpt.start_time),
                'end': timezone.datetime.combine(dpt.daily_plan.date, dpt.end_time),
                'allDay': False,
                'type': 'task'
            })

        # Add any tasks that are not part of a daily plan
        unscheduled_tasks = Task.objects.filter(
            created_by=request.user,
            dailyplantask__isnull=True
        )

        for task in unscheduled_tasks:
            events.append({
                'id': f'task_{task.id}',
                'title': task.name,
                'start': start_date,
                'end': start_date,
                'allDay': True,
                'type': 'unscheduled_task'
            })

        return Response(events)