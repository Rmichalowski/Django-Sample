from django.urls import path
from aplikacja import views
from django.contrib import admin

urlpatterns = [
    path('',views.index),

    path('lista_rzeczy/', views.lista_rzeczy),

    path('pomieszczenia/', views.pomieszczenia),

    path('pomieszczenia/<int:id>', views.polki_w_pomieszczeniu),

    path('rzeczynapolce/<int:id>', views.rzeczy_na_polce),

    path('widok/', views.widok),

    path('widok/<int:id>', views.widok_obraz),

    path('lodowka/', views.lodowka),

    path('lodowka/<int:id>', views.produkty_w_lodowce),

    path('wyszukiwanie_rzeczy', views.wyszukiwanie_rzeczy, name='wyszukiwanie_rzeczy'),

    path('lodowka_wyszukiwanie', views.lodowka_wyszukiwanie, name='lodowka_wyszukiwanie'),

    path('pomieszczenie_wyszukiwanie', views.pomieszczenie_wyszukiwanie, name='pomieszczenie_wyszukiwanie'),
   ]