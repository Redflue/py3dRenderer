# py3dRenderer
By Redflue

---
This project was made for educational purposes; I wanted to learn about 3d rendering and shaders. This is not reprensentative of my usual programming style as I wanted to make this quickly to test if it would work.

## Controls
```WASD``` To move.

```Space / LCtrl``` to change height.

```T/G``` to change Focal Length, ```R``` to reset it.

```Keyboard Arrows``` to rotate the view when the camera is unlocked, otherwise use you mouse like in any 3d first person game to rotate your view.

```Tab``` to lock or unlock the mouse from the screen.

```1``` or ```2``` to change the rendering mode between Colored and Depthmap.

## Dependencies
The project was made using:
- ```python 3.10``` or higher (as long as its compactible)
- ```pygame 2.5.2``` or higher (as long as its also compatible)
- ```compushady``` (for compute shaders)

## Requirements
Because of the nature of python and because of how **compushady** works, there are some harware and software requirements.
- A good computer, otherwise the fps will drop
- A discrete GPU, this is a requirement for compushady.
- Vulkan drivers, once again, a compushady requirement
