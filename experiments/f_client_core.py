from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Emulator():

    def __init__(self):
        self.counter = 0
        self.answer = " __ "
        self.up = "1000"
        self.down = "0100"
        self.left = "0010"
        self.right = "0001"

    def count(self, data):
        self.counter += 1
        if data == self.up:
            self.answer = " _up_ "
        elif data == self.down:
            self.answer = " _down_ "
        elif data == self.left:
            self.answer = " _left_ "
        elif data == self.right:
            self.answer = " _right_ "
        else:
            self.answer = " _none_ "
        return self.answer + str(self.counter)

obj = Emulator()


class UserAPI(Resource):

    def get(self, command):
        return obj.count(command)

api.add_resource(UserAPI, '/<string:command>')

if __name__ == '__main__':
    app.run(debug=False)