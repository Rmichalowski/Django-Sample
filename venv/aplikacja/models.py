from django.db import models
from django.db.models.enums import TextChoices
from datetime import date

class Gabaryt(models.Model):
    nazwa = models.CharField(max_length=255)
    def __str__(self):
        return self.nazwa

class Jednostka(models.Model):
    nazwa = models.CharField(max_length=255)
    skrót = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.nazwa

class Pomieszczenie(models.Model):
    nazwa = models.CharField(max_length=255)

    def get_all_items(self):
        return self.polki.all()

    def __str__(self):
        return self.nazwa

class Półka(models.Model):
    nazwa = models.CharField(max_length=255)
    opis = models.TextField(null=True, blank=True)
    udźwig = models.DecimalField(max_digits=255, decimal_places=2, null=True)
    pomieszczenie = models.ForeignKey(Pomieszczenie, related_name='polki',on_delete=models.CASCADE, null=True)
    x = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    y = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    a = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    b = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)

    def __str__(self):
        return self.nazwa

class Rzecz(models.Model):
    nazwa = models.CharField(max_length=255)
    ilość = models.DecimalField(max_digits=255, decimal_places=0, null=True)
    waga = models.DecimalField(max_digits=255, decimal_places=2, null=True)
    gabaryt = models.ForeignKey(Gabaryt, on_delete=models.CASCADE, null=True)
    półka = models.ForeignKey(Półka, related_name='rzeczy', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nazwa +" "+ str(self.ilość) + " szt."



class Lodówka(models.Model):
    nazwa =  models.CharField(max_length=255)
    pomieszczenie = models.ForeignKey(Pomieszczenie, on_delete=models.CASCADE, null=True)

    def get_all_items(self):
        return self.produkty.all()

    def __str__(self):
        return self.nazwa

class Produkt(models.Model):
    nazwa = models.CharField(max_length=255)
    data_przydatności = models.DateField()
    ilość = models.DecimalField(max_digits=255, decimal_places=2, null=True)
    jednostka = models.ForeignKey(Jednostka, on_delete=models.CASCADE, null=True)
    lodówka = models.ForeignKey(Lodówka, related_name='produkty' ,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nazwa +" "+ str(self.ilość) +" "+ str(self.jednostka)


