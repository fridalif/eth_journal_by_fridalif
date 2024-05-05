from django.forms import ModelForm
from .models import Profile


class ImageForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)
