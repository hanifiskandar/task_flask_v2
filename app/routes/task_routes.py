from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, make_response
from flask_login import login_required, current_user
from app.models import Task
from app.forms import TaskForm
from app import db
from weasyprint import HTML
from io import BytesIO

task_bp = Blueprint('task', __name__, url_prefix="/tasks")

@task_bp.route("/")
@login_required
def list_tasks():
    priority = request.args.get('priority')
    status = request.args.get('status')

    query = Task.query.filter_by(user_id=current_user.id)

    if priority:
        query = query.filter_by(priority=priority)
    if status:
        query = query.filter_by(status=int(status))

    tasks = query.order_by(Task.due_date).all()
    return render_template("tasks/index.html", tasks=tasks)


@task_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task created successfully!", "success")
        return redirect(url_for("task.list_tasks"))
    return render_template("tasks/create.html", form=form)


@task_bp.route("/<int:id>")
@login_required
def show_task(id):
    task = Task.query.get_or_404(id)
    return render_template("tasks/show.html", task=task)


@task_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.start_date = form.start_date.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        task.status = form.status.data
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for("task.list_tasks"))

    return render_template("tasks/edit.html", form=form, task=task)


@task_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "info")
    return redirect(url_for("task.list_tasks"))


@task_bp.route('/pdf')
@login_required
def export_tasks_pdf():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all()
    html = render_template('tasks/pdf.html', tasks=tasks)

    pdf_file = BytesIO()
    HTML(string=html).write_pdf(pdf_file)
    pdf_file.seek(0)

    response = make_response(pdf_file.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=tasks.pdf'
    return response
