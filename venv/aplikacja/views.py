from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .formularze import *
from django.shortcuts import get_object_or_404, redirect
from .urls import *
from datetime import datetime
from django.views.generic.edit import FormView
import datetime

import numpy as np
import skimage
import imageio
from PIL import Image
from PIL import ImageDraw
from os.path import exists
import matplotlib.pyplot as plt
import matplotlib.image
from PIL import ImageFont
import time

def index(response):
    return render(response, "index.html")

def lista_rzeczy(request):
    formularz_dodaj = Lista_RzeczyForm(request.POST or None, request.FILES or None)
    wszystkie = Rzecz.objects.all()

    if formularz_dodaj.is_valid():
        formularz_dodaj.save()
        return redirect(lista_rzeczy)

    if request.method == "POST":
        usun = request.POST.getlist('usun')
        Rzecz.objects.filter(pk__in=usun).delete()
        formularz_dodaj = Lista_RzeczyForm(None)
    return render(request, 'lista_rzeczy.html',{'form':formularz_dodaj, 'Lista_Rzeczy_all':wszystkie})

def lodowka(request):
    formularz_dodaj = LodówkaForm(request.POST or None, request.FILES or None)
    formularz2 = ProduktForm(request.POST or None, request.FILES or None)
    wszystkie = Lodówka.objects.all().prefetch_related("produkty")


    if formularz_dodaj.is_valid():
        formularz_dodaj.save()
        return redirect(lodowka)

    if formularz2.is_valid():
        formularz2.save()
        return redirect(lodowka)

    if request.method == "POST":
        usun = request.POST.getlist('usun')
        Lodówka.objects.filter(pk__in=usun).delete()
        formularz_dodaj = LodówkaForm(None)
        formularz2 = ProduktForm(None)
    return render(request, 'lodowka.html' , {'form':formularz_dodaj,'form2':formularz2, 'Lodówka_all':wszystkie})



def produkty_w_lodowce(request,id):
    formularz_dodaj = ProduktForm(request.POST or None, request.FILES or None)
    wszystkie = Produkt.objects.filter(lodówka_id=id)
    actual = Lodówka.objects.get(pk=id)

    if formularz_dodaj.is_valid():
        formularz_dodaj.lodówka = actual
        formularz_dodaj.save()


    if request.method == "POST":
        usun = request.POST.getlist('usun')
        Produkt.objects.filter(pk__in=usun).delete()
        formularz_dodaj = ProduktForm(None)
    return render(request,'produkty_w_lodowce.html' , {'form':formularz_dodaj,'Produkty_all':wszystkie, 'aktualna_lodowka':actual})



def produkt(response):
    produkt = Produkt.objects.all()
    return render(response, "lodowka.html", {'produkt': produkt})


def pomieszczenia(request):
    formularz_dodaj = PomieszczenieForm(request.POST or None, request.FILES or None)
    formularz2 = PomieszczenieForm(request.POST or None, request.FILES or None)
    wszystkie = Pomieszczenie.objects.all().prefetch_related("polki")

    if formularz_dodaj.is_valid():
        formularz_dodaj.save()
        return redirect(pomieszczenia)

    if formularz2.is_valid():
        formularz2.save()
        return redirect(pomieszczenia)

    if request.method == "POST":
        usun = request.POST.getlist('usun')
        Pomieszczenie.objects.filter(pk__in=usun).delete()
        formularz_dodaj = PomieszczenieForm(None)
        formularz2 = PomieszczenieForm(None)
    return render(request, 'pomieszczenia.html',{'form':formularz_dodaj, 'form2':formularz2, 'Pomieszczenie_all':wszystkie})

def polki_w_pomieszczeniu(request,id):
    formularz_dodaj = PółkaForm(request.POST or None, request.FILES or None)
    wszystkie = Półka.objects.filter(pomieszczenie_id=id)
    actual = Pomieszczenie.objects.get(pk=id)

    if formularz_dodaj.is_valid():
        formularz_dodaj.pomieszczenia = actual
        formularz_dodaj.save()
        y = int(formularz_dodaj.data["y"])
        x = int(formularz_dodaj.data["x"])
        b = int(formularz_dodaj.data["b"])
        a = int(formularz_dodaj.data["a"])
        nazwa = formularz_dodaj.data["nazwa"]
        RysujProstokat(y, x, b, a, nazwa, id)


    if request.method == "POST":
        usun = request.POST.getlist('usun')
        Półka.objects.filter(pk__in=usun).delete()
        formularz_dodaj = PółkaForm(None)
    return render(request,'polki_w_pomieszczeniu.html' , {'form':formularz_dodaj,'Polki_all':wszystkie, 'aktualne_pomieszczenie':actual})

def rzeczy_na_polce(request,id):
    formularz_dodaj = RzeczForm(request.POST or None, request.FILES or None)
    wszystkie = Rzecz.objects.filter(półka_id=id)
    actual = Półka.objects.get(pk=id)

    if formularz_dodaj.is_valid():
        formularz_dodaj.Półka_id = actual
        formularz_dodaj.save()

    if request.method == "POST":
        usun = request.POST.getlist('usun')
        Rzecz.objects.filter(pk__in=usun).delete()
        formularz_dodaj = RzeczForm(None)
    return render(request,'rzeczy_na_półce.html' , {'form':formularz_dodaj, 'rzeczy_all':wszystkie, 'aktualna_półka':actual} )


