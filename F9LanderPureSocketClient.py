# -------------------------------------------------- #
# --------------------_F9_Lander_------------------- #
# -------------PURE_SOCKET_CLIENT_EXAMPLE----------- #
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
    # getting data from server
    # eval is bad idea but it works
    data = eval(sock.recv(1024))
    if not data:
        break
    # print data, type(data)
    agent_state = (item for item in data if item["type"] == "actor").next()
    platform_state = (item for item in data if item["type"] == "decoration").next()
    system_state = (item for item in data if item["type"] == "system").next()
    # print agent_state, platform_state, system_state
    print "{" + str(agent_state) + "," + str(platform_state) + "," + str(system_state) + "}" + ","
    # output example
    # {'dist': 30.396299362182617, 'contact_time': 0, 'vx': -21.335142135620117, 'vy': 0.9811121821403503,
    # 'angle': -0.05268074572086334, 'px': 43.301612854003906, 'py': 42.239990234375, 'live': True, 'contact': False,
    # 'fuel': 791.9, 'type': 'actor', 'enj': True, 'wind': 32.0}
    #
    # {'angle': 0.01994907110929489, 'px': 52.044925689697266, 'py': 4.305685997009277, 'vx': 0.8977082371711731,
    # 'vy': 0.7780137658119202, 'type': 'decoration'}
    #
    # {'step': 99, 'type': 'system', 'flight_status': 'none', 'action': [0, 0, 1, 0], 'is_terminal_state': False,
    # 'score': 25.16671304950599}
    #
    #
    # 'dist' - distance between two nearest points of rocket and a platform body
    #
    # 'contact_time' - time counter, which starts from the moment when rocket contacts with the platform
    #                  you need to keep contact with the platform for some time, without destroying yourself, to win
    #
    # 'vx' | 'vy' - vertical and horizontal velocity
    #
    # 'angle' - angle of hade
    #
    # 'px' | 'py' - coordinates of the body central point
    #
    # 'live' - still alive? "False" if not
    #
    # 'contact' - is there a contact with the platform? "False" if not
    #
    # 'fuel' - the amount of remaining fuel
    #
    # 'type' - type of the object | "actor" - rocket | "decoration" - platform | "system" - world
    #
    # 'enj' - are the engines workable? "False" if fuel tank is empty
    #
    # 'wind' - wind strength
    #
    # 'step' - iteration counter
    #
    # 'flight_status' - win or loss? | "landed" or "destroyed"?
    #                   "none" means that you don't know, whether you landed or destroyed, or maybe still flying
    #                   "landed" means that you won
    #
    # 'action' - action performed in the step
    #
    # 'is_terminal_state' - means that the system has reached it's terminal state: rocket landed or destroyed
    #                       or drowned etc.
    #                       Difference with 'flight_status' is in the point of view, 'flight_status' describes only the
    #                       rocket status but not whole system.
    #
    # 'score' - synthetic score, you can use it or write your own
    #
    # random move
    # rnd = np.random.random_sample()
    # if rnd >= 0.7:
    #    rnd = 1
    # else:
    #    rnd = 0
    #
    # if-then-else logic
    if agent_state["vy"] <= -7.0:
        e1 = 1
        e2 = 1
        e3 = 1
    else:
        e1 = 0
        e2 = 0
        e3 = 0
    if agent_state["angle"] < 0.0:
        e2 = 1
    else:
        e2 = 0
    if agent_state["angle"] > 0.0:
        e3 = 1
    else:
        e3 = 0
    # system_state["flight_status"] | "none", "landed", "destroyed"
    # "none" means that we don't know, whether we landed or destroyed
    if system_state["flight_status"] == "destroyed" or (agent_state["fuel"] <= 0.0 and agent_state["dist"] >= 70.0):
        new = 1
    else:
        new = 0
    # keys map [up, left, right, new]
    # sending command to server
    sock.send(str([e1, e2, e3, new]))
    # time.sleep(3)

sock.close()
print "Socket closed"

# -------------------------------------------------- #
# --------------- you have landed ------------------ #
# -------------------------------------------------- #
