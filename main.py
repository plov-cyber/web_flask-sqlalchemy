from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from data import db_session
from data.categories import HazardCategory
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from depform import DepForm
from regform import RegisterForm
from loginform import LoginForm
from jobform import JobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.run()


@app.route('/')
def job_journal():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    d = {
        'title': 'Works log',
        'jobs': jobs
    }
    return render_template('job_journal.html', **d)


@app.route('/departments')
def department_journal():
    session = db_session.create_session()
    deps = session.query(Department).all()
    d = {
        'title': 'List of Departments',
        'deps': deps
    }
    return render_template('dep_journal.html', **d)


@app.route('/register', methods=["GET", "POST"])
def reg_form():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('reg_form.html', title='Регистрация', form=form,
                                   message='Passwords are different')
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('reg_form.html', title='Регистрация', form=form, message='User is already exists!')
        # noinspection PyArgumentList
        user = User(
            login=form.login.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('reg_form.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['POST', 'GET'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        # noinspection PyArgumentList
        job = Jobs(
            job=form.job_title.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            is_finished=form.is_finished.data,
            collaborators=form.collaborators.data
        )
        for category_id in list(map(int, form.category.data.split(', '))):
            category = session.query(HazardCategory).get(category_id)
            session.expunge(category)
            job.categories.append(category)
        current_user.job.append(job)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('job_form.html', title='Adding a job', form=form)


@app.route('/adddep', methods=['POST', 'GET'])
@login_required
def add_dep():
    form = DepForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        # noinspection PyArgumentList
        dep = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        current_user.department.append(dep)
        session.merge(current_user)
        session.commit()
        return redirect('/departments')
    return render_template('dep_form.html', title='Adding a department', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobForm()
    if request.method == 'GET':
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id, ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if jobs:
            form.job_title.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.is_finished.data = jobs.is_finished
            form.collaborators.data = jobs.collaborators
            form.category.data = ', '.join([str(item.id) for item in jobs.categories])
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id, ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if jobs:
            jobs.job = form.job_title.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.is_finished = form.is_finished.data
            jobs.collaborators = form.collaborators.data
            jobs.categories.clear()
            for category_id in list(map(int, form.category.data.split(', '))):
                category = session.query(HazardCategory).get(category_id)
                session.expunge(category)
                jobs.categories.append(category)
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job_form.html', title='Editing a job', form=form)


@app.route('/deps/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_deps(id):
    form = DepForm()
    if request.method == 'GET':
        session = db_session.create_session()
        deps = session.query(Department).filter(Department.id == id,
                                                ((Department.user == current_user) | (current_user.id == 1))).first()
        if deps:
            form.title.data = deps.title
            form.chief.data = deps.chief
            form.members.data = deps.members
            form.email.data = deps.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        deps = session.query(Department).filter(Department.id == id,
                                                ((Department.user == current_user) | (current_user.id == 1))).first()
        if deps:
            deps.title = form.title.data
            deps.chief = form.chief.data
            deps.members = form.members.data
            deps.email = form.email.data
            session.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('dep_form.html', title='Editing a department', form=form)


@app.route('/jobs_delete/<int:id>', methods=['POST', 'GET'])
@login_required
def jobs_delete(id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == id, ((Jobs.user == current_user) | (current_user.id == 1))).first()
    if jobs:
        session.delete(jobs)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/deps_delete/<int:id>', methods=['POST', 'GET'])
@login_required
def deps_delete(id):
    session = db_session.create_session()
    deps = session.query(Department).filter(Department.id == id,
                                            ((Department.user == current_user) | (Department.id == 1))).first()
    if deps:
        session.delete(deps)
        session.commit()
    else:
        abort(404)
    return redirect('/departments')


if __name__ == '__main__':
    main()
