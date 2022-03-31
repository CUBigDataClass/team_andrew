from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

#Setup App
app = Flask(__name__)
api_flask = Api(app)

#Create Empty Dict
todo_list = {}
''' SAMPLE DICTIONARY STRUCTURE
todo_list = {
"Note_1" : {
    1: {"task": "Write Code", "description": "use any language"},
    2: {"task": 'Task2', "description": "task 2 activated."},
    3: {"task": "Task3", "description": "task 3 activated."},
          }
            }
'''
#Initiate Parser Request for post and put method
parser = reqparse.RequestParser()
parser.add_argument("task", type=str, help="Required to add task", required=True)
parser.add_argument("description", type=str, help="Required to add description.", required=True)

parser1 = reqparse.RequestParser()
parser1.add_argument("task", type=str)
parser1.add_argument("description")

#Class for Adding, Displaying, Deleting, and Completing tasks in a Note.
class TodoTask(Resource):
    def get(self, todo_id, note_id):
        return todo_list[note_id][todo_id]

    def post(self, todo_id, note_id):
        args = parser.parse_args()
        if note_id == {}:
            abort(404, message="Note Empty")

        if note_id not in todo_list:
            abort(404, message="Note Not Present")
        if todo_id in todo_list[note_id]:
            abort(404, message="Task Already Present")
        todo_list[note_id][todo_id] = {"task": args["task"], "description": args["description"]}
        return todo_list[note_id]

    def put(self, todo_id, note_id):
        args = parser1.parse_args()
        if todo_id not in todo_list[note_id]:
            abort(404, message="Task Not Present")
        todo_list[note_id][todo_id]["description"] = "Completed"
        return todo_list[note_id][todo_id]


    def delete(self, todo_id, note_id):
        if todo_id not in todo_list[note_id]:
            abort(404, message="Task Not Present")
        del todo_list[note_id][todo_id]
        return todo_list[note_id]

#Class to Add, and Delete a Note.
class Todo_Note(Resource):
    def post(self, note_id):
        if note_id == {}:
            abort(404, message="Note Empty")
        args = parser.parse_args()
        if note_id in todo_list:
            abort(404, message="Note Already Present")
        todo_list[note_id] = {}
        todo_list[note_id][1] = {"task": args["task"], "description": args["description"]}
        return todo_list

    def delete(self, note_id):
        if note_id not in todo_list:
            abort(404, message="Note Not Present")
        del todo_list[note_id]
        return todo_list
#Class to Display all Notes and Tasks
class TodolistAll(Resource):
    def get(self):
        return todo_list

#Adding resources and Setting End points.
api_flask.add_resource(TodoTask, '/todo_task/<int:todo_id>/<string:note_id>')
api_flask.add_resource(Todo_Note, '/todo_note/<string:note_id>')
api_flask.add_resource(TodolistAll, '/todo')

if __name__ == '__main__':
    app.run(debug=True)
