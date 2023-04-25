
# Ez Fractal



<p align="center">
<img src="https://raw.githubusercontent.com/Wokia-Dev/EzFractal/master/Resources/Images/icon.png" width="200" height="200" />
</p>

<p align="center"><strong>Ez Fractal</strong> est un petit logiciel qui permet d'explorer l'ensemble de Julia et l'ensemble de Mandelbrot. Ez Fractal est développé en Python avec la bibliothèque <a href="https://github.com/Wokia-Dev/EZ">EZ</a>.</p>

> ###### _Chose language: [[ en ]](https://github.com/Wokia-Dev/EzFractal/) [[ fr ]](README_fr.md)_

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


<details>
<summary><h2>Qu'est-ce que les fractals ?</h2></summary>


### Définition
Les fractales sont des objets mathématiques qui ont la propriété d'être auto-similaires, c'est-à-dire que leur structure est répétée à différentes échelles. En d'autres termes, si l'on zoome sur une partie d'une fractale, on peut voir des motifs similaires à ceux observés à une plus grande échelle.


---

<details>
<summary><h3>Ensemble de Mandelbrot</h3></summary>

### Définition
L'ensemble de Mandelbrot est une fractale définie comme l'ensemble des points c dans le plan complexe pour lesquels la suite des nombres complexes obtenue en itérant la fonction quadratique $f(z) = z^2 + c$ ne diverge pas vers l'infini. Autrement dit, si on part d'un point c et qu'on calcule de manière répétée sa valeur en appliquant la fonction $f(z)$, soit $f(c)$, $f(f(c))$, $f(f(f(c)))...$ et ainsi de suite, alors soit cette suite de nombres complexes reste bornée, soit elle tend vers l'infini. Les points c pour lesquels la suite reste bornée appartiennent à l'ensemble de Mandelbrot, tandis que les points pour lesquels la suite tend vers l'infini n'appartiennent pas à l'ensemble.

---

<br>

### Algorithme de génération
```
Pour chaque pixel (x, y) dans l'image de sortie :
    Convertir les coordonnées du pixel en nombres complexes c
    Initialiser z = 0
    Pour chaque itération jusqu'à un nombre maximal défini :
        Si |z| > 2, quitter la boucle d'itération
        Mettre à jour z en appliquant la fonction f(z) = z^2 + c
    Calculer une valeur de couleur en fonction du nombre d'itérations effectuées
    Définir la couleur du pixel (x, y) dans l'image de sortie en fonction de la valeur de couleur calculée
```

<br>

### Implémentation python

#### Fonction qui calcule la couleur de chaque pixel de l'écran en fonction des paramètres donnés. La fonction modifie directement tout le tableau qui représente l'écran.
```python
@numba.njit(fastmath=True, parallel=True)
def render_mandelbrot(
        screen_array: np.array,
        max_iter: int,
        zoom: float,
        offset: np.array,
        width: int,
        height: int,
        menu_width: int = 0,
        saturation: float = 0.8,
        lightness: float = 0.5,
):
    # foreach pixel in the screen array using numba parallel
    for x in numba.prange(width - menu_width):
        for y in numba.prange(height):
            # define the complex number based on the pixel coordinates, zoom and offset
            c = (x - offset[0]) * zoom + 1j * (y - offset[1]) * zoom
            # define the initial value of z and the number of iterations
            z = 0
            num_iter = 0
            # iterate the function until the number is diverging or the max iterations is reached
            for i in range(max_iter):
                # julia set formula
                z = z ** 2 + c
                if z.real ** 2 + z.imag ** 2 > 4:
                    # if the number is diverging break the loop
                    break
                num_iter += 1

            # define the color based on the number of iterations and set the pixel color in the screen array
            screen_array[x, y] = iter_gradient_generator(
                num_iter, max_iter, saturation, lightness
            )
            # return the screen array
    return screen_array
```

<br>

#### Fonction qui génère la couleur d'un pixel en fonction du nombre d'itérations effectuées et du nombre d'itérations maximum.
```python
@numba.njit(fastmath=True)
def iter_gradient_generator(
    num_iter: int, max_iter: int, saturation: float = 0.8, lightness: float = 0.5
) -> list[int]:
    if num_iter == max_iter:
        return [0, 0, 0]
    else:
        h = num_iter / max_iter
        c = (1 - np.abs(2 * lightness - 1)) * saturation
        x = c * (1 - np.abs((h * 6) % 2 - 1))
        m = lightness - c / 2
        if 0 <= h < 1 / 6:
            r, g, b = c + m, x + m, m
        elif 1 / 6 <= h < 1 / 3:
            r, g, b = x + m, c + m, m
        elif 1 / 3 <= h < 1 / 2:
            r, g, b = m, c + m, x + m
        elif 1 / 2 <= h < 2 / 3:
            r, g, b = m, x + m, c + m
        elif 2 / 3 <= h < 5 / 6:
            r, g, b = x + m, m, c + m
        else:
            r, g, b = c + m, m, x + m
    return [int(r * 255), int(g * 255), int(b * 255)]
```

