from rest_framework.exceptions import ValidationError

from habits.models import Habit


class HabitValidator:

    def __init__(self, is_nice_habit, related_habit, period, time_to_complete, prize):
        self.is_nice_habit = is_nice_habit
        self.related_habit = related_habit
        self.prize = prize
        self.period = period
        self.time_to_complete = time_to_complete

    def __call__(self, value):
        is_nice_habit = dict(value).get(self.is_nice_habit)
        related_habit = dict(value).get(self.related_habit)
        prize = dict(value).get(self.prize)
        period = dict(value).get(self.period)
        time_to_complete = dict(value).get(self.time_to_complete)

        if not is_nice_habit:
            if not related_habit and not prize:
                raise ValidationError('Для полезной привычки нужно указать связаную привычку или вознаграждение')
            elif related_habit and prize:
                raise ValidationError('Для полезной привычки нужно указать связаную привычку ИЛИ вознаграждение')
            elif related_habit:
                # habit = Habit.objects.get(pk=related_habit)
                if not related_habit.is_nice_habit:
                    raise ValidationError('В связанные привычки могут попадать только приятные привычки')
        elif is_nice_habit:
            if related_habit or prize:
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
        if time_to_complete > 120:
            raise ValidationError('Время выполнения должно быть не больше 120 секунд')
