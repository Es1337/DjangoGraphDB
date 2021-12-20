from django import forms

class PersonInputForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    surname = forms.CharField(label='Surname', max_length=100)