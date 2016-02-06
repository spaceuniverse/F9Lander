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

To change type of control fix line 35 in F9LanderCORE.py

```bash
self.commands = "socket"   # "keyboard" "socket"
```

**"keyboard"**

**w** - main engine

**a** - left engine

**d** - right engine

**n, space** - restart game (new rocket)

**"socket"**

('127.0.0.1', 50007)

Send list [1, 1, 1, 0] to socket where [up, left, right, new]

1 - active

0 - off

______________________________________________

###Information:

To run in "keyboard" mode fix line 35 in F9LanderCORE.py

```bash
Run in console

$ python F9LanderCORE.py
```

To run in "socket" mode fix line 35 in F9LanderCORE.py

```bash
Run in first console

$ python F9LanderCORE.py

Then run in second console

$ python F9LanderClientCORE.py
```

To show opened sockets in Ubuntu

```bash
$ netstat -ntlp | grep LISTEN
```

______________________________________________

###Files:

F9LanderCORE.py - main class | server |

F9LanderClientCORE.py - external control script | client |

./experiments - folder with experimental scripts

**^_^**
______________________________________________
