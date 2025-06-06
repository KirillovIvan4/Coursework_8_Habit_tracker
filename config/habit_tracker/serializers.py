from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import  get_object_or_404
from rest_framework.response import Response


from users.serializers import UserSerializer

from habit_tracker.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


# class LessonSerializer(serializers.ModelSerializer):
#     link_video = serializers.URLField(validators=[validate_youtube_link])
#     class Meta:
#         model = Lesson
#         fields = '__all__'
#
#
# class CourseSerializer(serializers.ModelSerializer):
#     lessons = LessonSerializer(many=True, read_only=True)  # Пример для lessons
#     creator = UserSerializer(read_only=True)
#     last_lesson = serializers.SerializerMethodField()
#
#     subscription = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Course
#         fields = '__all__'
#     def get_subscription(self, instance):
#         pass
#
#
#     def get_last_lesson(self, instance):
#         if instance.lesson.all():
#             return instance.lesson.all().count()
#         return 0
#
#
#
#
# class PaymentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payments
#         fields = '__all__'
#
#
# class SubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = '__all__'
#
