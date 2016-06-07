# -------------------------------------------------- #
# --------------------_F9_Lander_------------------- #
# ----------------------WRAPPER--------------------- #
# -------------------------------------------------- #
# imports

import socket
import cPickle as pickle
import glob
import os

# -------------------------------------------------- #

RESET_CMD = str([0, 0, 0, 1])
DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 50007

# -------------------------------------------------- #


class F9GameClient:
    """Game wrapper"""
    def __init__(self, ip=DEFAULT_IP, port=DEFAULT_PORT):
        self.socket = socket.socket()
        self.socket.connect((ip, port))
        self.curState = None
        self.reset_game()
        self.totalScore = 0

    def reset_game(self):
        # send init command | new game
        self.socket.send(RESET_CMD)
        self.curState = self.getServerState()

    def isTerminalState(self, state):
        # system["flight_status"] | "none", "landed", "destroyed"
        # "none" means that we don't know, whether we landed or destroyed
        agent, _, system = state
        status = False
        if system["flight_status"] == "destroyed" or system["flight_status"] == "landed" or agent["py"] <= 0.0:
            status = True
        return status

    def getReward(self, state):
        agent, _, system = state
        score = 0.0
        if system["flight_status"] == "landed":
            score = 100.0
        elif self.isTerminalState(state):
            # MAYBE BUG ---> delete "or system["flight_status"] == "landed" from isTerminalState
            # but elif fixed it, so it's feature
            score = -100.0
        else:  # Remove this if you don't want to use handcrafted heuristic
            score = 1.0 / (1 + agent["dist"]) + agent["contact_time"]
        self.totalScore += score
        return score

    def actions(self, state=None):
        # returns legal actions, keys map [up, left, right, reset_game]
        act = [[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0], [1,1,0,0], [0,1,1,0], [1,0,1,0], [1,1,1,0]]
        return act

    def getServerState(self):
        # getting data from server
        data = eval(self.socket.recv(1024))
        state = None
        if data:
            agent_state = (item for item in data if item["type"] == "actor").next()
            platform_state = (item for item in data if item["type"] == "decoration").next()
            system_state = (item for item in data if item["type"] == "system").next()
            state = [agent_state, platform_state, system_state]
        return state

    def doAction(self, action):
        # act in the game environment
        if any([action == act for act in self.actions()]):
            self.socket.send(str(action))
            self.curState = self.getServerState()
        else:
            print "Invalid Action"

# -------------------------------------------------- #


class RLAgent:
    """Abstract class: an RLAgent performs reinforcement learning.
    The game client will call getAction() to get an action, perform the action, and
    then provide feedback (via provideFeedback()) to the RL algorithm, so it can learn."""
    def getAction(self, state):
        raise NotImplementedError("Override me")

    def provideFeedback(self, state, action, reward, new_state):
        raise NotImplementedError("Override me")

# -------------------------------------------------- #


class Snapshot:
    def __init__(self, prefix):
        self.prefix = prefix

    def save(self, state, num):
        file_path = '_'.join([self.prefix, str(num)])
        f = file(''.join([file_path, '.pkl']), 'wb')
        pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    def load(self):
        file_path = glob.glob(''.join([self.prefix, "*_[0-9]*.pkl"]))
        file_path.sort(key=os.path.getctime)
        state = None
        if len(file_path):
            f = file(file_path[-1], 'rb')
            print "Loading snapshot", file_path[-1]
            state = pickle.load(f)
            f.close()
        return state


# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
