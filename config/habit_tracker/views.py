from habit_tracker.models import Habit
from habit_tracker.paginations import CastomPagination
from habit_tracker.serializers import HabitSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated



class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer

class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = CastomPagination

class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
