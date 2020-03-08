from flask import Flask, render_template, request
from flask_login import LoginManager
from data import db_session
from data.users import User
from data.jobs import Jobs
from regform import RegisterForm

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


def add_users():
    session = db_session.create_session()
    surnames = ['Scott', 'Stinson', 'Mosby', 'Kandy']
    names = ['Ridley', 'Barni', 'Ted', 'Marshall']
    ages = [21, 22, 25, 23]
    positions = ['captain', 'general', 'engineer', 'doctor']
    specialities = ['research engineer', 'manager', 'programmer', 'surgeon']
    addresses = ['module_1', 'section_8', 'module_3', 'section_1']
    emails = ['scott_chief@mars.org', 'bar_stin@space.com', 'ted_best@sun.ru', 'candy_marsh@ship.co']
    for i in range(4):
        user = User()
        user.surname = surnames[i]
        user.name = names[i]
        user.age = ages[i]
        user.position = positions[i]
        user.speciality = specialities[i]
        user.address = addresses[i]
        user.email = emails[i]
        session.add(user)
    session.commit()


def add_jobs():
    session = db_session.create_session()
    team_leaders = [1, 2, 3, 4]
    jobs = ['Deployment of residental modules 1 and 2',
            'Exploration of mineral resources',
            'Development of a management system',
            'Building of module 3']
    work_sizes = [15, 25, 20, 100]
    collaborators = ['2, 3', '4, 3', '5', '1, 2, 3, 5']
    are_finished = [False, False, True, False]
    for i in range(4):
        job = Jobs()
        job.team_leader = team_leaders[i]
        job.job = jobs[i]
        job.work_size = work_sizes[i]
        job.collaborators = collaborators[i]
        job.is_finished = are_finished[i]
        session.add(job)
    session.commit()


@app.route('/')
def job_journal():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = []
    for i in range(len(jobs)):
        users.append(session.query(User).filter(User.id == jobs[i].team_leader).first())
    d = {
        'title': 'Журнал работ',
        'jobs': jobs,
        'users': users
    }
    return render_template('job_journal.html', **d)


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
        return 'Регистрация прошла успешно!'
    return render_template('reg_form.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
