from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()

    def perform_update(self, serializer):
        update_user = serializer.save()
        update_user.set_password(update_user.password)
        update_user.save()
