from habit_tracker.models import Habit
from habit_tracker.paginations import CastomPagination
from habit_tracker.serializers import HabitSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCreator



class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer

class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = CastomPagination

    def get_queryset(self):
        # Получаем привычки текущего пользователя
        user_habits = Habit.objects.filter(creator=self.request.user)
        # Получаем публичные привычки других пользователей
        public_habits = Habit.objects.filter(
            publicity_indicator=True
        ).exclude(
            creator=self.request.user  # Исключаем привычки текущего пользователя
        )
        # Объединяем два QuerySet
        return user_habits.union(public_habits)

class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCreator]
        return super().get_permissions()

class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCreator]
        return super().get_permissions()
