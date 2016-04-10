import socket

RESET_CMD = str([0, 0, 0, 1])
DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 50007

class F9GameClient:
    """Game wraper"""
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
        if system["flight_status"] == "destroyed" or system["flight_status"] == "landed" or \
                agent["fuel"] <= 0.0 or agent["py"] <= 0.0:
            status = True

        return status

    def getReward(self, state):
        agent, _, system = state
        if system["flight_status"] == "landed":
            score = 2.0
        elif self.isTerminalState(state):
            score = -2.0
        elif agent["dist"] > 0.5:  # Remove this if you don't want to use handcrafted heuristic
            score = -1.0 + (1.0 / agent["dist"]) + agent["contact_time"]
        else:
            score = 0.0

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
        if any([action == act for act in self.actions()]):
            self.socket.send(str(action))
            self.curState = self.getServerState()
        else:
            print "Invalid Action"
