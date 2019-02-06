import datetime
import pathlib
import random
import subprocess

from flask import Flask, flash, request, render_template


app = Flask(__name__)


SURVEY_APP_ROOT = pathlib.Path(__file__).parent


def all_users():
    """Return a list of all users on the system."""
    with open('/etc/passwd', 'r') as f:
        return {line.partition(':')[0] for line in f}


def is_badword(word):
    badfile = SURVEY_APP_ROOT / 'bad-words.txt'
    with badfile.open() as f:
        badwords = {line.strip() for line in f}

    return word.lower() in badwords


def make_integer_username():
    """Make a username that's u followed by an integer."""
    while True:
        username = 'u{}'.format(random.randint(1000, 10000))
        if username not in all_users():
            return username


def make_username(name):
    """Make a username from name that's not profane."""
    name = ''.join([c for c in name if c.isalpha() or c.isspace()])
    name_parts = name.lower().split()

    if not name_parts:
        return make_integer_username()

    if len(name_parts) == 1:
        username = name_parts[0]
        if is_badword(username) or username in all_users():
            return make_integer_username()
        return username

    for i in range(len(name_parts[0])):
        username = name_parts[0][0:i+1] + name_parts[-1]
        if is_badword(username) or username in all_users():
            continue
        return username

    return make_integer_username()


def user_exists(username):
    """Return True if username exists; else False."""
    return subprocess.run(['id', '-u', username]).returncode == 0


def create_user(username, password, name):
    adduser_input = '\n'.join([
        password,  # Password
        password,  # Confirm Password
        name,  # Full Name
        '',  # Room Number
        '',  # Work Phone
        '',  # Home Phone
        datetime.datetime.now().strftime('%x'),  # Other
        'Y',  # Yes, it's correct
    ]).encode()

    subprocess.run(
        [
            'adduser',
            '--conf', str(SURVEY_APP_ROOT / 'adduser.conf'),
            '--ingroup', 'linux_class',
            username
        ],
        input=adduser_input,
        check=True
    )


@app.route('/', methods=('GET', 'POST'))
def class_registration():
    if request.method == 'GET':
        return render_template('register.html')

    # POST ...
    password = request.form['password']
    password2 = request.form['password2']
    if len(password) < 8:
        errors = ['Password is too short!']
        return render_template('register.html', errors=errors)
    if password != password2:
        errors = ["Password doesn't match!"]
        return render_template('register.html', errors=errors)

    name = request.form['name']
    username = make_username(name)

    try:
        create_user(username, password, name)
    except Exception as e:
        errors = ["Couldn't create user!"]
        return render_template('register.html', errors=errors)

    return render_template('registered.html', name=name, username=username)
