from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import WorkspaceMember


User = get_user_model()



class AddMemberForm(forms.Form):
    username = forms.CharField(max_length=255, label='Username', required=True)
    email = forms.EmailField(max_length=255, label='Email', required=True)
    role = forms.ChoiceField(choices=WorkspaceMember.Role.choices, label='Role', required=True)

    def __init__(self, *args, **kwargs):
        self.workspace = kwargs.pop('workspace')
        super().__init__(*args, **kwargs)


    def clean_username(self):

        username = self.cleaned_data['username']

        try:
            user = User.objects.filter(username=username).first()
        except User.DoesNotExist():
            raise forms.ValidationError('User not found.')
        return user
    


class UpdateMemberForm(forms.ModelForm):

    class Meta:
        model = WorkspaceMember
        fields = ('members', 'role')

