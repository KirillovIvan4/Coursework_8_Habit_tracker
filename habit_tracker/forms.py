from django import forms


class HabitForm(forms.Form):
    days = forms.MultipleChoiceField(
        choices=[
         ('mon', 'Понедельник'),
         ('tue', 'Вторник'),
         ('wed', 'Среда'),
         ('thu', 'Четверг'),
         ('fri', 'Пятница'),
         ('sat', 'Суббота'),
         ('sun', 'Воскресенье'),

        ],
        widget=forms.CheckboxSelectMultiple,
        initial=['mon',]
    )
