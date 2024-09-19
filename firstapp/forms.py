from django.forms import ModelForm,forms
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__'
        exclude=['host','participants']
        

