from django import forms
from .models import Task
from django.utils import timezone


class TaskForm(forms.ModelForm):
    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'priority-select'})
    )
    created_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'task-datetime'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=True
    )
    
    class Meta:
        model = Task
        fields = ['title', 'priority', 'created_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'task-input', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format initial datetime value for datetime-local input
        if self.instance and getattr(self.instance, 'created_at', None):
            self.initial['created_at'] = self.instance.created_at.strftime('%Y-%m-%dT%H:%M')
