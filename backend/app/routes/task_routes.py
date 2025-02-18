# backend/app/routes/task_routes.py

from flask import request, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from app.models import Task
from app.auth import authenticate
from app.services.task_service import TaskService
from datetime import datetime

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')
api = Api(task_bp)

# --- Argument Parsers ---
task_parser = reqparse.RequestParser()
task_parser.add_argument('title', type=str, required=True, help='Title is required')
task_parser.add_argument('description', type=str)
task_parser.add_argument('due_date', type=str, required=True, help='Due date is required (YYYY-MM-DD)')
task_parser.add_argument('due_time', type=str, required=True, help='Due time is required (HH:MM:SS)')

task_update_parser = reqparse.RequestParser()
task_update_parser.add_argument('title', type=str)
task_update_parser.add_argument('description', type=str)
task_update_parser.add_argument('due_date', type=str)
task_update_parser.add_argument('due_time', type=str)
task_update_parser.add_argument('is_complete', type=bool)

# --- Resource Classes ---
class TaskList(Resource):
    @authenticate
    def get(self, user):
        print("--- TaskList.get() called ---")  # Add this
        tasks = TaskService.get_all_tasks(user.id)
        return jsonify(tasks)

    @authenticate
    def post(self, user):
        print("--- TaskList.post() called ---")  # Add this
        args = task_parser.parse_args()
        try:
            due_date = datetime.strptime(args['due_date'], '%Y-%m-%d').date()
            due_time = datetime.strptime(args['due_time'], '%H:%M:%S').time()
            new_task = TaskService.create_task(
                user.id, args['title'], args['description'], due_date, due_time
            )
            return jsonify(new_task), 201
        except ValueError as e:
            print(f"--- ValueError in TaskList.post(): {e} ---")  # Add this
            return {'message': str(e)}, 400
        except Exception as e:
            print(f"--- Exception in TaskList.post(): {e} ---") # Add this
            return {'message': 'An error occurred while creating tasks.'}, 500

class TaskResource(Resource):
    @authenticate
    def get(self, user, task_id):
        print(f"--- TaskResource.get() called with task_id: {task_id} ---")  # Add this
        task = TaskService.get_task(user.id, task_id)
        if task:
            return jsonify(task)
        else:
            return {'message': 'Task not found'}, 404

    @authenticate
    def put(self, user, task_id):
        print(f"--- TaskResource.put() called with task_id: {task_id} ---")  # Add this
        args = task_update_parser.parse_args()
        try:
            due_date = datetime.strptime(args['due_date'], '%Y-%m-%d').date() if args['due_date'] else None
            due_time = datetime.strptime(args['due_time'], '%H:%M:%S').time() if args['due_time'] else None
            updated_task = TaskService.update_task(
                user.id, task_id, args['title'], args['description'],
                due_date, due_time, args.get('is_complete')
            )
            if updated_task:
                return jsonify(updated_task)
            else:
                return {'message': 'Task not found'}, 404
        except ValueError as e:
            print(f"--- ValueError in TaskResource.put(): {e} ---") # Add this
            return {'message': str(e)}, 400
        except Exception as e:
            print(f"--- Exception in TaskResource.put(): {e} ---")  # Add this
            return {'message':"Update failed"}, 400

    @authenticate
    def delete(self, user, task_id):
        print(f"--- TaskResource.delete() called with task_id: {task_id} ---")  # Add this
        if TaskService.delete_task(user.id, task_id):
            return {'message': 'Task deleted successfully'}, 200
        else:
            return {'message': 'Task not found'}, 404

    @authenticate
    def patch(self, user, task_id):  #For marking task complete
        print(f"--- TaskResource.patch() called with task_id: {task_id} ---")  # Add this
        try:
            task = TaskService.mark_task_complete(user.id, task_id)
            if(task):
                return jsonify(task), 200
            return {'message': 'Task not found'}, 404
        except Exception as e:
            print(f"--- Exception in TaskResource.patch(): {e} ---")  # Add this
            return {'message':"Update failed"}, 400

# --- Add resources to the API ---
api.add_resource(TaskList, '')
api.add_resource(TaskResource, '/<int:task_id>')