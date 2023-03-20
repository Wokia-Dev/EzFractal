
# Ez Fractal



<p align="center">
<img src="https://raw.githubusercontent.com/Wokia-Dev/EzFractal/master/Resources/Images/icon.png" width="200" height="200" />
</p>

<p align="center"><strong>Ez Fractal</strong> est un petit logiciel qui permet d'explorer l'ensemble de Julia et l'ensemble de Mandelbrot. Ez Fractal est développé en Python avec la bibliothèque <a href="https://github.com/Wokia-Dev/EZ">EZ</a>.</p>

> ###### _Chose language: [[ fr ]](https://github.com/Wokia-Dev/EzFractal/) [[ en ]](README_en.md)_

## Installation

Cloner le projet

```bash
  git clone https://github.com/Wokia-Dev/EzFractal.git
```

Aller dans le dossier du projet

```bash
  cd EzFractal
```

Installer les dépendances

```bash
  pip install -r requirements.txt
```

Lancer l'application

```bash
  python main.py
```



## Paramètre

**Contrôle par défaut :**

<kbd>↑</kbd> , <kbd>↓</kbd> , <kbd>→</kbd> , <kbd>←</kbd> : se déplacer dans la fractal

```scroll up/down``` : zoomer dézoomer

<kbd>r</kbd> : réinitialiser la fractal

<kbd>Crtl</kbd> + <kbd>s</kbd> : exporter la fractal

<kbd>Echap</kbd> : quitter l'application

<br>

**Changer les paramètres :**

Vous pouvez changer les paramètres en modifiant le fichier ```CONFIG.ini``` depuis l'explorateur ou en cliquant sur le buton paramètre de l'application.

## Capture d'écran

![App Screenshot](https://user-images.githubusercontent.com/85500189/226345033-d998732a-c7f4-46a2-8146-f8ed29a126b8.png)



## Demo

https://user-images.githubusercontent.com/85500189/223299008-b944ae4b-0137-46fa-a1ea-cda749b4de61.mp4


## Optimisation

- Pour afficher la fractal un tableau [numpy](https://numpy.org/) 3 dimension est utiliser qui représente chaque pixel de la fenêtre avec les valeurs RGB. Les fonctions qui génèrent les fractals opèrent directement sur ce tableau. On met à jour la fenêtre seulement quand la fractal a fini d'être généré pour cela un utilise la fonction pygame ```pygame.surfarray.blit_array``` pour changer tous les pixels en une seule fois.

- Afin d'optimiser les performances, les fonctions qui génèrent les fractals sont compilées à l'aide de la bibliothèque [numba](https://numba.pydata.org/).


## Références

- [EZ](https://github.com/Wokia-Dev/EZ)
- [numpy](https://github.com/numpy/numpy)
- [numba](https://github.com/numba/numba)
- [pygame](https://github.com/pygame/pygame)
