from django import forms
from django.contrib.auth import get_user_model

from .models import WorkspaceMember, Workspace


User = get_user_model()



class AddMemberForm(forms.ModelForm):

    user = forms.ModelChoiceField(queryset=User.objects.all())


    class Meta:
        model = WorkspaceMember
        fields = ['members', 'role']
