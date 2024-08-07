from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DailyPlan, DailyPlanTask, MonthlyPlan
from .serializers import DailyPlanSerializer, MonthlyPlanSerializer, DailyPlanTaskSerializer
from apps.tasks.models import Task
from apps.users.models import UserAvailability
from django.utils import timezone
from calendar import monthrange
from datetime import timedelta, datetime, time, date
from django.db.models import F


class DailyPlanViewSet(viewsets.ModelViewSet):
    queryset = DailyPlan.objects.all()
    serializer_class = DailyPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = DailyPlan.objects.filter(user=self.request.user)
        date = self.request.query_params.get('date', None)
        if date is not None:
            queryset = queryset.filter(date=date)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=False, methods=['post'])
    def generate(self, request):
        date_str = request.data.get('date')
        if date_str:
            try:
                plan_date = datetime.strptime(date_str, "%d-%m-%Y").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use DD-MM-YYYY."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            plan_date = timezone.now().date()

        user_availability = UserAvailability.objects.filter(user=request.user, date=plan_date).first()
        if user_availability and not user_availability.is_available:
            return Response({"message": f"User is not available on {plan_date}. Reason: {user_availability.note}"}, status=status.HTTP_200_OK)

        start_time = time(hour=9, minute=0)  # Assume workday starts at 9 AM
        end_time = time(hour=17, minute=0)   # Assume workday ends at 5 PM
        
        daily_plan, created = DailyPlan.objects.get_or_create(
            user=request.user,
            date=plan_date
        )

        # Clear existing tasks if the plan is being regenerated
        if not created:
            daily_plan.dailyplantask_set.all().delete()

        available_tasks = Task.objects.filter(created_by=request.user).order_by(F('priority').desc())
        current_time = start_time
        
        for task in available_tasks:
            if current_time >= end_time:
                break

            task_duration = task.duration
            task_end_time = (datetime.combine(plan_date, current_time) + task_duration).time()

            if task_end_time <= end_time:
                DailyPlanTask.objects.create(
                    daily_plan=daily_plan,
                    task=task,
                    start_time=current_time,
                    end_time=task_end_time
                )
                current_time = task_end_time
            
        return Response(DailyPlanSerializer(daily_plan).data)


class DailyPlanTaskViewSet(viewsets.ModelViewSet):
    queryset = DailyPlanTask.objects.all()
    serializer_class = DailyPlanTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class MonthlyPlanViewSet(viewsets.ModelViewSet):
    queryset = MonthlyPlan.objects.all()
    serializer_class = MonthlyPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MonthlyPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def generate(self, request):
        month = request.data.get('month', timezone.now().month)
        year = request.data.get('year', timezone.now().year)

        try:
            month = int(month)
            year = int(year)
            if month < 1 or month > 12:
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid month or year."}, status=status.HTTP_400_BAD_REQUEST)

        monthly_plan, created = MonthlyPlan.objects.get_or_create(
            user=request.user,
            month=month,
            year=year
        )

        # Get the number of days in the month
        _, days_in_month = monthrange(year, month)

        # Generate or update daily plans for each day of the month
        daily_plans = []
        for day in range(1, days_in_month + 1):
            plan_date = date(year, month, day)
            daily_plan, _ = DailyPlan.objects.get_or_create(
                user=request.user,
                date=plan_date
            )
            daily_plans.append(DailyPlanSerializer(daily_plan).data)

        # You might want to add a field to MonthlyPlan to store or reference these daily plans
        # For now, we'll just return them in the response

        response_data = MonthlyPlanSerializer(monthly_plan).data
        response_data['daily_plans'] = daily_plans

        return Response(response_data)
