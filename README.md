# Linux 102 Class
This class is intended as a follow-on to the [Code Academy command line
course](https://www.codecademy.com/learn/learn-the-command-line).

Flay's draft slides are
[here](https://docs.google.com/presentation/d/1dG1hlHACDqVnNHmp1q0ZpJGPUYW2xI-qqSoXgHMFq18/edit#slide=id.g1b3d4c385b_1_25).

# Infrastructure Components
This class runs on a multiuser VM.  The management account on the VM runs a
browser-based SSH server so that users can log into the VM without any tools
besides a web browser, and a registration application that allows class
participants to generate their own SSH accounts.

The browser-based SSH server uses [WebSSH](https://pypi.org/project/webssh/)

The registration application is a small [Flask](http://flask.pocoo.org/)
webapp.  The CSS for the registration application is based on styles from [this
site](http://bettermotherfuckingwebsite.com/).

# One-time setup

## Create the Linux class user group
Accounts for class participants are created in a group called `linux_class` to
simplify tracking and management.  To create the group, run:

```
sudo adduser --group linux_class
```

## Set up the virtual environment
The SSH and registration applications are written to work with the latest
version of Python.  [Pyenv](https://github.com/pyenv/pyenv) makes it easy to
use your Python version of choice and create independent virtual environments.

Once `pyenv` and `pyenv-virtualenv` are installed, run:

```
pyenv install 3.7.2
pyenv virtualenv 3.7.2 class
pyenv activate class
pip install --upgrade pip
cd ~/linux_class
pip install -r requirements.txt
```

# Every time you run the class
The registration app runs on port 5000.
The Web SSH app runs on port 8000.

## Connect the VM to the network
* Start the Ubuntu server with a bridged network connection so it appears as
  another computer on the network.
* Log into the mplough account.
* Get the IP address of the machine.

## Run the registration app
It's not possible to run `adduser` as not root, even if it's `suid`.  So we
have to run the registration app like this:

```
cd ~/linux_class/registration_app
sudo -s
pyenv activate class
export FLASK_APP=registration_app.py
/home/mplough/.pyenv/shims/flask run --host 0.0.0.0 -p 5000
```

I don't like this solution as it involves running a flask app as root, but it's
expedient and the risk is acceptable given the isolated and snapshotted nature
of the VM.

## Run the Web SSH server
* Navigate to `/home/mplough/linux_class` directory and run:

```
wssh --port=8000
```


# Manual setup
## Add users

From `/home/mplough/linux_class/survey_app`,

```
sudo adduser --conf ./adduser.conf --ingroup linux_class [username]
```

## Remove users
Nuke a user plus their home directory and files like so:

```
sudo userdel -r user
```

## Skeleton directory
The `adduser.conf` file in the `survey_app` folder directs `adduser` to create
a user with a home directory populated by the skeleton in the `skel` folder in
this folder.

Note that the `adduser.conf` file includes an absolute path.  I haven't tested
it with relative paths, so you'll either need to change the absolute path to
fit or you can test relative paths.
