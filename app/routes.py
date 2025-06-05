from app import app,db
from flask import render_template,request, redirect, url_for
from app.models import Task
from app.forms import TaskForm


@app.route("/")
def home():
    return render_template("index.html", title="Home Page")

@app.route("/about")
def about():
    return render_template("about.html", title="About Parameter Here")


@app.route("/tasks")
def task_lists():
    tasks = Task.query.all()
    return render_template("tasks/index.html",tasks=tasks)

# @app.route("/tasks/create", methods=["GET","POST"])
# def task_create():
#     if request.method == "POST":
#         # title = request.form["title"]
#         # description = request.form["description"]
#         # new_task = Task(title=title, description=description)
#         data = request.form.to_dict()
#         new_task = Task(**data)
#         db.session.add(new_task)
#         db.session.commit()
#         return redirect(url_for("task_lists"))
#     return render_template("tasks/create.html")


@app.route("/tasks/create", methods=["GET", "POST"])
def task_create():
    form = TaskForm()

    if form.validate_on_submit():
        # This only runs if method is POST and validators pass
        new_task = Task(
            title=form.title.data,
            description=form.description.data
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("task_lists"))  # or whatever your list view is

    return render_template("tasks/create.html", form=form)


@app.route("/tasks/<int:id>")
def task_show(id):
    task = Task.query.get_or_404(id)
    return render_template("tasks/show.html", task=task)

# @app.route("/tasks/<int:id>/edit", methods=["GET","POST"])
# def task_edit(id):
#     task = Task.query.get_or_404(id)
#     if request.method == "POST":
#         task.title = request.form["title"]
#         task.description = request.form["description"]
#         db.session.commit()
#         return redirect(url_for("task_lists"))
#     return render_template("tasks/edit.html", task=task)

@app.route("/tasks/<int:id>/edit", methods=["GET", "POST"])
def task_edit(id):
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        db.session.commit()
        return redirect(url_for("task_lists"))

    return render_template("tasks/edit.html", form=form)

@app.route("/task/<int:id>/delete", methods=["POST"])
def task_delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("task_list"))
        