from django.shortcuts import render
from rest_framework.decorators import action, permission_classes
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitCreateSerializer, HabitShowSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticated


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        permission_classes(IsAuthenticated)
        new_habit = serializer.save()
        user = User.objects.get(email=self.request.user.email)
        new_habit.owner = user
        new_habit.save()

    # def perform_update(self, serializer):
    #     update_habit = serializer.save
    #     update_habit.save()

    def list(self, request, *args, **kwargs):
        queryset = Habit.objects.filter(owner=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return HabitCreateSerializer
        elif self.action in ['retrieve', 'list', 'public']:
            return HabitShowSerializer

    @action(detail=False, name='public')
    def public(self, request):
        permission_classes(IsAuthenticated)
        queryset = Habit.objects.filter(is_public=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
