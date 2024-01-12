from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from habits.apps import HabitsConfig
# from users.views import UserCreateAPIView, UserListAPIView, UserUpdateAPIView,
from users.views import UserViewSet

app_name = HabitsConfig.name

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    # user
    path('', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]