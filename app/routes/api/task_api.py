from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, make_response,jsonify
from flask_login import login_required, current_user
from app.models import Task
from app.forms import TaskForm
from app import db
from io import BytesIO

task_api = Blueprint("task_api", __name__, url_prefix="/api/tasks")

# @task_api.route("/")
# @login_required
# def list_tasks():
#     priority = request.args.get('priority')
#     status = request.args.get('status')

#     query = Task.query.filter_by(user_id=current_user.id)

#     if priority:
#         query = query.filter_by(priority=priority)
#     if status:
#         query = query.filter_by(status=int(status))

#     tasks = query.order_by(Task.due_date).all()
#     return render_template("tasks/index.html", tasks=tasks)


# @task_api.route("/", methods=["GET"])
# def get_tasks():
#     tasks = Task.query.all()
#     data = []
#     for task in tasks:
#         data.append({
#             "id": task.id,
#             "title": task.title,
#             "description": task.description,
#             "start_date": task.start_date.isoformat() if task.start_date else None,
#             "due_date": task.due_date.isoformat() if task.due_date else None,
#             "priority": task.priority.capitalize(),
#             "status": {1: "To Do", 2: "Doing", 3: "Done"}.get(task.status, "Unknown")
#         })
#     return jsonify(data)


@task_api.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@task_api.route("/<int:id>", methods=["GET"])
def show_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@task_api.route("/", methods=["POST"])
def store_task():
    data = request.get_json()

    task = Task(
        title=data.get("title"),
        description=data.get("description"),
        start_date=data.get("start_date"),
        due_date=data.get("due_date"),
        priority=data.get("priority", "medium").lower(),
        status=data.get("status", 1),
        user_id=data.get("user_id")  # or get from `current_user.id` if using auth
    )

    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@task_api.route("/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.start_date = data.get("start_date", task.start_date)
    task.due_date = data.get("due_date", task.due_date)
    task.priority = data.get("priority", task.priority).lower()
    task.status = data.get("status", task.status)

    db.session.commit()
    return jsonify(task.to_dict())

@task_api.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})




