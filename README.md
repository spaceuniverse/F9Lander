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

You can control rocket manually through keyboard or using external script through socket. To change type of control you should use key '-s' for "socket" mode. Default mode is "keyboard".

```bash
$ python F9LanderCORE.py -s
```

__**"keyboard"**__

**w** - main engine;

**a** - left engine;

**d** - right engine;

**n, space** - restart game (new rocket) | SPACE will work even in "socket" control mode;

You can find more information about controls in **help.pdf**

__**"socket"**__

The `F9GameClient` class is a simple wrapper that helps you to control rocket through the socket. See `F9utils.py` for more details.

Or if you want to use pure `F9LanderPureSocketClient.py` code:

To control rocket through socket you should send the string with list of four numbers [up, left, right, new] to the socket address. Each of the numbers can be 1 or 0, which means: 1 - activate, 0 - do nothing.

For example [1, 1, 1, 0] means that all engines are working. [0, 0, 0, 1] means that you want to get a new rocket and restart.

As an output you will receive a string with list of dictionaries [{}, {}, {}] with information about every object in simulation. You can see an example of such list in F9LanderClientCORE.py

Socket address ('127.0.0.1', 50007)

Keys map [up - main engine, left - left engine, right - right engine, new - new rocket]

______________________________________________

###Command line options and how to run:

By default the game will run in "keyboard" mode.

```bash
$ python F9LanderCORE.py
```

To run it in the "socket" mode start the server script with the following options:

```bash
$ python F9LanderCORE.py -s
```

Then run in second console:

```bash
$ python F9LanderClientCORE.py
```

`F9LanderClientCORE.py` is a client which sends commands to the server, you can modify it if you are familiar with python, or write your own script in any programming language. F9LanderClientCORE represents Python API.

If you want to write your own API script:

First start the server F9LanderCORE.py and then you can send the string with list [up, left, right, new] to socket ('127.0.0.1', 50007). "up", "left", "right" and "new" can be 1 or 0.

You can modify the socket address and port by running the server with the following options:

```bash
$ python F9LanderCORE.py -i 127.0.0.1 -p 50007
```

As an output you will get a string with the list of dictionaries [{}, {}, {}] with information about every object in simulation.

______________________________________________

###Information:

__To show opened sockets in Ubuntu__

```bash
$ netstat -ntlp | grep LISTEN
```
______________________________________________

###Files:

`F9LanderCORE.py` - main class | server |

`F9LanderClientCORE.py` - external control script | client | Python API |

`F9LanderPureSocketClient.py` - external control script | client | pure socket API without wrapper |

`./experiments` - folder with experimental scripts

`./res` - folder with resources

**^_^**

______________________________________________
