from django.urls import path, include
from rest_framework import routers

from habits.apps import HabitsConfig
from habits.views import HabitViewSet

app_name = HabitsConfig.name

router = routers.DefaultRouter()
router.register(r'', HabitViewSet)

urlpatterns = [
    path('', include(router.urls))
    ]