</details>

<details>
<summary><h3>Ensemble de Julia</h3></summary>

### Définition
L'ensemble de Julia est une autre famille de fractales, également définie en termes de suites de nombres complexes itératives. Contrairement à l'ensemble de Mandelbrot, l'ensemble de Julia est défini pour un point fixe de départ, plutôt que pour tous les points du plan complexe. Pour un nombre complexe donné, appelé constante de Julia, on itère une fonction complexe $f(z)$ qui prend en entrée un autre nombre complexe, en utilisant une suite itérative de la forme $z$, $f(z)$, $f(f(z))$, $f(f(f(z)))...$ et ainsi de suite. Si cette suite de nombres complexes diverge vers l'infini, le point de départ n'appartient pas à l'ensemble de Julia pour cette constante de Julia. Si la suite reste bornée, le point de départ appartient à l'ensemble de Julia. 

---

<br>

### Algorithme de génération
```
Définir la constante de Julia complexe c
Définir les dimensions de l'image de sortie, représentant l'ensemble de Julia
Pour chaque pixel (x, y) dans l'image de sortie :
    Convertir les coordonnées du pixel en nombre complexe z = x + yi
    Pour chaque itération jusqu'à un nombre maximal défini :
        Si |z| > 2, quitter la boucle d'itération
        Mettre à jour z en appliquant la fonction f(z) = z^2 + c
    Calculer une valeur de couleur en fonction du nombre d'itérations effectuées
    Définir la couleur du pixel (x, y) dans l'image de sortie en fonction de la valeur de couleur calculée
```

<br>

### Implémentation python

#### Fonction qui calcule la couleur de chaque pixel de l'écran en fonction des paramètres donnés. La fonction modifie directement tout le tableau qui représente l'écran.
```python
@numba.njit(fastmath=True, parallel=True)
def render_julia(
    screen_array: np.array,
    c: complex,
    max_iter: int,
    zoom: float,
    offset: np.array,
    width: int,
    height: int,
    menu_width: int = 0,
    saturation: float = 0.8,
    lightness: float = 0.5,
):
    # foreach pixel in the screen array using numba parallel
    for x in numba.prange(width - menu_width):
        for y in numba.prange(height):
            # define the complex number based on the pixel coordinates, zoom and offset
            z = (x - offset[0]) * zoom + 1j * (y - offset[1]) * zoom
            # number of iterations
            num_iter = 0

            # iterate the function until the number is diverging or the max iterations is reached
            for i in range(max_iter):
                # julia set formula
                z = z**2 + c
                if z.real**2 + z.imag**2 > 4:
                    # exit the loop if the number is diverging
                    break
                num_iter += 1

            # define the color based on the number of iterations and set the pixel color in the screen array
            screen_array[x, y] = iter_gradient_generator(
                num_iter, max_iter, saturation, lightness
            )
    # return the screen array
    return screen_array
```

<br>

#### Fonction qui génère la couleur d'un pixel en fonction du nombre d'itérations effectuées et du nombre d'itérations maximum.

```python
@numba.njit(fastmath=True)
def iter_gradient_generator(
    num_iter: int, max_iter: int, saturation: float = 0.8, lightness: float = 0.5
) -> list[int]:
    if num_iter == max_iter:
        return [0, 0, 0]
    else:
        h = num_iter / max_iter
        c = (1 - np.abs(2 * lightness - 1)) * saturation
        x = c * (1 - np.abs((h * 6) % 2 - 1))
        m = lightness - c / 2
        if 0 <= h < 1 / 6:
            r, g, b = c + m, x + m, m
        elif 1 / 6 <= h < 1 / 3:
            r, g, b = x + m, c + m, m
        elif 1 / 3 <= h < 1 / 2:
            r, g, b = m, c + m, x + m
        elif 1 / 2 <= h < 2 / 3:
            r, g, b = m, x + m, c + m
        elif 2 / 3 <= h < 5 / 6:
            r, g, b = x + m, m, c + m
        else:
            r, g, b = c + m, m, x + m
    return [int(r * 255), int(g * 255), int(b * 255)]
```

</details>


</details>

## Optimisation

- Pour afficher la fractal un tableau [numpy](https://numpy.org/) 3 dimension est utiliser qui représente chaque pixel de la fenêtre avec les valeurs RGB. Les fonctions qui génèrent les fractals opèrent directement sur ce tableau. On met à jour la fenêtre seulement quand la fractal a fini d'être généré pour cela un utilise la fonction pygame ```pygame.surfarray.blit_array``` pour changer tous les pixels en une seule fois.

- Afin d'optimiser les performances, les fonctions qui génèrent les fractals sont compilées à l'aide de la bibliothèque [numba](https://numba.pydata.org/).


## Références

- [EZ](https://github.com/Wokia-Dev/EZ)
- [numpy](https://github.com/numpy/numpy)
- [numba](https://github.com/numba/numba)
- [pygame](https://github.com/pygame/pygame)
