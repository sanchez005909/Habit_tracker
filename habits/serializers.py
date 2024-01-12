from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import HabitValidator


class HabitCreateSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

        # fields = ['id', 'action', 'place', 'time_do_it', 'related_habit', 'prize', 'time_to_complete',
        #           'is_nice_habit', 'period']
        validators = [HabitValidator(is_nice_habit='is_nice_habit', related_habit='related_habit',
                                     period='period', time_to_complete='time_to_complete', prize='prize')]


class HabitShowSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'action', 'place', 'time', 'date', 'related_habit', 'prize', 'time_to_complete']
