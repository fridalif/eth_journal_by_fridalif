import django.forms as forms
from .models import Profile


class ImageForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput({'id': "image_form"}), label='')

    class Meta:
        model = Profile
        fields = ('avatar',)
