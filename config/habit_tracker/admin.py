from django.contrib import admin

from habit_tracker.models import Habit, Days


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'place', 'time', 'action',)
    list_filter = ('place', 'time', 'action',)
    search_fields = ('place', 'time', 'action',)

@admin.register(Days)
class DaysAdmin(admin.ModelAdmin):
    list_display = ('pk', 'days', )
    list_filter = ('days', )
    search_fields = ('days',)