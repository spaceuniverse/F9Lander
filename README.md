______________________________________________

###F9Lander

Simple 2d simulation of Falcon 9 rocket landing on an ocean platform.

______________________________________________

###Requirements:

0. **python 2.7**
https://www.python.org/downloads/

1. **pygame**
http://www.pygame.org/download.shtml

    installation of pygame with anaconda:

    http://stackoverflow.com/questions/19636480/installation-of-pygame-with-anaconda

    the easiest way to install using conda is:

    ```bash
    $ conda install -c https://conda.binstar.org/krisvanneste pygame

    or

    $ conda install -c https://conda.anaconda.org/kne pygame
    ```

2. **pybox2d**
https://github.com/pybox2d/pybox2d

    to install using conda:

    ```bash
    $ conda install -c https://conda.anaconda.org/kne pybox2d
    ```

3. **numpy**
http://www.scipy.org/scipylib/download.html

    to install using conda:

    ```bash
    $ conda install numpy
    ```

n. **common sense**

p.s. conda (not necessary | only if you choose conda way of packages installation)

http://conda.pydata.org/miniconda.html

______________________________________________

###Demo:

https://youtu.be/wCqZF0uTbKY

______________________________________________

###Controls:

You can control rocket manually through keyboard or using external script through socket.

####Keyboard mode

**w** - main engine;

**a** - left engine;

**d** - right engine;

**n, space** - restart game (new rocket) | SPACE will work even in "socket" control mode;

You can find more information about controls in **help.pdf**

####Socket mode

The `F9GameClient` class is a simple wraper to help you control rocket through the socket. See `F9utils.py` for more details.

______________________________________________

###Command line options:

By default the game will run in "keyboard" mode. To run it in the "socket" mode start the server script with the following options:

```bash
$ python F9LanderCORE.py -s
```

Then run in second console:

```bash
$ python F9LanderClientCORE.py
```

`F9LanderClientCORE.py` is a client which sends commands to the server, you can modify it if you are familiar with python. It represents the Python API.

You can modify the socket address and port by running the server with the following options:

```bash
$ python F9LanderCORE.py -i 127.0.0.1 -p 50007
```
______________________________________________

###Files:

`F9LanderCORE.py` - main class | server |

`F9LanderClientCORE.py` - external control script | client | Python API |

`./experiments` - folder with experimental scripts

`./res` - folder with resources

**^_^**
______________________________________________
