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

To change type of control - fix line 35 in F9LanderCORE.py

```bash
self.commands = "keyboard"   # "keyboard" "socket" | in future "fifo"
```

__**"keyboard"**__

**w** - main engine

**a** - left engine

**d** - right engine

**n, space** - restart game (new rocket) | SPACE works even in external control modes

For more information read help.pdf

__**"socket"**__

Socket address ('127.0.0.1', 50007)

Send list [1, 1, 1, 0] to socket, where entities means [up, left, right, new]

1 - activate, 0 - do nothing

______________________________________________

###Information:

__To run in "keyboard" mode - fix line 35 in F9LanderCORE.py__

Run in console:

```bash
$ python F9LanderCORE.py
```

__To run in "socket" mode fix - line 35 in F9LanderCORE.py__

Run in first console

```bash
$ python F9LanderCORE.py
```

Then run in second console

```bash
$ python F9LanderClientCORE.py
```

F9LanderClientCORE is a client which sends commands to server, you can modify it or write your own script in any programming language

Just start server before and send list [up, left, right, new] to socket ('127.0.0.1', 50007) | (up, left, right, new can be 1 or 0)

You can modify this address in server code (F9LanderCORE line 301-303)

__To show opened sockets in Ubuntu__

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
