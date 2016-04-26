from flask import Flask, request
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


class Data(Resource):

    def get(self):
        return {"data: ": obj.answer}

    def put(self):
        data = request.form['data']
        return obj.count(data)

api.add_resource(Data, '/')

if __name__ == '__main__':
    app.run(debug=True)