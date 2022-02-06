from django.forms import ModelForm
from django import forms
from .models import *

class PomieszczenieForm(ModelForm):
    class Meta:
       model = Pomieszczenie
       fields = ['nazwa']

class Lista_RzeczyForm(ModelForm):
    class Meta:
       model = Rzecz
       fields = ['nazwa','ilość','waga','gabaryt','półka']

class LodówkaForm(ModelForm):
    class Meta:
        model = Lodówka
        fields = ['nazwa']

class ProduktForm(ModelForm):
    class Meta:
        model = Produkt
        fields = ["nazwa","data_przydatności","ilość","jednostka","lodówka"]


class PółkaForm(ModelForm):
    class Meta:
        model = Półka
        fields = ["nazwa","opis","udźwig","pomieszczenie","x" , "y" , "a" , "b" ]

class RzeczForm(ModelForm):
    class Meta:
        model = Rzecz
        fields = ["nazwa","ilość","waga","gabaryt","półka"]

