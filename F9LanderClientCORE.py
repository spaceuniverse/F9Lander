# -------------------------------------------------- #
# --------------------_F9_Lander_------------------- #
# ----------------------CLIENT---------------------- #
# -------------------------------------------------- #

import socket
import numpy as np

# for delay in debug launch
import time

# -------------------------------------------------- #

sock = socket.socket()
sock.connect(('127.0.0.1', 50007))
# send init command | new game
sock.send(str([0, 0, 0, 1]))

while True:
    # eval is bad idea but it works
    data = eval(sock.recv(1024))
    #
    if not data:
        break
    # print data, type(data)
    agent_state = (item for item in data if item["type"] == "actor").next()
    platform_state = (item for item in data if item["type"] == "decoration").next()
    system_state = (item for item in data if item["type"] == "system").next()
    print agent_state, platform_state, system_state
    # output example
    # {'dist': 30.396299362182617, 'contact_time': 0, 'vx': -21.335142135620117, 'vy': 0.9811121821403503,
    # 'angle': -0.05268074572086334, 'px': 43.301612854003906, 'py': 42.239990234375, 'live': True, 'contact': False,
    # 'fuel': 791.9, 'type': 'actor', 'enj': True, 'wind': 32.0} {'angle': 0.01994907110929489,
    # 'px': 52.044925689697266, 'py': 4.305685997009277, 'vx': 0.8977082371711731, 'vy': 0.7780137658119202,
    # 'type': 'decoration'} {'step': 99, 'type': 'system', 'flight_status': 'none'}
    rnd = np.random.random_sample()
    if rnd >= 0.7:
        rnd = 1
    else:
        rnd = 0
    # system_state["flight_status"] | "none", "landed", "destroyed"
    # "none" means that we don't know, whether we landed or destroyed
    if system_state["flight_status"] == "destroyed" or (agent_state["fuel"] <= 0.0 and agent_state["dist"] >= 99.0):
        new = 1
    else:
        new = 0
    # keys map [up, left, right, new]
    sock.send(str([rnd, 1, 1, new]))
    # time.sleep(3)

sock.close()
print "Socket closed"
# -------------------------------------------------- #
# --------------- you have landed ------------------ #
# -------------------------------------------------- #