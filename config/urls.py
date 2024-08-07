from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import CustomTokenObtainPairView, UserListCreateView, UserDetailView, ChangePasswordView, UserAvailabilityViewSet, CustomUserViewSet
from rest_framework.routers import DefaultRouter
from apps.tasks.views import TaskViewSet
from apps.plans.views import DailyPlanViewSet, MonthlyPlanViewSet
from apps.departments.views import DepartmentViewSet


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'daily-plans', DailyPlanViewSet)
router.register(r'monthly-plans', MonthlyPlanViewSet)
router.register(r'user-availability', UserAvailabilityViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/', include(router.urls)),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('apps.plans.urls')),
    #path('api/calendar-events/', CalendarEventsView.as_view(), name='calendar-events'),

]