from django import forms

from web.models import Audio, User


class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ('audio', 'speaker_num', 'language', 'model')

class UserCreationForm(forms.ModelForm):
    class Meta:
        model= User
        fields=('username','password')