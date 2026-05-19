from django import forms
from django.contrib.auth import get_user_model
from .models import WorkspaceInvitation




User = get_user_model()

class InviteMemberForm(forms.ModelForm):

    class Meta:
        model = WorkspaceInvitation
        fields = ('email', 'role')


    def __init__(self, *args, **kwargs):
        self.workspace = kwargs.pop('workspace')
        super().__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This user already exists. User the "Add Member" form insted.')
        return email
    

