from django.contrib import admin

from habit_tracker.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'place', 'time', 'action',)
    list_filter = ('place', 'time', 'action',)
    search_fields = ('place', 'time', 'action',)
