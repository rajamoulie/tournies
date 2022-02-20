from dataclasses import fields
from django.forms import ModelForm
from .models import Tourney
from django.contrib.auth.models import User


class TourneyForm(ModelForm) :
    class Meta :
        model = Tourney
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm) :
    class Meta :
        model = User
        fields = ['username', 'email']