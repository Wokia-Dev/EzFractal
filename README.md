
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


## Optimization

- To display the fractal, a 3-dimensional [numpy](https://numpy.org/) array is used to represent each pixel of the window with RGB values. The functions that generate the fractals operate directly on this array. The window is updated only when the fractal has finished being generated, and for this, the pygame function ```pygame.surfarray.blit_array``` is used to change all pixels at once.

- To optimize performance, the functions that generate the fractals are compiled using the [numba](https://numba.pydata.org/) library.


## References

- [EZ](https://github.com/Wokia-Dev/EZ)
- [numpy](https://github.com/numpy/numpy)
- [numba](https://github.com/numba/numba)
- [pygame](https://github.com/pygame/pygame)
