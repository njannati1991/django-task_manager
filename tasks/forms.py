from django import forms
from django.contrib.auth import get_user_model
from .models import Task


User = get_user_model()

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'priority', 'assigned_to', 'due_date')


    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        if project:
            self.fields['assigned_to'].queryset = User.objects.filter(workspaces__workspace = project.workspace)