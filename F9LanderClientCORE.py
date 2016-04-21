# -------------------------------------------------- #
# --------------------_F9_Lander_------------------- #
# ----------------------CLIENT---------------------- #
# -------------------------------------------------- #

import numpy as np

from F9utils import F9GameClient
from F9utils import RLAgent

# for delay in debug launch
import time

# -------------------------------------------------- #


class SimpleAgent(RLAgent):
    def __init__(self, client):
        self.client = client

    def getAction(self, state):
        # state example
        # ({'dist': 30.396299362182617, 'contact_time': 0, 'vx': -21.335142135620117, 'vy': 0.9811121821403503,
        # 'angle': -0.05268074572086334, 'px': 43.301612854003906, 'py': 42.239990234375, 'live': True, 'contact': False,
        # 'fuel': 791.9, 'type': 'actor', 'enj': True, 'wind': 32.0}, {'angle': 0.01994907110929489,
        # 'px': 52.044925689697266, 'py': 4.305685997009277, 'vx': 0.8977082371711731, 'vy': 0.7780137658119202,
        # 'type': 'decoration'}, {'step': 99, 'type': 'system', 'flight_status': 'none'})
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
        agent, platform, system = state
        actions = self.client.actions(state)  # Get legal actions for state

        # Agent if-then-else logic example
        if agent["vy"] <= -7.0:
            action = actions[-1]  # Full throttle
        else:
            action = actions[0]  # Do nothing

        if agent["angle"] < 0.0:
            action[1] = 1  # Left nozzle burn
        else:
            action[1] = 0

        if agent["angle"] > 0.0:
            action[2] = 1  # Right nozzle burn
        else:
            action[2] = 0

        return action

    def provideFeedback(self, state, action, reward, new_state):
        # Do nothing
        pass

# -------------------------------------------------- #


def solve():
    # Setup agent
    client = F9GameClient()
    ai = SimpleAgent(client)
    state = client.curState  # Observe current state

    while True:
        action = ai.getAction(state)                            # Decide what to do
        client.doAction(action)                                 # Act
        new_state = client.curState                             # Observe new state
        reward = client.getReward(new_state)                    # Observe reward
        ai.provideFeedback(state, action, reward, new_state)    # Provide feeback to the agent

        agent, platform, system = new_state
        print "Agent state %s\n Platform state %s\n System state %s\n Reward %s\n" % (agent, platform, system, reward)

        if client.isTerminalState(new_state):
            client.reset_game()
            state = client.curState
        else:
            state = new_state

if __name__ == "__main__":
    solve()

# -------------------------------------------------- #
# --------------- you have landed ------------------ #
# -------------------------------------------------- #
