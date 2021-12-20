from django.forms import ModelForm
from .models import Person, Trophy, League, Club, Manager, Player, Midfielder, Forward

class TrophyForm(ModelForm):
    class Meta:
        model = Trophy
        fields = ['name', 'date_won']

class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ['name', 'country']

class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ['name']

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'surname']

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'surname']

class ManagerForm(ModelForm):
    class Meta:
        model = Manager
        fields = ['name', 'surname']
