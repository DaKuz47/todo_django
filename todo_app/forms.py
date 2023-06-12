from django import forms

from .models import List, Task


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name']
        labels = {'name': 'Название'}


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']
        labels = {'name': 'Название', 'descriptioin': 'Описание'}
