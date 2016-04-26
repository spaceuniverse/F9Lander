# -------------------------------------------------- #
# --------------------_F9_Lander_------------------- #
# -----------------REST_CLIENT_EXAMPLE-------------- #
# -------------------------------------------------- #

import urllib

# for delay in debug launch
import time

# -------------------------------------------------- #

# send init command | new game
url = "http://localhost:5000/0001"
answer = urllib.urlopen(url).read()

while True:
    # time.sleep(1.0)
    answer = answer.replace("true", "True")
    answer = answer.replace("false", "False")
    data = eval(answer)
    print data, type(data)
    #
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
    url = "http://localhost:5000/" + str(e1) + str(e2) + str(e3) + str(new)
    answer = urllib.urlopen(url).read()


# -------------------------------------------------- #
# --------------- you have landed ------------------ #
# -------------------------------------------------- #
