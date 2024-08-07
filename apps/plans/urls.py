from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyPlanViewSet, MonthlyPlanViewSet, DailyPlanTaskViewSet
from .calendar_views import CalendarEventsView

router = DefaultRouter()
router.register(r'daily-plans', DailyPlanViewSet)
router.register(r'daily-plan-tasks', DailyPlanTaskViewSet)

urlpatterns = [
    path('calendar-events/', CalendarEventsView.as_view(), name='calendar-events'),
    path('', include(router.urls)),
    # ... other URL patterns ...
]