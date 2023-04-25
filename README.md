
# Ez Fractal



<p align="center">
<img src="https://raw.githubusercontent.com/Wokia-Dev/EzFractal/master/Resources/Images/icon.png" width="200" height="200" />
</p>

<p align="center"><strong>Ez Fractal</strong> is a small software that allows exploring the Julia and Mandelbrot set. Ez Fractal is developed in Python with the <a href="https://github.com/Wokia-Dev/EZ">EZ</a> library.</p>

> ###### _Chose language: [[ en ]](https://github.com/Wokia-Dev/EzFractal/) [[ fr ]](README_fr.md)_

## Installation

Clone the project


```bash
  git clone https://github.com/Wokia-Dev/EzFractal.git
```

Go to the project folder

```bash
  cd EzFractal
```

Install dependencies


```bash
  pip install -r requirements.txt
```

Run the application

```bash
  python main.py
```

<br>

There is also an executable version in the "Executable" folder.

## Settings

**Default Controls :**

<kbd>↑</kbd> , <kbd>↓</kbd> , <kbd>→</kbd> , <kbd>←</kbd> : Move around in the fractal

```scroll up/down``` : Zoom in/out

<kbd>r</kbd> : Reset the fractal

<kbd>Crtl</kbd> + <kbd>s</kbd> : Export the fractal

<kbd>Echap</kbd> : Quit the application

<br>

**Change Settings :**

You can change settings by modifying the ```CONFIG.ini``` file from the file explorer or by clicking on the settings button in the application.

## Screenshots

![App Screenshot](https://user-images.githubusercontent.com/85500189/226345033-d998732a-c7f4-46a2-8146-f8ed29a126b8.png)



## Demo

https://user-images.githubusercontent.com/85500189/223299008-b944ae4b-0137-46fa-a1ea-cda749b4de61.mp4

<details>
<summary><h2>What are fractals ?</h2></summary>


### Definition
Fractals are mathematical objects that have the property of being self-similar, meaning that their structure is repeated at different scales. In other words, if one zooms in on a part of a fractal, one can see patterns similar to those observed at a larger scale.

---

<details>
<summary><h3>Mandelbrot Set</h3></summary>

### Definition
The Mandelbrot set is a fractal defined as the set of points c in the complex plane for which the sequence of complex numbers obtained by iterating the quadratic function $f(z) = z^2 + c$ does not diverge to infinity. In other words, if we start with a point c and repeatedly calculate its value by applying the function $f(z)$, i.e. $f(c)$, $f(f(c))$, $f(f(f(c)))...$ and so on, then either this sequence of complex numbers remains bounded, or it tends to infinity. The points c for which the sequence remains bounded belong to the Mandelbrot set, while the points for which the sequence tends to infinity do not belong to the set.


---

<br>

### Generation algorithm
```
For each pixel (x, y) in the output image:
    Convert the pixel coordinates to corresponding complex numbers c
    Initialize z = 0
    For each iteration up to a maximum number defined:
        If |z| > 2, exit the iteration loop
        Update z by applying the function f(z) = z^2 + c
    Calculate a color value based on the number of iterations performed
    Set the color of the pixel (x, y) in the output image based on the calculated color value.
```

<br>

### Python implementation

The function that calculates the color of each pixel on the screen based on the given parameters. The function directly modifies the array that represents the screen.

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

#### A function that generates the color of a pixel based on the number of iterations performed and the maximum number of iterations.

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
<summary><h3>Julia set</h3></summary>

### Definition
The Julia set is another family of fractals, also defined in terms of iterative sequences of complex numbers. Unlike the Mandelbrot set, the Julia set is defined for a fixed starting point, rather than for all points in the complex plane. For a given complex number, called the Julia constant, a complex function f(z) is iterated using an iterative sequence of the form z, f(z), f(f(z)), f(f(f(z))), and so on. If this sequence of complex numbers diverges to infinity, the starting point does not belong to the Julia set for this Julia constant. If the sequence remains bounded, the starting point belongs to the Julia set.

---

<br>

### Generation algorithm
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

### Python implementation

#### Function that calculates the color of each pixel on the screen based on the given parameters. The function directly modifies the entire array that represents the screen.

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

#### Function that generates the color of a pixel based on the number of iterations performed and the maximum number of iterations.

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

## Optimization

- To display the fractal, a 3-dimensional [numpy](https://numpy.org/) array is used to represent each pixel of the window with RGB values. The functions that generate the fractals operate directly on this array. The window is updated only when the fractal has finished being generated, and for this, the pygame function ```pygame.surfarray.blit_array``` is used to change all pixels at once.

- To optimize performance, the functions that generate the fractals are compiled using the [numba](https://numba.pydata.org/) library.


## References

- [EZ](https://github.com/Wokia-Dev/EZ)
- [numpy](https://github.com/numpy/numpy)
- [numba](https://github.com/numba/numba)
- [pygame](https://github.com/pygame/pygame)
