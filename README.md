# WizFood
Wizfood is Capstone project at school to graduate

## Run Virtual Environment

Virtual environment is a key component in ensuring that the application is configured in the right environment

##### Requirements
* Python 3
* Pip 3
* SWI-Prolog

```bash
$ brew install python3
$ brew install swi-prolog
```

Pip3 is installed with Python3

##### Installation
To install virtualenv via pip run:
```bash
$ pip3 install virtualenv
```

##### Usage
Creation of virtualenv:

    $ virtualenv -p python3 venv

If the above code does not work, you could also do

    $ python3 -m venv venv

To activate the virtualenv:

    $ source venv/bin/activate

Or, if you are **using Windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

    $ venv\Scripts\activate

To deactivate the virtualenv (after you finished working):

    $ deactivate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt

## Run Application

### Docker
Build:

    $ docker build -t wizfood:1.0 . 

Run:

    $ docker run --rm -p 5000:5000 wizfood:1.0

### Without Docker
Start the server by running:

    $ export FLASK_ENV=development
    $ export ENV=local
    $ export FLASK_APP=app
    $ export PYTHONPATH=.
    $ python3 -m flask run

## Unit Tests
To run the unit tests use the following commands:

    $ python3 -m venv venv_unit
    $ source venv_unit/bin/activate
    $ pip install -r requirements.txt
    $ pytest unit_test

To check the coverage of the test

    $ pytest --cov=app unit_test/