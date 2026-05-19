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


    def clean(self):
        cleaned_data = super().clean()

        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if not username or not email:
            return cleaned_data
        

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            raise forms.ValidationError("User not found. Please invite the user via invitation system.")

        
        if user.email.lower() != email.lower():
            raise forms.ValidationError('Email does not match this username,')


        if WorkspaceMember.objects.filter(
            workspace = self.workspace,
            members = user,

        ).exists():
            raise forms.ValidationError('This user is already a member of this workspace.')

        self.cleaned_data['user_instance'] = user
        
        
        return cleaned_data
    
        


class UpdateMemberForm(forms.ModelForm):

    class Meta:
        model = WorkspaceMember
        fields = ('members', 'role')

