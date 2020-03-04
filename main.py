from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.sqlite")
    add_users()
    add_jobs()
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


if __name__ == '__main__':
    main()
