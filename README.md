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

3. **numpy**
http://www.scipy.org/scipylib/download.html

n. **common sense**

______________________________________________

###Demo:

https://youtu.be/wCqZF0uTbKY

______________________________________________

###Controls:

You can control rocket manually through keyboard or using external script through socket. To change type of control you should choose it in line 35 in F9LanderCORE.py

```bash
self.commands = "keyboard"   # "keyboard" "socket" | in future "fifo"
```

__**"keyboard"**__

**w** - main engine;

**a** - left engine;

**d** - right engine;

**n, space** - restart game (new rocket) | SPACE works even in external control modes;

More information about control you can find in **help.pdf**

__**"socket"**__

To control rocket through socket you should send to address the string with list with four numbers [up, left, right, new]. Each of this numbers can be 1 or 0, which means: 1 - activate, 0 - do nothing.

For example [1, 1, 1, 0] means that all engines are working. [0, 0, 0, 1] means that you want to get new rocket and restart.

As output you will get string with list of dictionaries [{}, {}, {}] with information about every object in simulation. The example of such list you can see in F9LanderClientCORE.py

Socket address ('127.0.0.1', 50007)

______________________________________________

###Information:

__To run in "keyboard" mode choose it in line 35 in F9LanderCORE.py__

Run in console:

```bash
$ python F9LanderCORE.py
```

__To run in "socket" mode choose it in line 35 in F9LanderCORE.py__

Run in first console:

```bash
$ python F9LanderCORE.py
```

Then run in second console:

```bash
$ python F9LanderClientCORE.py
```

F9LanderClientCORE is a client which sends commands to server, you can modify it if you are familiar with python, or write your own script in any programming language. F9LanderClientCORE represents Python API.

First start the server F9LanderCORE.py and then you can send string with list [up, left, right, new] to socket ('127.0.0.1', 50007). Up, Left, Right and New can be 1 or 0.

You can modify socket address in server code: F9LanderCORE.py line 301-303.

As output you will get string with list of dictionaries [{}, {}, {}] with information about every object in simulation.

__To show opened sockets in Ubuntu__

```bash
$ netstat -ntlp | grep LISTEN
```

______________________________________________

###Files:

F9LanderCORE.py - main class | server |

F9LanderClientCORE.py - external control script | client | Python API |

./experiments - folder with experimental scripts
./res - folder with resources

**^_^**
______________________________________________