def polka(response):
    polka = Półka.objects.all()
    return render(response, "pomieszczenia.html", {'polka': polka})

def widok(response):
    wszystkie = Pomieszczenie.objects.all()
    return render(response, "widok.html", {'pomieszczenia_all':wszystkie})

def widok_obraz(request,id):
    formularz_edit = PółkaForm(request.POST or None, request.FILES or None)

    wszystkie = Półka.objects.filter(pomieszczenie_id=id)
    actual = Pomieszczenie.objects.get(pk=id)

    if formularz_edit.is_valid():
        formularz_edit.pomieszczenia = actual
        formularz_edit.save()

    # Program Rysowanie.py
    if request.method == "POST":
        y =int (formularz_edit.data["y"])
        x =int(formularz_edit.data["x"])
        b =int(formularz_edit.data["b"])
        a =int(formularz_edit.data["a"])
        nazwa = formularz_edit.data["nazwa"]
        RysujProstokat(y,x,b,a,nazwa,id)
    #
    return render(request, 'widok_obraz.html', {'widok_obraz': id, 'form':formularz_edit, 'aktualne_pomieszczenie':actual})

# funkcje z programu ###################################################################################################
def LoadOrCreateObraz(nazwa_obrazu):
    global sciezka_pliku
    sciezka_pliku = "aplikacja/static/image/" + str(nazwa_obrazu) + ".jpg"
    if exists(sciezka_pliku):
        print("Reading image...")
        obraz = imageio.imread(sciezka_pliku)
        np.array(obraz)
        print(obraz.shape)
        return obraz
    else:
        print("Creating image...")
        obraz = 255 * np.ones((720, 1280, 3), np.uint8)
        np.array(obraz)
        print(obraz.shape)
        imageio.imwrite(sciezka_pliku, obraz)
        return obraz

def RysujProstokat( y,  x,  b,  a, opis,nazwa):
    global obraz
    #print(y,x,b,a,opis,nazwa)
    label = opis
    obraz2 = LoadOrCreateObraz(nazwa)

    sciezka_pliku = "aplikacja/static/image/" + str(nazwa) + ".jpg"
    for i in range(x,x+a):
        obraz2[y,i] = 0
        obraz2[y+b,i] = 0

    for i in range(y,y+b):
        obraz2[i,x] = 0
        obraz2[i,x+a] = 0

    imageio.imwrite(sciezka_pliku, obraz2)

    obraz2 = Image.open(sciezka_pliku)
    mojFont = ImageFont.truetype("arial.ttf",20)
    obrazTemp = ImageDraw.Draw(obraz2)
    obrazTemp.text((x+5,y+5),label,font=mojFont, fill=(0,0,0))
    obraz2.save(sciezka_pliku)
    obraz = imageio.imread(sciezka_pliku)
########################################################################################################################
def wyszukiwanie_rzeczy(request):
    if request.method == "POST":
        wyszukiwanie = request.POST['wyszukiwanie']
        rzeczy = Rzecz.objects.filter(nazwa__contains=wyszukiwanie)
        return render(request, 'lista_rzeczy_wyszukiwanie.html', {'wyszukiwanie':wyszukiwanie, 'rzeczy':rzeczy})
    else:
        return render(request, 'lista_rzeczy_wyszukiwanie.html',{})

def lodowka_wyszukiwanie(request):
    if request.method == "POST":
        wyszukiwanie = request.POST['wyszukiwanie']
        lodowka = Lodówka.objects.filter(nazwa__contains=wyszukiwanie)
        return render(request, 'lodowka_wyszukiwanie.html', {'wyszukiwanie':wyszukiwanie, 'lodowka':lodowka})
    else:
        return render(request, 'lodowka_wyszukiwanie.html',{})


def pomieszczenie_wyszukiwanie(request):
    formularz_dodaj = PomieszczenieForm(request.POST or None, request.FILES or None)
    formularz2 = PomieszczenieForm(request.POST or None, request.FILES or None)
    wszystkie = Pomieszczenie.objects.all().prefetch_related("polki")

    if formularz_dodaj.is_valid():
        formularz_dodaj.save()
        return redirect(pomieszczenia)

    if formularz2.is_valid():
        formularz2.save()
        return redirect(pomieszczenia)

    if request.method == "POST":
        usun = request.POST.getlist('usun')
        Pomieszczenie.objects.filter(pk__in=usun).delete()
        formularz_dodaj = PomieszczenieForm(None)
        formularz2 = PomieszczenieForm(None)
        wyszukiwanie = request.POST['wyszukiwanie']
        pomieszczenie = Pomieszczenie.objects.filter(nazwa__contains=wyszukiwanie)
        return render(request, 'pomieszczenie_wyszukiwanie.html', {'form': formularz_dodaj, 'form2': formularz2,'wyszukiwanie': wyszukiwanie, 'pomieszczenie': pomieszczenie})
    else:
        return render(request, 'pomieszczenie_wyszukiwanie.html', {})
