# backend/app/services/task_service.py
from app import db
from app.models import Task
from datetime import datetime

class TaskService:
    @staticmethod
    def create_task(user_id, title, description, due_date, due_time):
        if not isinstance(due_date, datetime.date):
            raise ValueError("due_date must be a datetime.date object")
        if not isinstance(due_time, datetime.time):
            raise ValueError("due_time must be a datetime.time object")
        new_task = Task(
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            due_time=due_time
        )
        db.session.add(new_task)
        db.session.commit()
        return TaskService.task_to_dict(new_task)

    @staticmethod
    def get_all_tasks(user_id):
        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.due_date).all()
        return [TaskService.task_to_dict(task) for task in tasks]

    @staticmethod
    def get_task(user_id, task_id):
        task = Task.query.filter_by(user_id=user_id, id=task_id).first()
        return TaskService.task_to_dict(task) if task else None

    @staticmethod
    def update_task(user_id, task_id, title=None, description=None, due_date=None, due_time=None, is_complete=None):
        task = Task.query.filter_by(user_id=user_id, id=task_id).first()
        if not task:
            return None
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if due_date is not None:
            if not isinstance(due_date, datetime.date):
                raise ValueError("due_date must be a datetime.date object")
            task.due_date = due_date
        if due_time is not None:
            if not isinstance(due_time, datetime.time):
                raise ValueError("due_time must be a datetime.time object")
            task.due_time = due_time
        if is_complete is not None:
            task.is_complete = is_complete
        db.session.commit()
        return TaskService.task_to_dict(task)

    @staticmethod
    def delete_task(user_id, task_id):
        task = Task.query.filter_by(user_id=user_id, id=task_id).first()
        if not task:
            return False
        db.session.delete(task)
        db.session.commit()
        return True

    @staticmethod
    def mark_task_complete(user_id, task_id):
        task = Task.query.filter_by(user_id=user_id, id=task_id).first()
        if not task:
            return None
        task.is_complete = True
        db.session.commit()
        return TaskService.task_to_dict(task)
    
    @staticmethod
    def task_to_dict(task):
        if not task:
            return None
        return {
            'id': task.id,
            'user_id': task.user_id,
            'title': task.title,
            'description': task.description,
            'due_date': str(task.due_date),
            'due_time': str(task.due_time),
            'is_complete': task.is_complete,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        }