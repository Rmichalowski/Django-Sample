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

def LoadOrCreateObraz(nazwa_obrazu):
    sciezka_pliku = "venv/aplikacja/static/image/" + nazwa_obrazu + ".jpg"
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



def RysujProstokat( y,  x,  b,  a, nazwa):
    global obraz
    label = "nazwa polki"
    obraz2 = LoadOrCreateObraz(nazwa)

    sciezka_pliku = "venv/aplikacja/static/image/" + nazwa + ".jpg"
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




if __name__ == "__main__":
    #obraz = LoadOrCreateObraz("obraz")
    # plt.imshow(obraz)
    # plt.show()

    RysujProstokat(500,100,130,400,"35")

    plt.imshow(obraz)
    plt.show()







