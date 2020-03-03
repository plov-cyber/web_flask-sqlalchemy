from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.sqlite")
    surnames = ['Scott', 'Stinson', 'Mosby', 'Kandy']
    names = ['Ridley', 'Barni', 'Ted', 'Marshall']
    ages = [21, 22, 25, 23]
    positions = ['captain', 'general', 'engineer', 'doctor']
    specialities = ['research engineer', 'manager', 'programmer', 'surgeon']
    addresses = ['module_1', 'section_8', 'module_3', 'section_1']
    emails = ['scott_chief@mars.org', 'bar_stin@space.com', 'ted_best@sun.ru', 'candy_marsh@ship.co']
    session = db_session.create_session()
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
    app.run()


if __name__ == '__main__':
    main()
